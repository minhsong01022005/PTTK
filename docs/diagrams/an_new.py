# -*- coding: utf-8 -*-
from lib import *
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
# ---- icon biên / thực thể
def icon(name, kind):
    fig, ax = plt.subplots(figsize=(0.6,0.5), dpi=200); ax.set_xlim(0,1.2); ax.set_ylim(0,1); ax.axis('off')
    if kind=='b':
        ax.plot([0.05,0.05],[0.25,0.75],'k',lw=1.2); ax.plot([0.05,0.3],[0.5,0.5],'k',lw=1.2); ax.plot([0.3,0.3],[0.3,0.7],'k',lw=1.2)
        ax.add_patch(Circle((0.7,0.5),0.3,fc=BLUE,ec='k',lw=1.2))
    else:
        ax.add_patch(Circle((0.6,0.55),0.3,fc=BLUE,ec='k',lw=1.2)); ax.plot([0.3,0.9],[0.1,0.1],'k',lw=1.2)
    fig.savefig(os.path.join(IMG,name),transparent=True,bbox_inches='tight',pad_inches=0.02); plt.close(fig)
icon('ic_b.png','b'); icon('ic_e.png','e')

# ---- lớp phân tích (chỉ thuộc tính, không phương thức)
def box(n, attrs, fill=BLUE, abstract=False):
    return node(n, cls(n, attrs, None, fill=fill, abstract=abstract))
def mult(a,b,m1,m2,extra=''):
    return f'  {a} -> {b} [dir=none, taillabel="{m1}", headlabel="{m2}", labeldistance=1.8, fontsize=9{extra}];\n'
def comp(whole,part,m1='1',m2='*'):
    return f'  {whole} -> {part} [arrowtail=diamond, dir=back, arrowhead=none, taillabel="{m1}", headlabel="{m2}", labeldistance=1.8, fontsize=9];\n'.replace('dir=back, arrowhead=none','dir=back')
def gen(a,b): return f'  {b} -> {a} [arrowhead=empty];\n'

d = header(rankdir='TB', splines='true', nodesep='0.5', ranksep='0.5')
d += box('InventoryStaff4',['-warehouseId : String'])+box('Supplier4',['-supplierId : String','-name : String','-phone : String'])
d += box('ImportInvoice4',['-invoiceId : String','-importDate : Date','-totalAmount : Float','-status : String'])
d += box('ImportDetail4',['-quantity : Integer','-importPrice : Float'])+box('Part4',['-partId : String','-partName : String','-stockQuantity : Integer'])
d += '  InventoryStaff4 -> ImportInvoice4 [arrowhead=vee, taillabel="1", headlabel="*", labeldistance=1.8, fontsize=9];\n  Supplier4 -> ImportInvoice4 [arrowhead=vee, taillabel="1", headlabel="*", labeldistance=1.8, fontsize=9];\n'
d += '  ImportInvoice4 -> ImportDetail4 [arrowtail=diamond, dir=back, taillabel="1", headlabel="*", labeldistance=1.8, fontsize=9];\n  ImportDetail4 -> Part4 [arrowhead=vee, taillabel="*", headlabel="1", labeldistance=1.8, fontsize=9];\n}\n'
render(d,'lop_pt_nhapphutung')
d = header(rankdir='TB', splines='true', nodesep='0.8', ranksep='0.7')
d += box('Customer4',['-customerLevel : String'])+box('Service4',['-serviceId : String','-serviceName : String','-price : Float','-description : String'])+box('Part4',['-partId : String','-partName : String','-unitPrice : Float','-description : String'])
for t in ('Service4','Part4'): d += f'  Customer4 -> {t} [arrowhead=vee, taillabel="1", headlabel="*", labeldistance=1.8, fontsize=9];\n'
d += '}\n'; render(d,'lop_pt_timkiem')

