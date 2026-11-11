# -*- coding: utf-8 -*-
from lib import *
# Package
d=header(rankdir='TB',splines='true',nodesep='0.6',ranksep='0.8')
def pk(i,t,items,fill=BLUE):
    rows=''.join(f'<TR><TD ALIGN="LEFT">{esc(x)}</TD></TR>' for x in items)
    return f'  {i} [shape=plaintext, margin=0, label=<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0"><TR><TD ALIGN="LEFT" BORDER="1" BGCOLOR="{fill}" WIDTH="60" HEIGHT="18"><FONT POINT-SIZE="9">&nbsp;</FONT></TD><TD></TD></TR><TR><TD COLSPAN="2" BORDER="1" BGCOLOR="{fill}" CELLPADDING="8"><TABLE BORDER="0" CELLSPACING="0"><TR><TD><B>{esc(t)}</B></TD></TR>{rows}</TABLE></TD></TR></TABLE>>];\n'
d+=pk('view','view (WEB-INF/views)',['common/*.jsp','inventory/*.jsp','customer/*.jsp'])
d+=pk('ctl','gara.controller',['EncodingFilter, AuthFilter','LoginServlet, LogoutServlet, HomeServlet','ImportServlet, SearchServlet'])
d+=pk('dao','gara.dao',['DAO, MemberDAO4, SupplierDAO4','PartDAO4, ServiceDAO4, ImportInvoiceDAO4'])
d+=pk('impl','gara.dao.impl',['*DAOImpl4 (JDBC)'])
d+=pk('model','gara.model',['user, catalog, transaction'])
d+=pk('util','gara.util',['PasswordUtil'])
d+=pk('db','MySQL: GaraManDB',['tblMember, tblSupplier, tblPart,','tblService, tblImportInvoice, tblImportDetail'],ORANGE)
for a,b in [('ctl','view'),('ctl','impl'),('ctl','dao'),('ctl','model'),('impl','dao'),('impl','model'),('ctl','util'),('impl','db'),('dao','model')]:
    d+=f'  {a} -> {b} [style=dashed, arrowhead=open];\n'
d+='}\n'; render(d,'goi',dpi=130)
# Deployment
d=header(rankdir='LR',splines='true',nodesep='0.5',ranksep='1.0')
def nd(i,t,inner,fill='#E8E8E8'):
    return f'  {i} [shape=box3d, style=filled, fillcolor="{fill}", margin="0.25,0.2", label=<<B>{esc(t)}</B><BR/>{inner}>];\n'
def cp(i,t,fill=BLUE): return f'    {i} [shape=component, style=filled, fillcolor="{fill}", label="{t}"];\n'
d+=nd('c1','Máy khách (nhân viên kho)','&laquo;device&raquo;<BR/>Trình duyệt web')
d+=nd('c2','Máy khách (khách hàng)','&laquo;device&raquo;<BR/>Trình duyệt web')
d+='  subgraph cluster_srv { label="Máy chủ ứng dụng — Apache Tomcat 9 (Java 17)"; style=filled; fillcolor="#E8E8E8"; fontname="%s";\n'%FONT
d+=cp('war','GaraMan.war (JSP + Servlet)')+cp('jdbc','MySQL Connector/J')
d+='  }\n'
d+='  subgraph cluster_db { label="Máy chủ CSDL — MySQL 8"; style=filled; fillcolor="#E8E8E8"; fontname="%s";\n'%FONT
d+=cp('sch','Schema GaraManDB',ORANGE)+'  }\n'
d+=nd('pr','Máy in','&laquo;device&raquo;<BR/>In hóa đơn nhập')
d+='  c1 -> war [dir=both, label="HTTP :8080", arrowtail=none];\n  c2 -> war [dir=both, label="HTTP :8080"];\n  war -> jdbc [style=dashed, arrowhead=open];\n  jdbc -> sch [dir=both, label="TCP :3306"];\n  c1 -> pr [label="in từ trình duyệt", style=dashed];\n'
d+='}\n'; render(d,'trienkhai',dpi=130)
print('ok')
