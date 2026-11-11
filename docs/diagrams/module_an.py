# -*- coding: utf-8 -*-
from lib import *

# ================= Lớp phân tích - Nhập phụ tùng =================
d = header(rankdir='TB', splines='true', nodesep='0.5', ranksep='0.8')
B = {  # lớp biên
 'GDChinhNVKho': (['-btnNhapPhuTung : Button'], []),
 'GDChonNCC': (['-txtTimNCC : TextField','-tblNCC : Table','-btnThemNCC : Button'], ['+hienThiDSNCC()','+chonNCC()']),
 'GDLapHoaDon': (['-tblChiTiet : Table','-btnThemPhuTung : Button','-btnXacNhan : Button'], ['+hienThiHoaDon()','+xacNhan()']),
 'GDChonPhuTung': (['-txtTimPT : TextField','-tblPhuTung : Table','-txtSoLuong, txtDonGia'], ['+hienThiDSPT()','+chonPhuTung()']),
}
for n,(a,m) in B.items(): d += node(n, cls(n,a,m,stereotype='boundary'))
E_ = {
 'Supplier4': (['-id','-code','-name','-phone','-address'], ['+searchSupplier()']),
 'Part4': (['-id','-code','-name','-unitPrice','-stockQuantity'], ['+searchPart()','+updateStock()']),
 'ImportInvoice4': (['-id','-importDate','-totalAmount'], ['+create()','+addDetail()','+save()']),
 'ImportDetail4': (['-id','-quantity','-unitPrice'], []),
}
for n,(a,m) in E_.items(): d += node(n, cls(n,a,m,stereotype='entity'))
dep = [('GDChinhNVKho','GDChonNCC'),('GDChonNCC','GDLapHoaDon'),('GDLapHoaDon','GDChonPhuTung'),('GDChonPhuTung','GDLapHoaDon'),
       ('GDChonNCC','Supplier4'),('GDLapHoaDon','ImportInvoice4'),('GDChonPhuTung','Part4')]
for a,b in dep: d += f'  {a} -> {b} [style=dashed, arrowhead=open];\n'
d += '  ImportInvoice4 -> ImportDetail4 [arrowhead=diamond, headlabel="", taillabel="1", headlabel="1..*", labeldistance=1.6, fontsize=9, dir=back, arrowtail=diamond, arrowhead=none];\n'
d += '  ImportInvoice4 -> Supplier4 [dir=none, taillabel="n", headlabel="1", labeldistance=1.6, fontsize=9];\n'
d += '  ImportInvoice4 -> Part4 [style=dashed, arrowhead=open, constraint=false];\n'
d += '  ImportDetail4 -> Part4 [dir=none, taillabel="n", headlabel="1", labeldistance=1.6, fontsize=9];\n'
d += '  {rank=same; Supplier4; ImportInvoice4; ImportDetail4; Part4}\n}\n'
render(d,'lop_pt_nhapphutung')

# ================= Lớp phân tích - Tìm kiếm =================
d = header(rankdir='TB', splines='true', nodesep='0.7', ranksep='0.9')
B = {
 'GDChinhKH': (['-btnTimKiem : Button'], []),
 'GDTimKiem': (['-txtTuKhoa : TextField','-btnTimKiem : Button','-tblKetQua : Table'], ['+hienThiKetQua()','+chonXemChiTiet()']),
 'GDChiTiet': (['-lblMa, lblTen, lblLoai','-lblDonGia, lblMoTa','-btnQuayLai : Button'], ['+hienThiChiTiet()']),
}
for n,(a,m) in B.items(): d += node(n, cls(n,a,m,stereotype='boundary'))
E_ = {
 'Service4': (['-id','-code','-name','-price','-description'], ['+searchService()','+getDetail()']),
 'Part4': (['-id','-code','-name','-unitPrice','-stockQuantity'], ['+searchPart()','+getDetail()']),
}
for n,(a,m) in E_.items(): d += node(n, cls(n,a,m,stereotype='entity'))
for a,b in [('GDChinhKH','GDTimKiem'),('GDTimKiem','GDChiTiet'),('GDTimKiem','Service4'),('GDTimKiem','Part4'),('GDChiTiet','Service4'),('GDChiTiet','Part4')]:
    d += f'  {a} -> {b} [style=dashed, arrowhead=open];\n'