# ---- thực thể toàn hệ thống (theo hình phân tích gốc)
d = header(rankdir='BT', splines='true', nodesep='0.45', ranksep='0.7')
E = {'Member4':(['-username : String','-password : String','-phone : String'],True),'FullName4':(['-firstName : String','-lastName : String'],False),
 'Address4':(['-street : String','-city : String'],False),'Customer4':(['-customerLevel : String'],False),'Staff4':(['-hireDate : Date'],True),
 'SalesStaff4':(['-counterId : String'],False),'Manager4':(['-role : String'],False),'InventoryStaff4':(['-warehouseId : String'],False),'Technician4':(['-specialty : String'],False),
 'Supplier4':(['-supplierId : String','-taxCode : String','-email : String','-phone : String'],False),
 'Appointment4':(['-appointmentId : String','-bookDate : Date','-bookTime : Time','-status : String'],False),
 'SalesInvoice4':(['-invoiceId : String','-createDate : Date','-totalAmount : Float','-paymentStatus : String'],False),
 'SalesDetailService4':(['-actualPrice : Float'],False),'SalesDetailPart4':(['-quantity : Integer','-actualPrice : Float'],False),
 'ImportInvoice4':(['-invoiceId : String','-importDate : Date','-totalAmount : Float'],False),'ImportDetail4':(['-quantity : Integer','-importPrice : Float'],False),
 'Service4':(['-serviceId : String','-serviceName : String','-price : Float'],False),'Part4':(['-partId : String','-partName : String','-stockQuantity : Integer','-unitPrice : Float'],False),
 'StatCustomer4':(['-totalSpent : Float','-visitCount : Integer'],False),'StatSupplier4':(['-totalImportValue : Float','-importQuantity : Integer'],False),
 'StatService4':(['-totalRevenue : Float','-usageCount : Integer'],False),'StatPart4':(['-totalRevenue : Float','-soldQuantity : Integer'],False)}
for n,(a,ab) in E.items(): d += box(n,a,abstract=ab)
for a,b in [('Customer4','Member4'),('Staff4','Member4'),('SalesStaff4','Staff4'),('Manager4','Staff4'),('InventoryStaff4','Staff4'),('Technician4','Staff4'),
            ('StatCustomer4','Customer4'),('StatSupplier4','Supplier4'),('StatService4','Service4'),('StatPart4','Part4')]: d += gen(b,a)
for w,p in [('Member4','FullName4'),('Member4','Address4'),('Supplier4','Address4')]:
    d += f'  {w} -> {p} [arrowtail=diamond, dir=back];\n'
for w,p in [('SalesInvoice4','SalesDetailService4'),('SalesInvoice4','SalesDetailPart4'),('ImportInvoice4','ImportDetail4')]:
    d += f'  {w} -> {p} [arrowtail=diamond, dir=back, taillabel="1", headlabel="*", labeldistance=1.7, fontsize=9];\n'
for a,b,m1,m2 in [('Customer4','Appointment4','1','*'),('Customer4','SalesInvoice4','1','*'),('SalesStaff4','SalesInvoice4','1','*'),('Technician4','SalesDetailService4','1','*'),
   ('Supplier4','ImportInvoice4','1','*'),('InventoryStaff4','ImportInvoice4','1','*'),('Service4','SalesDetailService4','1','*'),('Part4','SalesDetailPart4','1','*'),('Part4','ImportDetail4','1','*')]:
    d += mult(a,b,m1,m2)
d += '}\n'; render(d,'lop_thucthe_phantich')

# ---- trạng thái
def state(name, states, trans, final):
    d = header(rankdir='TB', splines='true', nodesep='0.7', ranksep='0.7')
    d += '  start [shape=circle, style=filled, fillcolor=black, label="", width=0.25];\n  end [shape=doublecircle, style=filled, fillcolor=black, label="", width=0.2];\n'
    for k,v in states.items(): d += f'  {k} [shape=box, style="rounded,filled", fillcolor="{BLUE}", label="{v}", margin="0.3,0.15"];\n'
    for a,b,l in trans: d += f'  {a} -> {b} [label="  {l}  "];\n'
    for s,l in final: d += f'  {s} -> end [label="  {l}  "];\n'
    return render(d+'}\n',name)
state('trangthai_nhapphutung',{'s1':'Hiển thị GD chính NV kho','s2':'Hiển thị GD chọn nhà cung cấp','s3':'Hiển thị GD lập hóa đơn nhập','s4':'Hiển thị GD chọn phụ tùng','s5':'Hiển thị GD nhập SL, đơn giá'},
 [('start','s1','Bắt đầu'),('s1','s2','[chọn chức năng nhập phụ tùng]'),('s2','s3','[chọn 1 nhà cung cấp]'),('s3','s4','[chọn thêm phụ tùng]'),('s4','s5','[chọn 1 phụ tùng]'),('s5','s3','[chọn thêm vào hóa đơn]')],[('s3','[chọn xác nhận hóa đơn]\\nKết thúc')])
