<%@ include file="/WEB-INF/views/common/header.jspf" %>
<!DOCTYPE html>
<html lang="vi"><head><meta charset="UTF-8"><title>Lập hóa đơn nhập - GaraMan</title>
<link rel="stylesheet" href="${ctx}/css/style.css"></head>
<body>
<%@ include file="/WEB-INF/views/common/topbar.jspf" %>
<div class="container">
<div class="card">
  <h1>Lập hóa đơn nhập phụ tùng</h1>
  <c:if test="${not empty loi}"><div class="alert err"><c:out value="${loi}"/></div></c:if>
  <div class="info-box">
    <span class="k">Nhà cung cấp</span><b><c:out value="${hoaDon.supplier.name}"/> (<c:out value="${hoaDon.supplier.code}"/>)</b>
    <span class="k">Số điện thoại</span><span><c:out value="${hoaDon.supplier.phone}"/></span>
    <span class="k">Nhân viên kho</span><span><c:out value="${sessionScope.member.fullName}"/></span>
    <span class="k">Ngày nhập</span><span><fmt:formatDate value="${hoaDon.importDate}" pattern="dd/MM/yyyy HH:mm"/></span>
  </div>
  <table>
    <thead><tr><th>TT</th><th>Mã PT</th><th>Tên phụ tùng</th><th class="num">Số lượng</th><th class="num">Đơn giá</th><th class="num">Thành tiền</th><th>Sửa</th><th>Xóa</th></tr></thead>
    <tbody>
    <c:if test="${empty hoaDon.listDetail}"><tr><td colspan="8" style="text-align:center;color:#5b6b7b">Chưa có phụ tùng nào trong hóa đơn</td></tr></c:if>
    <c:forEach var="d" items="${hoaDon.listDetail}" varStatus="st">
      <tr><td>${st.count}</td><td><c:out value="${d.part.code}"/></td><td><c:out value="${d.part.name}"/></td>
          <td class="num">${d.quantity}</td>
          <td class="num"><fmt:formatNumber value="${d.unitPrice}" pattern="#,##0"/></td>
          <td class="num"><fmt:formatNumber value="${d.amount}" pattern="#,##0"/></td>
          <td class="act"><a class="btn sm sec" href="${ctx}/import/detail/form?index=${st.index}">sửa</a></td>
          <td class="act"><form method="post" action="${ctx}/import/detail/remove" style="margin:0">
              <input type="hidden" name="index" value="${st.index}"><button class="btn sm danger" type="submit">xóa</button></form></td></tr>
    </c:forEach>
    </tbody>
    <tfoot><tr><td colspan="5" class="num">Tổng tiền thanh toán</td><td class="num"><fmt:formatNumber value="${hoaDon.totalAmount}" pattern="#,##0"/> VNĐ</td><td colspan="2"></td></tr></tfoot>
  </table>
  <div class="actions">
    <a class="btn" href="${ctx}/import/parts">+ Thêm phụ tùng</a>
    <form method="post" action="${ctx}/import/invoice/confirm" style="margin:0">
      <button class="btn ok<c:if test='${empty hoaDon.listDetail}'> disabled</c:if>" type="submit" <c:if test="${empty hoaDon.listDetail}">disabled</c:if>>Xác nhận hóa đơn</button></form>
    <form method="post" action="${ctx}/import/invoice/cancel" style="margin:0"><button class="btn sec" type="submit">Hủy</button></form>
  </div>
</div>
</div>
</body></html>
