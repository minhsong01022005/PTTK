<%@ include file="/WEB-INF/views/common/header.jspf" %>
<!DOCTYPE html>
<html lang="vi"><head><meta charset="UTF-8"><title>Chọn phụ tùng - GaraMan</title>
<link rel="stylesheet" href="${ctx}/css/style.css"></head>
<body>
<%@ include file="/WEB-INF/views/common/topbar.jspf" %>
<div class="container">
<div class="card">
  <h1>Chọn phụ tùng</h1>
  <p class="sub">Tìm phụ tùng theo tên, bấm &quot;Chọn&quot; để nhập số lượng và đơn giá.</p>
  <form class="inline" method="get" action="${ctx}/import/parts">
    <input type="text" name="key" value="<c:out value='${key}'/>" placeholder="Nhập tên phụ tùng...">
    <button class="btn" type="submit">Tìm kiếm</button>
    <a class="btn sec" href="${ctx}/import/part/new">+ Thêm mới phụ tùng</a>
  </form>
  <c:if test="${not empty thongBao}"><div class="alert info"><c:out value="${thongBao}"/></div></c:if>
  <table>
    <thead><tr><th>TT</th><th>Mã PT</th><th>Tên phụ tùng</th><th class="num">Số lượng tồn</th><th class="num">Đơn giá nhập tham khảo</th><th>Chọn</th></tr></thead>
    <tbody>
    <c:forEach var="p" items="${listPart}" varStatus="st">
      <tr><td>${st.count}</td><td><c:out value="${p.code}"/></td><td><c:out value="${p.name}"/></td>
          <td class="num">${p.stockQuantity}</td><td class="num"><fmt:formatNumber value="${p.unitPrice}" pattern="#,##0"/></td>
          <td><a class="btn sm" href="${ctx}/import/detail/form?partId=${p.id}">Chọn</a></td></tr>
    </c:forEach>
    </tbody>
  </table>
  <div class="actions"><a class="btn sec" href="${ctx}/import/invoice/view">Quay lại hóa đơn</a></div>
</div>
</div>
</body></html>
