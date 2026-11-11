# -*- coding: utf-8 -*-
from lib import *
def build(name, lanes, nodes, edges, dpi=130):
    """lanes: [(id,title)], nodes: id->(lane,kind,label), edges: (a,b,label,opts)"""
    d = f'digraph G {{\n graph [rankdir=TB, splines=ortho, nodesep=0.5, ranksep=0.38, bgcolor=white, pad=0.3, newrank=true, fontname="{FONT}", fontsize=13];\n node [fontname="{FONT}", fontsize=11];\n edge [fontname="{FONT}", fontsize=10];\n'
    for lid,t in lanes:
        d += f' subgraph cluster_{lid} {{ label="{t}"; labelloc=t; style="filled"; fillcolor="#F7FBFE" ; color="#444444"; margin=18;\n'
        for n,(l,k,lab) in nodes.items():
            if l!=lid: continue
            lab = lab.replace('"','\\"')
            if k=='act': d += f'  {n} [shape=box, style=filled, fillcolor="{BLUE}", label="{lab}", margin="0.18,0.1"];\n'
            elif k=='dec': d += f'  {n} [shape=hexagon, style=filled, fillcolor="#FFF2B3", label="{lab}", margin="0.1,0.05"];\n'
            elif k=='mrg': d += f'  {n} [shape=diamond, style=filled, fillcolor="white", label="", width=0.3, height=0.3];\n'
            elif k=='start': d += f'  {n} [shape=circle, style=filled, fillcolor=black, label="", width=0.25];\n'
            elif k=='end': d += f'  {n} [shape=doublecircle, style=filled, fillcolor=black, label="", width=0.2];\n'
            elif k=='conn': d += f'  {n} [shape=circle, style=filled, fillcolor=white, label="{lab}", width=0.35, fontsize=12];\n'
        d += ' }\n'
    for a,b,l,*o in edges:
        extra = (', constraint=false' if o and o[0]=='back' else '')
        d += f'  {a} -> {b} [{"xlabel=" + chr(34) + l + chr(34) if l else ""}{extra}];\n'
    d += '}\n'
    return render(d,name,dpi=dpi)
U,S='u','s'
L=[(U,'Nhân viên kho'),(S,'Hệ thống')]
# --- NPT phần 1: chọn NCC -> tạo hóa đơn
N={'s':(U,'start',''),'a1':(U,'act','Click "Nhập phụ tùng"'),'b1':(S,'act','Hiển thị giao diện chọn nhà cung cấp\\n(ô tìm kiếm + danh sách NCC hiện có)'),
 'a2':(U,'act','Nhập từ khóa tên NCC, click "Tìm kiếm"'),'b2':(S,'act','Tìm và hiển thị danh sách NCC\\nkhớp từ khóa'),
 'd1':(U,'dec','Có NCC cần chọn trong danh sách?'),'a3':(U,'act','Click "Thêm mới nhà cung cấp"'),'a4':(U,'act','Nhập thông tin NCC, click "Lưu"'),
 'b3':(S,'act','Lưu NCC mới vào CSDL'),'m1':(U,'mrg',''),'a5':(U,'act','Click chọn nhà cung cấp'),'b4':(S,'act','Tạo hóa đơn nhập với NCC đã chọn'),
 'b5':(S,'act','Hiển thị giao diện lập hóa đơn\\n(bảng phụ tùng rỗng)'),'A':(S,'conn','A')}
E=[('s','a1',''),('a1','b1',''),('b1','a2',''),('a2','b2',''),('b2','d1',''),('d1','a3','không'),('a3','a4',''),('a4','b3',''),('b3','m1',''),('d1','m1','có'),('m1','a5',''),('a5','b4',''),('b4','b5',''),('b5','A','')]
build('hd_nhap_A',L,N,E)
# --- NPT phần 2: thêm phụ tùng
N={'A':(U,'conn','A'),'m0':(U,'mrg',''),'a1':(U,'act','Click "Thêm phụ tùng"'),'b1':(S,'act','Hiển thị danh sách phụ tùng trong hệ thống'),
 'd1':(U,'dec','Phụ tùng đã có trong danh mục?'),'a2':(U,'act','Click "Thêm mới phụ tùng"'),'a3':(U,'act','Nhập thông tin phụ tùng, click "Lưu"'),'b2':(S,'act','Lưu phụ tùng mới vào CSDL'),
 'm1':(U,'mrg',''),'a4':(U,'act','Click chọn phụ tùng'),'m2':(U,'mrg',''),'a5':(U,'act','Nhập số lượng, đơn giá, click "Thêm"'),
 'd2':(S,'dec','Số lượng, đơn giá hợp lệ?'),'b3':(S,'act','Báo lỗi, không cho phép "Thêm"'),'b4':(S,'act','Thêm dòng chi tiết vào hóa đơn,\\ncập nhật bảng và tổng tiền'),'m3':(S,'mrg',''),
 'd3':(U,'dec','Chưa thêm được?'),'d4':(U,'dec','Còn phụ tùng cần nhập?'),'B':(U,'conn','B')}
