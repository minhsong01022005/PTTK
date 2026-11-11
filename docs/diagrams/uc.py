# -*- coding: utf-8 -*-
from lib import *
from PIL import Image, ImageDraw
# actor icon (người que, đầu xanh như VP)
def mk_actor():
    im = Image.new('RGBA', (60, 110), (255,255,255,0)); d = ImageDraw.Draw(im)
    d.ellipse((18,4,42,28), fill=BLUE, outline='black', width=2)
    d.line((30,28,30,68), fill='black', width=2); d.line((10,42,50,42), fill='black', width=2)
    d.line((30,68,12,100), fill='black', width=2); d.line((30,68,48,100), fill='black', width=2)
    p = os.path.join(IMG, 'actor.png'); im.save(p); return p
ACT = mk_actor()

def actor(id_, label):
    return f'  {id_} [shape=none, image="{ACT}", label="{label}", labelloc=b, imagescale=false, width=0.7, height=1.3, fontsize=11];\n'
def uc(id_, label, extra=''):
    return f'  {id_} [shape=ellipse, style=filled, fillcolor="{BLUE2}", label="{label}", fontsize=11, margin="0.18,0.08" {extra}];\n'

# ---------------- UC tổng quan ----------------
d = header(rankdir='LR', splines='true', nodesep='0.35', ranksep='1.3')
for i,l in [('Mem','Thành viên\\n(Member)'),('Cus','Khách hàng\\n(Customer)'),('Mgr','Nhân viên quản lí\\n(Manager)'),('Inv','Nhân viên kho\\n(Inventory Staff)'),('Sal','Nhân viên bán hàng\\n(Sales Staff)')]:
    d += actor(i,l)
d += f'  subgraph cluster_sys {{ label="GaraMan - Hệ thống quản lý gara ô tô"; labeljust=l; fontsize=13; style=filled; fillcolor="{BLUE}"; color=black; penwidth=1.5;\n'
for i,l in [('login','Login'),('logout','Logout'),('stat','View Statistics 4'),('msv','Manage Services 4'),('mpt','Manage Parts 4'),
            ('imp','Import Parts 4'),('msp','Manage Suppliers 4'),('rcus','Receive Customer 4'),('rreq','Receive Request 4'),
            ('asg','Assign Technician 4'),('pay','Process Payment 4'),('srch','Search Information 4'),('book','Book Appointment 4')]:
    d += '  ' + uc(i,l)
d += '  }\n'
e = lambda a,b,x='': f'  {a} -> {b} [dir=none{x}];\n'
for u in ['login','logout']: d += e('Mem',u)
d += f'  Cus -> Mem [arrowhead=empty, color=black]; Mgr -> Mem [arrowhead=empty]; Inv -> Mem [arrowhead=empty]; Sal -> Mem [arrowhead=empty];\n'
for u in ['srch','book']: d += e('Cus',u)
for u in ['stat','msv','mpt']: d += e('Mgr',u)
for u in ['imp','msp']: d += e('Inv',u)
for u in ['rcus','rreq','asg','pay']: d += e('Sal',u)
d += '}\n'
render(d,'uc_tongquan')

# ---------------- UC chi tiết: tìm kiếm ----------------
d = header(rankdir='LR', splines='true', nodesep='0.5', ranksep='1.2')
d += actor('Cus','Khách hàng\\n(Customer)')
d += f'  subgraph cluster_sys {{ label="Tìm kiếm thông tin dịch vụ/phụ tùng"; labeljust=l; fontsize=13; style=filled; fillcolor="{BLUE}"; color=black;\n'
d += '  ' + uc('srch','Search Information 4') + '  ' + uc('kw','Enter Keyword 4') + '  ' + uc('det','View Details 4') + '  }\n'
d += '  Cus -> srch [dir=none];\n'
d += '  srch -> kw [style=dashed, arrowhead=open, label="«include»"];\n  srch -> det [style=dashed, arrowhead=open, label="«include»"];\n}\n'
render(d,'uc_timkiem')

# ---------------- UC chi tiết: nhập phụ tùng ----------------
d = header(rankdir='LR', splines='true', nodesep='0.5', ranksep='1.2')
d += actor('Inv','Nhân viên kho\\n(Inventory Staff)')
d += f'  subgraph cluster_sys {{ label="Nhập phụ tùng"; labeljust=l; fontsize=13; style=filled; fillcolor="{BLUE}"; color=black;\n'
d += '  ' + uc('imp','Import Parts 4') + '  ' + uc('sup','Select Supplier 4') + '  ' + uc('prt','Select Part 4') + '  ' + uc('cnf','Confirm Invoice 4') + '  }\n'
d += '  Inv -> imp [dir=none];\n'
for u in ['sup','prt','cnf']: d += f'  imp -> {u} [style=dashed, arrowhead=open, label="«include»"];\n'
d += '}\n'
render(d,'uc_nhapphutung')
print('uc ok')
