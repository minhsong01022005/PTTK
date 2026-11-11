# -*- coding: utf-8 -*-
from lib import *

# ================= ERD =================
T = {
 'tblMember4':[('PK','id','INT'),('','username','VARCHAR(50) U'),('','password','CHAR(64)'),('','firstName','VARCHAR(50)'),('','lastName','VARCHAR(50)'),('','street','VARCHAR(150)'),('','city','VARCHAR(80)'),('','phone','VARCHAR(20)'),('','email','VARCHAR(100)'),('','role','ENUM')],
 'tblCustomer4':[('PK,FK','memberId','INT'),('','customerLevel','VARCHAR(30)')],
 'tblStaff4':[('PK,FK','memberId','INT'),('','hireDate','DATE'),('','position','VARCHAR(50)')],
 'tblManager4':[('PK,FK','staffId','INT'),('','managementLevel','VARCHAR(30)')],
 'tblSalesStaff4':[('PK,FK','staffId','INT'),('','counterId','VARCHAR(20)')],
 'tblInventoryStaff4':[('PK,FK','staffId','INT'),('','warehouseId','VARCHAR(20)')],
 'tblTechnician4':[('PK,FK','staffId','INT'),('','specialty','VARCHAR(50)')],
 'tblCar4':[('PK','id','INT'),('','plate','VARCHAR(20)'),('','brand','VARCHAR(50)'),('','model','VARCHAR(50)'),('FK','customerId','INT')],
 'tblSupplier4':[('PK','id','INT'),('','code','VARCHAR(20) U'),('','name','VARCHAR(150)'),('','taxCode','VARCHAR(20)'),('','phone','VARCHAR(20)'),('','email','VARCHAR(100)'),('','street','VARCHAR(150)'),('','city','VARCHAR(80)')],
 'tblService4':[('PK','id','INT'),('','code','VARCHAR(20) U'),('','name','VARCHAR(150)'),('','price','DECIMAL(15,0)'),('','description','TEXT')],
 'tblPart4':[('PK','id','INT'),('','code','VARCHAR(20) U'),('','name','VARCHAR(150)'),('','unitPrice','DECIMAL(15,0)'),('','stockQuantity','INT'),('','description','TEXT')],
 'tblAppointment4':[('PK','id','INT'),('','appointmentTime','DATETIME'),('','content','VARCHAR(255)'),('','status','VARCHAR(20)'),('FK','customerId','INT'),('FK','serviceId','INT NULL')],
 'tblImportInvoice4':[('PK','id','INT'),('','importDate','DATETIME'),('','totalAmount','DECIMAL(15,0)'),('FK','supplierId','INT'),('FK','inventoryStaffId','INT')],
 'tblImportDetail4':[('PK','id','INT'),('FK','importInvoiceId','INT'),('FK','partId','INT'),('','quantity','INT'),('','unitPrice','DECIMAL(15,0)')],
 'tblSalesInvoice4':[('PK','id','INT'),('','invoiceDate','DATETIME'),('','totalAmount','DECIMAL(15,0)'),('','paymentStatus','VARCHAR(20)'),('FK','customerId','INT'),('FK','salesStaffId','INT'),('FK','carId','INT')],
 'tblSalesDetailService4':[('PK','id','INT'),('FK','salesInvoiceId','INT'),('FK','serviceId','INT'),('FK','technicianId','INT NULL'),('','price','DECIMAL(15,0)')],
 'tblSalesDetailPart4':[('PK','id','INT'),('FK','salesInvoiceId','INT'),('FK','partId','INT'),('','quantity','INT'),('','unitPrice','DECIMAL(15,0)')],
}
def tbl(name, cols):
    rows = f'<TR><TD COLSPAN="3" BGCOLOR="{ORANGE}" SIDES="B"><B>{name}</B></TD></TR>'
    for k,c,t in cols:
        b = '<B>' if 'PK' in k else ''
        e = '</B>' if 'PK' in k else ''
        kk = {'PK':'&#128273;','PK,FK':'&#128273;','FK':'FK'}.get(k,'')
        rows += f'<TR><TD ALIGN="LEFT" BGCOLOR="{ORANGE2}" WIDTH="26"><FONT POINT-SIZE="8">{k or "&nbsp;"}</FONT></TD><TD ALIGN="LEFT" BGCOLOR="{ORANGE2}">{b}{c}{e}</TD><TD ALIGN="LEFT" BGCOLOR="{ORANGE2}"><FONT POINT-SIZE="9">{t}</FONT></TD></TR>'
    return f'<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="3">{rows}</TABLE>>'