d += '  {rank=same; Service4; Part4}\n}\n'
render(d,'lop_pt_timkiem')

# ================= Trạng thái =================
def state_diagram(name, states, trans, init, final_from):
    d = header(rankdir='TB', splines='true', nodesep='0.6', ranksep='0.75')
    d += '  start [shape=circle, style=filled, fillcolor=black, label="", width=0.25];\n  end [shape=doublecircle, style=filled, fillcolor=black, label="", width=0.2];\n'
    for k,v in states.items():
        d += f'  {k} [shape=box, style="rounded,filled", fillcolor="{BLUE}", label="{v}", margin="0.25,0.12"];\n'
    d += f'  start -> {init};\n'
    for a,b,l in trans:
        d += f'  {a} -> {b} [label="{l}", fontsize=10];\n'
    for s,l in final_from: d += f'  {s} -> end [label="{l}"];\n'
    d += '}\n'
    return render(d,name)

state_diagram('trangthai_nhapphutung',
 {'s1':'Hiển thị GDChinhNVKho','s2':'Hiển thị GDChonNCC\\n(danh sách nhà cung cấp)','s3':'Hiển thị GDLapHoaDon\\n(hóa đơn nhập)','s4':'Hiển thị GDChonPhuTung\\n(danh sách phụ tùng)','s5':'Thông báo nhập\\nphụ tùng thành công'},
 [('s1','s2','[click chọn Nhập phụ tùng]'),('s2','s2','[nhập từ khóa, Tìm kiếm] /\\nhiển thị NCC khớp'),('s2','s3','[click chọn 1 NCC] /\\nkhởi tạo hóa đơn'),
  ('s3','s4','[click Thêm phụ tùng]'),('s4','s3','[chọn phụ tùng, nhập số lượng,\\nđơn giá, Thêm] / thêm chi tiết'),('s3','s5','[click Xác nhận hóa đơn] /\\nlưu hóa đơn, cộng tồn kho')],
 's1', [('s5','[quay về trang chủ]')])
state_diagram('trangthai_timkiem',
 {'t1':'Hiển thị GDChinhKH','t2':'Hiển thị GDTimKiem\\n(ô nhập từ khóa)','t3':'Hiển thị GDChiTiet\\n(thông tin chi tiết)'},
 [('t1','t2','[click chọn Tìm thông tin\\ndịch vụ/phụ tùng]'),('t2','t2','[nhập từ khóa, Tìm kiếm] /\\nhiển thị danh sách kết quả'),('t2','t3','[click xem 1 dịch vụ/phụ tùng]'),('t3','t2','[click Quay lại]')],
 't1', [('t2','[thoát về trang chủ]')])

# ================= Giao tiếp =================
def comm(name, objs, actor_id, links):
    d = header(rankdir='TB', splines='true', nodesep='1.4', ranksep='1.3')
    d += f'  {actor_id} [shape=none, image="{os.path.join(IMG,"actor.png")}", label="{objs[actor_id]}", labelloc=b, imagescale=false];\n'
    for k,v in objs.items():
        if k==actor_id: continue
        d += f'  {k} [shape=box, style=filled, fillcolor="{BLUE}", label="{v}", margin="0.2,0.12"];\n'
    for a,b,msgs in links:
        rows = ''.join(f'<TR><TD ALIGN="LEFT">{ {"f":"&#8595;","b":"&#8593;","s":"&#10227;"}[m[0]] } {i}: {esc(t)}</TD></TR>' for m,i,t in msgs)
        d += f'  {a} -> {b} [dir=none, label=<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1">{rows}</TABLE>>];\n'
    d += '}\n'
    return render(d, name)

