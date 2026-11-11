# -*- coding: utf-8 -*-
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
plt.rcParams['font.family']='DejaVu Sans'
BLUE='#7DCDF5'
def seq(name, parts, msgs, title=None, w=None):
    """parts: [(key,label)], msgs: [(from,to,text,kind)] kind: '' call, 'r' return, 'self'; ('frame',text) ('endframe',)"""
    n=len(parts); X={k:i*2.6+1.3 for i,(k,_) in enumerate(parts)}
    H=len(msgs)*0.62+2.2
    fig,ax=plt.subplots(figsize=(n*2.6+0.4,H)); ax.set_xlim(0,n*2.6+0.2); ax.set_ylim(0,H); ax.axis('off')
    top=H-0.4
    for k,l in parts:
        ax.add_patch(Rectangle((X[k]-1.1,top-0.7),2.2,0.7,fc=BLUE,ec='black',lw=1))
        ax.text(X[k],top-0.35,l,ha='center',va='center',fontsize=8,weight='bold')
        ax.plot([X[k],X[k]],[top-0.7,0.3],ls=(0,(5,4)),color='#444',lw=0.8)
    y=top-1.05; fr=None
    for m in msgs:
        if m[0]=='frame':
            fr=(y+0.25,m[1]); y-=0.45; continue
        if m[0]=='endframe':
            ax.add_patch(Rectangle((0.15,y+0.2),n*2.6-0.1,fr[0]-y-0.2,fc='none',ec='#555',lw=1.1))
            ax.add_patch(Rectangle((0.15,fr[0]-0.3),1.1,0.3,fc='#E6E6E6',ec='#555'))
            ax.text(0.2,fr[0]-0.15,'loop',fontsize=8,va='center',weight='bold')
            ax.text(1.4,fr[0]-0.15,'['+fr[1]+']',fontsize=8,va='center')
            y-=0.3; continue
        a,b,t,kind=m
        if a==b:
            ax.plot([X[a],X[a]+0.5,X[a]+0.5,X[a]],[y+0.12,y+0.12,y-0.12,y-0.12],color='black',lw=1)
            ax.annotate('',xy=(X[a],y-0.12),xytext=(X[a]+0.3,y-0.12),arrowprops=dict(arrowstyle='-|>',color='black',lw=1))
            ax.text(X[a]+0.6,y,t,fontsize=7.5,va='center',ha='left')
        else:
            ls='--' if kind=='r' else '-'
            style='->' if kind=='r' else '-|>'
            ax.annotate('',xy=(X[b],y),xytext=(X[a],y),arrowprops=dict(arrowstyle=style,color='black',lw=1,ls=ls))
            ax.text((X[a]+X[b])/2,y+0.07,t,fontsize=7.5,ha='center',va='bottom',bbox=dict(fc='white',ec='none',pad=0.5))
        y-=0.62
    fig.savefig(f'img/{name}.png',dpi=140,bbox_inches='tight',facecolor='white'); plt.close(fig)

P=[('nv','Nhân viên kho'),('jsp','Giao diện JSP'),('sv','ImportServlet'),('dao','DAO Impl'),('bean','Thực thể')]
# --- Import 1: chọn NCC
seq('tt_nhap_1',P,[
 ('nv','jsp','1. Chọn menu Nhập phụ tùng',''),('jsp','sv','2. GET /import/supplier',''),
 ('sv','jsp','3. Hiển thị form chọn NCC','r'),('nv','jsp','4. Nhập tên NCC, bấm Tìm',''),
 ('jsp','sv','5. GET ?key=...',''),('sv','dao','6. searchSupplier(key)',''),('dao','bean','7. new Supplier4(...)',''),
 ('bean','dao','8. Supplier4','r'),('dao','sv','9. List<Supplier4>','r'),('sv','jsp','10. forward chon-ncc.jsp','' ),
 ('jsp','nv','11. Hiển thị danh sách NCC','r'),('nv','jsp','12. Chọn nhà cung cấp',''),
 ('jsp','sv','13. GET /import/new?supplierId',''),('sv','dao','14. getSupplierById(id)',''),
 ('dao','sv','15. Supplier4','r'),('sv','bean','16. new ImportInvoice4(supplier)',''),
 ('sv','sv','17. lưu hóa đơn tạm vào session',''),('sv','jsp','18. redirect /import/invoice (PRG)',''),
 ('jsp','sv','19. GET /import/invoice',''),('sv','jsp','20. forward lap-hoa-don.jsp',''),('jsp','nv','21. Hiển thị form lập hóa đơn','r')])
