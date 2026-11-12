<%@ include file="/WEB-INF/views/common/header.jspf" %>
<!DOCTYPE html>
<html lang="vi"><head><meta charset="UTF-8"><title>Chọn nhà cung cấp - GaraMan</title>
<link rel="stylesheet" href="${ctx}/css/style.css"></head>
<body>
<%@ include file="/WEB-INF/views/common/topbar.jspf" %>
<div class="container">
<div class="card">
  <h1>Chọn nhà cung cấp</h1>
  <p class="sub">Tìm nhà cung cấp theo tên hoặc mã, sau đó bấm &quot;Chọn&quot;.</p>
  <form class="inline" method="get" action="${ctx}/import/suppliers">
    <input type="text" name="key" value="<c:out value='${key}'/>" placeholder="Nhập tên hoặc mã nhà cung cấp...">
    <button class="btn" type="submit">Tìm kiếm</button>
    <a class="btn sec" href="${ctx}/import/supplier/new">+ Thêm mới nhà cung cấp</a>
  </form>
  <c:if test="${not empty thongBao}"><div class="alert info"><c:out value="${thongBao}"/></div></c:if>
  <table>
    <thead><tr><th>TT</th><th>Mã NCC</th><th>Tên nhà cung cấp</th><th>Số điện thoại</th><th>Chọn</th></tr></thead>
    <tbody>
    <c:forEach var="s" items="${listSupplier}" varStatus="st">
      <tr><td>${st.count}</td><td><c:out value="${s.code}"/></td><td><c:out value="${s.name}"/></td><td><c:out value="${s.phone}"/></td>
          <td><a class="btn sm" href="${ctx}/import/invoice/new?supplierId=${s.id}">Chọn</a></td></tr>
    </c:forEach>
    </tbody>
  </table>
  <div class="actions"><a class="btn sec" href="${ctx}/home">Quay lại</a></div>
</div>
</div>
</body></html>
