# -*- coding: utf-8 -*-
import subprocess
from lib import *
POS = {'Member4':(800,110),'FullName4':(158,340),'Customer4':(420,340),'Staff4':(1060,340),'Address4':(1420,340),'Supplier4':(1700,110),'StatSupplier4':(1900,340),
 'StatCustomer4':(135,560),'Car4':(560,560),'SalesStaff4':(800,560),'Manager4':(1030,560),'InventoryStaff4':(1520,560),'Appointment4':(175,800),'SalesInvoice4':(470,800),
 'ImportInvoice4':(1520,800),'Technician4':(1260,800),'SalesDetailService4':(470,1040),'SalesDetailPart4':(900,1040),'ImportDetail4':(1515,1040),
 'Service4':(420,1290),'Part4':(1135,1290),'StatService4':(420,1520),'StatPart4':(1135,1520)}
K=0.62
def build(name, E, with_car, typed):
    d = f'digraph G {{\n graph [splines=line, bgcolor=white, pad=0.3, fontname="{FONT}"];\n node [fontname="{FONT}", fontsize=11];\n edge [fontname="{FONT}", fontsize=10];\n'
    for n,(a,ab) in E.items():
        x,y = POS[n]; d += f'  {n} [pos="{x*K:.0f},{(1600-y)*K:.0f}", shape=plaintext, margin=0, label={cls(n,a,None,abstract=ab)}];\n'
    lab = 'labeldistance=2.2, fontsize=10'
    for a,b in [('Customer4','Member4'),('Staff4','Member4'),('SalesStaff4','Staff4'),('Manager4','Staff4'),('InventoryStaff4','Staff4'),('Technician4','Staff4'),
                ('StatCustomer4','Customer4'),('StatSupplier4','Supplier4'),('StatService4','Service4'),('StatPart4','Part4')]:
        d += f'  {a} -> {b} [arrowhead=empty];\n'
    for w,p in [('Member4','FullName4'),('Member4','Address4'),('Supplier4','Address4')]:
        d += f'  {w} -> {p} [dir=back, arrowtail=diamond, headlabel="1", {lab}];\n'
    for w,p in [('SalesInvoice4','SalesDetailService4'),('SalesInvoice4','SalesDetailPart4'),('ImportInvoice4','ImportDetail4')]:
        d += f'  {w} -> {p} [dir=back, arrowtail=diamond, taillabel="1", headlabel="*", {lab}];\n'
    assoc = [('Customer4','Appointment4','1','*'),('Customer4','SalesInvoice4','1','*'),('SalesStaff4','SalesInvoice4','1','*'),('Technician4','SalesDetailService4','1','*'),
      ('Supplier4','ImportInvoice4','1','*'),('InventoryStaff4','ImportInvoice4','1','*'),('Service4','SalesDetailService4','1','*'),('Part4','SalesDetailPart4','1','*'),('Part4','ImportDetail4','1','*')]
    if with_car: assoc += [('Customer4','Car4','1','*'),('Car4','SalesInvoice4','1','*'),('Service4','Appointment4','1','0..1')]
    for a,b,m1,m2 in assoc: d += f'  {a} -> {b} [dir=none, taillabel="{m1}", headlabel="{m2}", {lab}];\n'
    d += '}\n'
    p = os.path.join(IMG,name+'.dot'); open(p,'w',encoding='utf8').write(d)
    r = subprocess.run(['neato','-n','-Tpng','-Gdpi=130',p,'-o',os.path.join(IMG,name+'.png')],capture_output=True,text=True)
    if r.returncode: raise RuntimeError(r.stderr[:1500])