# --- Import 2: loop thêm dòng
seq('tt_nhap_2',P,[
 ('frame','còn thêm phụ tùng'),
 ('nv','jsp','22. Bấm Thêm phụ tùng, nhập tên',''),('jsp','sv','23. GET /import/part?key',''),
 ('sv','dao','24. searchPart(key)',''),('dao','sv','25. List<Part4>','r'),('sv','jsp','26. forward chon-phu-tung.jsp',''),
 ('jsp','nv','27. Hiển thị danh sách phụ tùng','r'),('nv','jsp','28. Chọn phụ tùng',''),
 ('jsp','sv','29. GET /import/detail?partId',''),('sv','dao','30. getPartById(id)',''),('dao','sv','31. Part4','r'),
 ('sv','jsp','32. forward nhap-so-luong.jsp',''),('jsp','nv','33. Hiển thị form SL, đơn giá','r'),
 ('nv','jsp','34. Nhập số lượng, đơn giá, bấm Lưu',''),('jsp','sv','35. POST /import/detail',''),
 ('sv','sv','36. validate(sl, dg)',''),('sv','bean','37. new ImportDetail4(part, sl, dg)',''),
 ('sv','bean','38. hoaDon.addDetail(ct)',''),('bean','bean','39. tính thành tiền, tổng tiền',''),
 ('sv','jsp','40. redirect /import/invoice',''),('jsp','nv','41. Hiển thị hóa đơn cập nhật','r'),('endframe',)])
# --- Import 3: xác nhận
seq('tt_nhap_3',P,[
 ('nv','jsp','42. Bấm Xác nhận hóa đơn',''),('jsp','sv','43. POST /import/confirm',''),
 ('sv','dao','44. addImportInvoice(hoaDon)',''),('dao','dao','45. BEGIN: lưu hóa đơn + chi tiết',''),
 ('dao','dao','46. cập nhật tồn kho, COMMIT',''),('dao','sv','47. true','r'),
 ('sv','jsp','48. redirect /import/invoice/print',''),('jsp','sv','49. GET /import/invoice/print',''),
 ('sv','jsp','50. forward in-hoa-don.jsp',''),('jsp','nv','51. Hiển thị hóa đơn nhập đã lưu','r')])
# --- Search
S=[('kh','Khách hàng'),('jsp','Giao diện JSP'),('sv','SearchServlet'),('dao','DAO Impl'),('bean','Thực thể')]
seq('tt_timkiem',S,[
 ('kh','jsp','1. Chọn menu Tìm thông tin',''),('jsp','sv','2. GET /search',''),('sv','jsp','3. forward tim-kiem.jsp',''),
 ('jsp','kh','4. Hiển thị form tìm kiếm','r'),('kh','jsp','5. Nhập từ khóa, bấm Tìm',''),
 ('jsp','sv','6. GET /search?key=...',''),('sv','dao','7. searchService(key)',''),('dao','bean','8. new Service4(...)',''),
 ('bean','dao','9. Service4','r'),('dao','sv','10. List<Service4>','r'),('sv','dao','11. searchPart(key)',''),
 ('dao','bean','12. new Part4(...)',''),('bean','dao','13. Part4','r'),('dao','sv','14. List<Part4>','r'),
 ('sv','jsp','15. forward tim-kiem.jsp',''),('jsp','kh','16. Hiển thị danh sách kết quả','r'),
 ('kh','jsp','17. Chọn một mục',''),('jsp','sv','18. GET /search/detail?type&id',''),
 ('sv','dao','19. getServiceById / getPartById',''),('dao','sv','20. Service4 / Part4','r'),
 ('sv','jsp','21. forward chi-tiet.jsp',''),('jsp','kh','22. Hiển thị chi tiết','r')])
print('ok')
