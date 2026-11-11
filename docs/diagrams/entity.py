# -*- coding: utf-8 -*-
from lib import *

def A(typed, items):
    return [(f'-{n} : {t}' if typed else f'-{n}') for n,t in items]

def entity(name, typed):
    C = {}
    C['Member4'] = (A(typed,[('id','int'),('username','String'),('password','String'),('fullName','FullName4'),('address','Address4'),('phone','String'),('email','String')]), True)
    C['FullName4'] = (A(typed,[('firstName','String'),('lastName','String')]), False)
    C['Address4'] = (A(typed,[('street','String'),('city','String')]), False)
    C['Customer4'] = ([], False)
    C['Staff4'] = (A(typed,[('startDate','Date'),('position','String')]), True)
    for n in ['Manager4','SalesStaff4','InventoryStaff4','Technician4']: C[n] = ([], False)
    C['Car4'] = (A(typed,[('id','int'),('plate','String'),('brand','String'),('model','String')]), False)
    C['Supplier4'] = (A(typed,[('id','int'),('code','String'),('name','String'),('taxCode','String'),('phone','String'),('email','String'),('address','Address4')]), False)
    C['Service4'] = (A(typed,[('id','int'),('code','String'),('name','String'),('price','long'),('description','String')]), False)
    C['Part4'] = (A(typed,[('id','int'),('code','String'),('name','String'),('unitPrice','long'),('stockQuantity','int'),('description','String')]), False)
    C['Appointment4'] = (A(typed,[('id','int'),('appointmentTime','Date'),('content','String'),('status','String')]), False)
    C['ImportInvoice4'] = (A(typed,[('id','int'),('importDate','Date'),('totalAmount','long')]), False)
    C['ImportDetail4'] = (A(typed,[('id','int'),('quantity','int'),('unitPrice','long')]), False)
    C['SalesInvoice4'] = (A(typed,[('id','int'),('invoiceDate','Date'),('totalAmount','long'),('paymentStatus','String')]), False)
    C['SalesDetailService4'] = (A(typed,[('id','int'),('price','long')]), False)
    C['SalesDetailPart4'] = (A(typed,[('id','int'),('quantity','int'),('unitPrice','long')]), False)
    C['StatService4'] = (A(typed,[('usageCount','int'),('revenue','long')]), False)
    C['StatPart4'] = (A(typed,[('importedQty','int'),('soldQty','int')]), False)
    C['StatCustomer4'] = (A(typed,[('invoiceCount','int'),('revenue','long')]), False)
    C['StatSupplier4'] = (A(typed,[('importedQty','int'),('importedAmount','long')]), False)

    d = header(rankdir='BT', splines='true', nodesep='0.45', ranksep='0.9')
    for n,(at,ab) in C.items():
        d += node(n, cls(n, at, None, abstract=ab))
    inh = [('Customer4','Member4'),('Staff4','Member4'),('Manager4','Staff4'),('SalesStaff4','Staff4'),('InventoryStaff4','Staff4'),('Technician4','Staff4'),
           ('StatService4','Service4'),('StatPart4','Part4'),('StatCustomer4','Customer4'),('StatSupplier4','Supplier4')]
    for a,b in inh: d += f'  {a} -> {b} [arrowhead=empty, color=black];\n'
    comp = [('Member4','FullName4'),('Member4','Address4'),('Supplier4','Address4'),('ImportInvoice4','ImportDetail4'),('SalesInvoice4','SalesDetailService4'),('SalesInvoice4','SalesDetailPart4')]
    for a,b in comp: d += f'  {b} -> {a} [arrowhead=diamond, dir=forward, headlabel="1", taillabel="{"1..*" if "Detail" in b else "1"}", labeldistance=1.6, fontsize=9];\n'
    assoc = [('Customer4','Car4','1','n'),('Customer4','Appointment4','1','n'),('Customer4','SalesInvoice4','1','n'),('Car4','SalesInvoice4','1','n'),
             ('SalesStaff4','SalesInvoice4','1','n'),('Supplier4','ImportInvoice4','1','n'),('InventoryStaff4','ImportInvoice4','1','n'),
             ('Technician4','SalesDetailService4','1','n'),('Part4','ImportDetail4','1','n'),('Part4','SalesDetailPart4','1','n'),
             ('Service4','SalesDetailService4','1','n'),('Service4','Appointment4','0..1','n')]
    for a,b,m1,m2 in assoc: d += f'  {a} -> {b} [dir=none, taillabel="{m1}", headlabel="{m2}", labeldistance=1.7, fontsize=9];\n'
    d += '}\n'
    return render(d, name)

entity('lop_thucthe_phantich', False)
entity('lop_thucthe_thietke', True)
print('ok')