def A(items,typed=False): return [(f'-{n} : {t}' if typed else f'-{n}') for n,t in items]
# phân tích
S='String'
EA = {'Member4':([f'-username : {S}',f'-password : {S}',f'-phone : {S}'],True),'FullName4':([f'-firstName : {S}',f'-lastName : {S}'],False),
 'Address4':([f'-street : {S}',f'-city : {S}'],False),'Customer4':(['-customerLevel : String'],False),'Staff4':(['-hireDate : Date'],True),
 'SalesStaff4':(['-counterId : String'],False),'Manager4':(['-role : String'],False),'InventoryStaff4':(['-warehouseId : String'],False),'Technician4':(['-specialty : String'],False),
 'Supplier4':(['-supplierId : String','-taxCode : String','-email : String','-phone : String'],False),
 'Appointment4':(['-appointmentId : String','-bookDate : Date','-bookTime : Time','-status : String'],False),
 'SalesInvoice4':(['-invoiceId : String','-createDate : Date','-totalAmount : Float','-paymentStatus : String'],False),
 'SalesDetailService4':(['-actualPrice : Float'],False),'SalesDetailPart4':(['-quantity : Integer','-actualPrice : Float'],False),
 'ImportInvoice4':(['-invoiceId : String','-importDate : Date','-totalAmount : Float'],False),'ImportDetail4':(['-quantity : Integer','-importPrice : Float'],False),
 'Service4':(['-serviceId : String','-serviceName : String','-price : Float'],False),'Part4':(['-partId : String','-partName : String','-stockQuantity : Integer','-unitPrice : Float'],False),
 'StatCustomer4':(['-totalSpent : Float','-visitCount : Integer'],False),'StatSupplier4':(['-totalImportValue : Float','-importQuantity : Integer'],False),
 'StatService4':(['-totalRevenue : Float','-usageCount : Integer'],False),'StatPart4':(['-totalRevenue : Float','-soldQuantity : Integer'],False)}
build('lop_thucthe_phantich',EA,False,False)
# thiết kế (theo hình thiết kế gốc: có id, kiểu dữ liệu, Car4)
T=True
ED = {'Member4':(A([('id','Integer'),('username','String'),('password','String'),('fullName','FullName4'),('address','Address4'),('phone','String'),('email','String'),('role','String')],T),True),
 'FullName4':(A([('firstName','String'),('lastName','String')],T),False),'Address4':(A([('street','String'),('city','String')],T),False),
 'Customer4':(A([('customerLevel','String')],T),False),'Staff4':(A([('hireDate','Date'),('position','String')],T),True),
 'SalesStaff4':(A([('counterId','String')],T),False),'Manager4':(A([('managementLevel','String')],T),False),'InventoryStaff4':(A([('warehouseId','String')],T),False),'Technician4':(A([('specialty','String')],T),False),
 'Supplier4':(A([('id','Integer'),('code','String'),('name','String'),('taxCode','String'),('phone','String'),('email','String'),('address','Address4')],T),False),
 'Car4':(A([('id','Integer'),('licensePlate','String'),('brand','String'),('model','String')],T),False),
 'Appointment4':(A([('id','Integer'),('bookDate','Date'),('bookTime','Time'),('status','String'),('note','String')],T),False),
 'SalesInvoice4':(A([('id','Integer'),('code','String'),('createDate','Date'),('totalAmount','Float'),('paymentStatus','String')],T),False),
 'SalesDetailService4':(A([('id','Integer'),('actualPrice','Float')],T),False),'SalesDetailPart4':(A([('id','Integer'),('quantity','Integer'),('actualPrice','Float')],T),False),
 'ImportInvoice4':(A([('id','Integer'),('code','String'),('importDate','Date'),('totalAmount','Float'),('status','String')],T),False),
 'ImportDetail4':(A([('id','Integer'),('quantity','Integer'),('importPrice','Float')],T),False),
 'Service4':(A([('id','Integer'),('code','String'),('name','String'),('price','Float'),('description','String')],T),False),
 'Part4':(A([('id','Integer'),('code','String'),('name','String'),('unitPrice','Float'),('stockQuantity','Integer'),('description','String')],T),False),
 'StatCustomer4':(A([('visitCount','Integer'),('totalSpent','Float')],T),False),'StatSupplier4':(A([('importQuantity','Integer'),('totalImportValue','Float')],T),False),
 'StatService4':(A([('usageCount','Integer'),('totalRevenue','Float')],T),False),'StatPart4':(A([('soldQuantity','Integer'),('totalRevenue','Float')],T),False)}
build('lop_thucthe_thietke',ED,True,True)
print('ok')