E=[('A','m0',''),('m0','a1',''),('a1','b1',''),('b1','d1',''),('d1','a2','chưa'),('a2','a3',''),('a3','b2',''),('b2','m1',''),('d1','m1','có'),('m1','a4',''),('a4','m2',''),('m2','a5',''),('a5','d2',''),
 ('d2','b3','không'),('d2','b4','có'),('b3','m3',''),('b4','m3',''),('m3','d3',''),('d3','m2','nhập lại','back'),('d3','d4','đã thêm'),('d4','m0','còn','back'),('d4','B','hết')]
build('hd_nhap_B',L,N,E)
# --- NPT phần 3: xác nhận
N={'B':(U,'conn','B'),'a1':(U,'act','Click "Xác nhận hóa đơn"'),'b1':(S,'act','Lưu hóa đơn và các chi tiết\\n(trong một transaction)'),'d1':(S,'dec','Lưu thành công?'),
 'b2':(S,'act','Rollback, báo lỗi lưu hóa đơn'),'e1':(S,'end',''),'b3':(S,'act','Cộng dồn số lượng tồn kho\\ncác phụ tùng'),'b4':(S,'act','Báo lưu thành công,\\nhiển thị hóa đơn nhập'),
 'a2':(U,'act','In hóa đơn nhập'),'a3':(U,'act','Thanh toán cho nhà cung cấp'),'e2':(U,'end','')}
E=[('B','a1',''),('a1','b1',''),('b1','d1',''),('d1','b2','không'),('b2','e1',''),('d1','b3','có'),('b3','b4',''),('b4','a2',''),('a2','a3',''),('a3','e2','')]
build('hd_nhap_C',L,N,E)
# --- Tìm kiếm
L2=[(U,'Khách hàng'),(S,'Hệ thống')]
N={'s':(U,'start',''),'a1':(U,'act','Chọn menu "Tìm thông tin dịch vụ/phụ tùng"'),'b1':(S,'act','Hiển thị giao diện tìm kiếm\\n(thanh nhập từ khóa)'),'m0':(U,'mrg',''),
 'a2':(U,'act','Nhập từ khóa, click "Tìm kiếm"'),'d1':(S,'dec','Từ khóa rỗng?'),'b2':(S,'act','Cảnh báo "Vui lòng nhập từ khóa\\ndịch vụ/phụ tùng cần tìm"'),
 'b3':(S,'act','Tìm dịch vụ và phụ tùng\\ncó tên chứa từ khóa'),'d2':(S,'dec','Lỗi kết nối CSDL?'),'b4':(S,'act','Hiển thị pop-up "Đã xảy ra lỗi kết nối,\\nvui lòng thử lại sau"'),
 'd3':(S,'dec','Có kết quả?'),'b5':(S,'act','Hiển thị danh sách rỗng +\\n"Không tìm thấy kết quả phù hợp"'),'b6':(S,'act','Hiển thị danh sách kết quả\\n(dịch vụ + phụ tùng)'),'m1':(S,'mrg',''),
 'd4':(U,'dec','Chưa có kết quả để xem?'),'a3':(U,'act','Click "chọn" một dịch vụ/phụ tùng'),'b7':(S,'act','Lấy thông tin chi tiết từ CSDL'),
 'b8':(S,'act','Hiển thị chi tiết (mã, tên, loại, đơn giá, mô tả)\\nvà nút "Quay lại", "Đặt lịch hẹn"'),'e':(U,'end','')}
E=[('s','a1',''),('a1','b1',''),('b1','m0',''),('m0','a2',''),('a2','d1',''),('d1','b2','có'),('d1','b3','không'),('b3','d2',''),('d2','b4','có'),('d2','d3','không'),('d3','b5','không'),('d3','b6','có'),
 ('b5','m1',''),('b6','m1',''),('b2','m1',''),('b4','m1',''),('m1','d4',''),('d4','m0','nhập lại','back'),('d4','a3','có kết quả'),('a3','b7',''),('b7','b8',''),('b8','e','')]
build('hd_timkiem',L2,N,E)
print('ok')