d = header(rankdir='BT', splines='true', nodesep='0.4', ranksep='0.9')
for n,c in T.items(): d += node(n, tbl(n,c))
fk = [('tblCustomer4','tblMember4'),('tblStaff4','tblMember4'),('tblManager4','tblStaff4'),('tblSalesStaff4','tblStaff4'),('tblInventoryStaff4','tblStaff4'),('tblTechnician4','tblStaff4'),
      ('tblCar4','tblCustomer4'),('tblAppointment4','tblCustomer4'),('tblAppointment4','tblService4'),('tblImportInvoice4','tblSupplier4'),('tblImportInvoice4','tblInventoryStaff4'),
      ('tblImportDetail4','tblImportInvoice4'),('tblImportDetail4','tblPart4'),('tblSalesInvoice4','tblCustomer4'),('tblSalesInvoice4','tblSalesStaff4'),('tblSalesInvoice4','tblCar4'),
      ('tblSalesDetailService4','tblSalesInvoice4'),('tblSalesDetailService4','tblService4'),('tblSalesDetailService4','tblTechnician4'),('tblSalesDetailPart4','tblSalesInvoice4'),('tblSalesDetailPart4','tblPart4')]
one_to_one = {('tblCustomer4','tblMember4'),('tblStaff4','tblMember4'),('tblManager4','tblStaff4'),('tblSalesStaff4','tblStaff4'),('tblInventoryStaff4','tblStaff4'),('tblTechnician4','tblStaff4')}
for a,b in fk:
    if (a,b) in one_to_one: d += f'  {a} -> {b} [dir=both, arrowhead=teetee, arrowtail=teeodot, color="#444444"];\n'
    else: d += f'  {a} -> {b} [dir=both, arrowhead=teetee, arrowtail=crowodot, color="#444444"];\n'
d += '}\n'
render(d,'erd')

# ================= Lớp chi tiết: Nhập phụ tùng =================
LIGHT = '#CFEFFF'
d = header(rankdir='LR', splines='true', nodesep='0.25', ranksep='1.1')
V = {  # JSP
 'nvkho-home.jsp':(['+menu Nhập phụ tùng'],[]),
 'chon-ncc.jsp':(['-listSupplier : List<Supplier4>','-key : String'],[]),
 'them-ncc.jsp':(['-ncc : Supplier4','-loi : String'],[]),
 'lap-hoa-don.jsp':(['-hoaDon : ImportInvoice4','-loi : String'],[]),
 'chon-phu-tung.jsp':(['-listPart : List<Part4>','-key : String'],[]),
 'them-phu-tung.jsp':(['-pt : Part4','-loi : String'],[]),
 'nhap-so-luong.jsp':(['-pt : Part4','-soLuong, donGia','-loi : String'],[]),
 'in-hoa-don.jsp':(['-hoaDon : ImportInvoice4'],[]),
}
def jid(n): return n.replace('-','_').replace('.','_')
for n,(a,m) in V.items(): d += node(jid(n), cls(n,a,None,stereotype='JSP'))
d += node('ImportServlet', cls('ImportServlet',['-supplierDAO : SupplierDAO4','-partDAO : PartDAO4','-invoiceDAO : ImportInvoiceDAO4'],
  ['#doGet(req, resp)','#doPost(req, resp)','-listSupplier()','-addSupplier()','-newInvoice()','-viewInvoice()','-listPart()','-addPart()','-showDetailForm()','-saveDetail()','-removeDetail()','-confirmInvoice()','-printInvoice()','-cancelInvoice()','~validate(sl, dg) : boolean'], stereotype='Servlet'))
DAOI = {'SupplierDAO4':['+searchSupplier(key) : List<Supplier4>','+getSupplierById(id) : Supplier4','+addSupplier(s) : boolean'],
        'PartDAO4':['+searchPart(key) : List<Part4>','+getPartById(id) : Part4','+addPart(p) : boolean'],
        'ImportInvoiceDAO4':['+addImportInvoice(hd) : boolean']}
for n,m in DAOI.items(): d += node(n, cls(n,[],m,fill=LIGHT,stereotype='interface'))
d += node('DAO', cls('DAO',[],['#getConnection() : Connection']))
for n in ['SupplierDAOImpl4','PartDAOImpl4','ImportInvoiceDAOImpl4']: d += node(n, cls(n,[],[ '+(các phương thức của interface)'] ))
M = {'Supplier4':['-id : int','-code, name : String','-taxCode, phone, email','-address : Address4'],
     'Part4':['-id : int','-code, name : String','-unitPrice : long','-stockQuantity : int'],
     'ImportInvoice4':['-id : int','-importDate : Date','-totalAmount : long','-supplier : Supplier4','-inventoryStaff : InventoryStaff4','-listDetail : List<ImportDetail4>'],
     'ImportDetail4':['-id : int','-part : Part4','-quantity : int','-unitPrice : long']}