comm('giaotiep_nhapphutung',
 {'A':'Nhân viên kho','g1':'GDChinhNVKho','g2':'GDChonNCC','g3':'GDLapHoaDon','g4':'GDChonPhuTung','sup':'Supplier4','inv':'ImportInvoice4','prt':'Part4'}, 'A',
 [('A','g1',[('f',1,'click chọn Nhập phụ tùng')]),
  ('g1','g2',[('f',2,'gọi GDChonNCC')]),
  ('g2','sup',[('f',3,'yêu cầu tìm danh sách NCC'),('s',4,'tìm các NCC trong hệ thống'),('b',5,'trả kết quả')]),
  ('A','g2',[('b',6,'hiển thị danh sách NCC'),('f',7,'click chọn 1 NCC')]),
  ('g2','g3',[('f',8,'gọi GDLapHoaDon')]),
  ('g3','inv',[('f',9,'yêu cầu khởi tạo hóa đơn'),('s',10,'tạo hóa đơn với NCC đã chọn'),('b',11,'trả kết quả'),('f',21,'yêu cầu thêm chi tiết phụ tùng'),('s',22,'lưu chi tiết vào danh sách'),('b',23,'trả kết quả'),('f',26,'yêu cầu lưu hóa đơn'),('s',27,'lưu thông tin hóa đơn'),('b',31,'trả kết quả')]),
  ('A','g3',[('b',12,'hiển thị hóa đơn'),('f',13,'chọn thêm phụ tùng'),('b',24,'hiển thị hóa đơn (lặp 13–24)'),('f',25,'click xác nhận hóa đơn'),('b',32,'báo nhập phụ tùng thành công')]),
  ('g3','g4',[('f',14,'gọi GDChonPhuTung'),('b',20,'gọi lại GDLapHoaDon')]),
  ('g4','prt',[('f',15,'yêu cầu tìm danh sách phụ tùng'),('s',16,'tìm các phụ tùng trong kho'),('b',17,'trả kết quả')]),
  ('A','g4',[('b',18,'hiển thị danh sách phụ tùng'),('f',19,'chọn phụ tùng, nhập số lượng, đơn giá')]),
  ('inv','prt',[('f',28,'yêu cầu cập nhật tồn kho'),('s',29,'cộng dồn số lượng tồn'),('b',30,'trả kết quả')])])

comm('giaotiep_timkiem',
 {'A':'Khách hàng','g1':'GDChinhKH','g2':'GDTimKiem','g3':'GDChiTiet','sv':'Service4','pt':'Part4'}, 'A',
 [('A','g1',[('f',1,'click chọn Tìm kiếm thông tin dịch vụ')]),
  ('g1','g2',[('f',2,'gọi GDTimKiem')]),
  ('A','g2',[('b',3,'hiển thị giao diện nhập từ khóa'),('f',4,'nhập từ khóa, click tìm kiếm'),('b',11,'hiển thị danh sách kết quả'),('f',12,'click xem 1 dịch vụ')]),
  ('g2','sv',[('f',5,'yêu cầu tìm dịch vụ khớp từ khóa'),('s',6,'tìm các dịch vụ khớp'),('b',7,'trả kết quả')]),
  ('g2','pt',[('f',8,'yêu cầu tìm phụ tùng khớp từ khóa'),('s',9,'tìm các phụ tùng khớp'),('b',10,'trả kết quả')]),
  ('g2','g3',[('f',13,'gọi GDChiTiet')]),
  ('g3','sv',[('f',14,'yêu cầu lấy chi tiết dịch vụ'),('s',15,'lấy thông tin chi tiết'),('b',16,'trả kết quả')]),
  ('A','g3',[('b',17,'hiển thị thông tin chi tiết')])])
print('ok')
