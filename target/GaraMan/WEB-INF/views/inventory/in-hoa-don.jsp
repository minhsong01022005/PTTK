<%@ include file="/WEB-INF/views/common/header.jspf" %>
<!DOCTYPE html>
<html lang="vi"><head><meta charset="UTF-8"><title>In hóa đơn nhập - GaraMan</title>
<link rel="stylesheet" href="${ctx}/css/style.css"></head>
<body>
<%@ include file="/WEB-INF/views/common/topbar.jspf" %>
<div class="container">
<div class="card">
  <div class="alert okm">Lưu hóa đơn thành công, số lượng tồn kho đã được cộng dồn.</div>
  <div class="print-area">
    <h1>HÓA ĐƠN NHẬP PHỤ TÙNG số ${hoaDon.id}</h1>
    <div class="info-box">
      <span class="k">Nhà cung cấp</span><b><c:out value="${hoaDon.supplier.name}"/></b>
      <span class="k">Điện thoại</span><span><c:out value="${hoaDon.supplier.phone}"/></span>
      <span class="k">Nhân viên kho</span><span><c:out value="${hoaDon.inventoryStaff.fullName}"/></span>
      <span class="k">Ngày nhập</span><span><fmt:formatDate value="${hoaDon.importDate}" pattern="dd/MM/yyyy HH:mm"/></span>
    </div>
    <table>
      <thead><tr><th>TT</th><th>Mã PT</th><th>Tên phụ tùng</th><th class="num">Số lượng</th><th class="num">Đơn giá</th><th class="num">Thành tiền</th></tr></thead>
      <tbody>
      <c:forEach var="d" items="${hoaDon.listDetail}" varStatus="st">
        <tr><td>${st.count}</td><td><c:out value="${d.part.code}"/></td><td><c:out value="${d.part.name}"/></td><td class="num">${d.quantity}</td>
            <td class="num"><fmt:formatNumber value="${d.unitPrice}" pattern="#,##0"/></td><td class="num"><fmt:formatNumber value="${d.amount}" pattern="#,##0"/></td></tr>
      </c:forEach>
      </tbody>
      <tfoot><tr><td colspan="5" class="num">Tổng tiền thanh toán cho nhà cung cấp</td><td class="num"><fmt:formatNumber value="${hoaDon.totalAmount}" pattern="#,##0"/> VNĐ</td></tr></tfoot>
    </table>
  </div>
  <div class="actions"><button class="btn" type="button" onclick="window.print()">In hóa đơn</button><a class="btn sec" href="${ctx}/home">Về trang chủ</a></div>
</div>
</div>
</body></html>