MM = {'ImportInvoice4':['+addDetail(ct)','+updateDetail(i, sl, dg)','+removeDetail(i)'],'ImportDetail4':['+getAmount() : long'],'Supplier4':[],'Part4':[]}
for n,a in M.items(): d += node(n, cls(n,a,MM[n],stereotype='JavaBean'))
d += node('InventoryStaff4', cls('InventoryStaff4',['(kế thừa Staff4 → Member4)'],[],stereotype='JavaBean'))
for j in V: d += f'  ImportServlet -> {jid(j)} [style=dashed, arrowhead=open];\n'
for n in DAOI: d += f'  ImportServlet -> {n} [arrowhead=open];\n'
for n,i in [('SupplierDAOImpl4','SupplierDAO4'),('PartDAOImpl4','PartDAO4'),('ImportInvoiceDAOImpl4','ImportInvoiceDAO4')]:
    d += f'  {i} -> {n} [style=dashed, dir=back, arrowtail=empty, arrowhead=none];\n  DAO -> {n} [dir=back, arrowtail=empty, arrowhead=none];\n'
for a,b in [('SupplierDAOImpl4','Supplier4'),('PartDAOImpl4','Part4'),('ImportInvoiceDAOImpl4','ImportInvoice4')]: d += f'  {a} -> {b} [style=dashed, arrowhead=open];\n'
d += '  ImportInvoice4 -> ImportDetail4 [dir=back, arrowtail=diamond, arrowhead=none, taillabel="1", headlabel="1..*", labeldistance=1.5, fontsize=9];\n'
d += '  ImportInvoice4 -> InventoryStaff4 [dir=none, taillabel="n", headlabel="1", labeldistance=1.5, fontsize=9];\n'
d += '  ImportInvoice4 -> Supplier4 [dir=none, taillabel="n", headlabel="1", labeldistance=1.5, fontsize=9];\n'
d += '  ImportDetail4 -> Part4 [dir=none, taillabel="n", headlabel="1", labeldistance=1.5, fontsize=9];\n'
d += '}\n'
render(d,'lop_ct_nhapphutung', dpi=120)

# ================= Lớp chi tiết: Tìm kiếm =================
d = header(rankdir='LR', splines='true', nodesep='0.3', ranksep='1.2')
for n,a in [('customer-home.jsp',['+menu Tìm thông tin']),('tim-kiem.jsp',['-key : String','-listService : List<Service4>','-listPart : List<Part4>','-loi, thongBao : String']),
            ('chi-tiet.jsp',['-loai, ma, ten : String','-gia : long','-moTa : String','-tonKho : int'])]:
    d += node(jid(n), cls(n,a,None,stereotype='JSP'))
d += node('SearchServlet', cls('SearchServlet',['-serviceDAO : ServiceDAO4','-partDAO : PartDAO4'],['#doGet(req, resp)','#doPost(req, resp)','-showSearchForm()','-search()','-showDetail()'],stereotype='Servlet'))
d += node('ServiceDAO4', cls('ServiceDAO4',[],['+searchService(key) : List<Service4>','+getServiceById(id) : Service4'],fill=LIGHT,stereotype='interface'))
d += node('PartDAO4', cls('PartDAO4',[],['+searchPart(key) : List<Part4>','+getPartById(id) : Part4'],fill=LIGHT,stereotype='interface'))
d += node('DAO', cls('DAO',[],['#getConnection() : Connection']))
d += node('ServiceDAOImpl4', cls('ServiceDAOImpl4',[],['+(các phương thức của interface)']))
d += node('PartDAOImpl4', cls('PartDAOImpl4',[],['+(các phương thức của interface)']))
d += node('Service4', cls('Service4',['-id : int','-code, name : String','-price : long','-description : String'],[],stereotype='JavaBean'))
d += node('Part4', cls('Part4',['-id : int','-code, name : String','-unitPrice : long','-stockQuantity : int','-description : String'],[],stereotype='JavaBean'))
for j in ['customer_home_jsp','tim_kiem_jsp','chi_tiet_jsp']: d += f'  SearchServlet -> {j} [style=dashed, arrowhead=open];\n'
d += '  SearchServlet -> ServiceDAO4 [arrowhead=open];\n  SearchServlet -> PartDAO4 [arrowhead=open];\n'
for n,i,m in [('ServiceDAOImpl4','ServiceDAO4','Service4'),('PartDAOImpl4','PartDAO4','Part4')]:
    d += f'  {i} -> {n} [style=dashed, dir=back, arrowtail=empty, arrowhead=none];\n  DAO -> {n} [dir=back, arrowtail=empty, arrowhead=none];\n  {n} -> {m} [style=dashed, arrowhead=open];\n'
d += '}\n'
render(d,'lop_ct_timkiem', dpi=140)
print('ok')