state('trangthai_timkiem',{'t1':'Hiển thị GD chính KH','t2':'Hiển thị GD tìm kiếm','t3':'Hiển thị GD chi tiết'},
 [('start','t1','Bắt đầu'),('t1','t2','[chọn chức năng tìm kiếm]'),('t2','t2','[nhập từ khóa, click tìm kiếm]'),('t2','t3','[click 1 dịch vụ/phụ tùng]'),('t3','t2','[chọn quay lại]')],[('t2','[chọn thoát]\\nKết thúc'),('t3','[chọn thoát]\\nKết thúc')])

# ---- giao tiếp (icon actor/biên/thực thể)
def comm(name, nodes, edges, pos=None, rankdir='LR'):
    d = header(rankdir=rankdir, splines='true', nodesep='0.3', ranksep='0.9')
    d = d.replace('fontsize=11]','fontsize=16]',1)
    for k,(kind,lbl) in nodes.items():
        im = {'a':'actor.png','b':'ic_b.png','e':'ic_e.png'}[kind]
        d += f'  {k} [shape=none, image="{os.path.join(IMG,im)}", label="{lbl}", labelloc=b, imagescale=false];\n'
    for a,b,l in edges:
        d += f'  {a} -> {b} [label="{l}", fontsize=15];\n'
    return render(d+'}\n',name,dpi=110)
comm('giaotiep_nhapphutung',{'A':('a','Nhân viên kho'),'g1':('b','GDChinhNVKho'),'g2':('b','GDChonNCC'),'g3':('b','GDLapHoaDon'),'g4':('b','GDChonPhuTung'),'sup':('e','Supplier4'),'inv':('e','ImportInvoice4'),'prt':('e','Part4')},
 [('A','g1','1: chọn nhập phụ tùng'),('g1','g2','2: gọi'),('g2','sup','3: gọi'),('sup','sup','4: getDanhSachNCC()'),('sup','g2','5: trả về'),('g2','A','6: hiển thị'),('A','g2','7: chọn 1 NCC'),
  ('g2','g3','8: gọi'),('g3','inv','9: gọi'),('inv','inv','10: createInvoice(ncc)'),('inv','g3','11: trả về'),('g3','A','12: hiển thị'),('A','g3','13: chọn thêm phụ tùng'),('g3','g4','14: gọi'),
  ('g4','prt','15: gọi'),('prt','prt','16: getDanhSachPhuTung()'),('prt','g4','17: trả về'),('g4','A','18: hiển thị'),('A','g4','19: chọn 1 phụ tùng, nhập SL'),('g4','g3','20: gọi'),
  ('g3','inv','21: gọi'),('inv','inv','22: addDetail(pt, sl)'),('inv','g3','23: trả về'),('g3','A','24: hiển thị'),('A','g3','25: chọn xác nhận'),('g3','inv','26: gọi'),('inv','inv','27: saveInvoice()'),
  ('inv','prt','28: gọi'),('prt','prt','29: updateStock()'),('prt','inv','30: trả về'),('inv','g3','31: trả về'),('g3','A','32: báo thành công')], {'A':(60,330),'g1':(330,260),'g2':(610,190),'sup':(845,150),'g3':(860,400),'inv':(1105,480),'prt':(1290,430),'g4':(1450,250)})
comm('giaotiep_timkiem',{'A':('a','Khách hàng'),'g1':('b','GDChinhKH'),'g2':('b','GDTimKiem'),'g3':('b','GDChiTiet'),'sv':('e','Service4'),'pt':('e','Part4')},
 [('A','g1','1: chọn tìm kiếm'),('g1','g2','2: gọi'),('g2','A','3: hiển thị'),('A','g2','4: nhập từ khóa, click tìm kiếm'),('g2','sv','5: gọi'),('sv','sv','6: searchService(keyword)'),('sv','g2','7: trả về'),
  ('g2','pt','8: gọi'),('pt','pt','9: searchPart(keyword)'),('pt','g2','10: trả về'),('g2','A','11: hiển thị danh sách'),('A','g2','12: click 1 dịch vụ'),('g2','g3','13: gọi'),
  ('g3','sv','14: gọi'),('sv','sv','15: getServiceDetail()'),('sv','g3','16: trả về'),('g3','A','17: hiển thị chi tiết')], {'A':(60,300),'g1':(360,250),'g2':(700,190),'pt':(980,160),'sv':(1160,330),'g3':(900,430)})
print('ok')
