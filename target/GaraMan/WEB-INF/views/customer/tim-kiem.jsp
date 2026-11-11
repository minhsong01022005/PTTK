<%@ include file="/WEB-INF/views/common/header.jspf" %>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>
<!DOCTYPE html>
<html lang="vi"><head><meta charset="UTF-8"><title>Tìm kiếm thông tin - GaraMan</title>
<link rel="stylesheet" href="${ctx}/css/style.css"></head>
<body>
<%@ include file="/WEB-INF/views/common/topbar.jspf" %>
<div class="container">
<div class="card">
  <h1>Tìm thông tin dịch vụ / phụ tùng</h1>
  <p class="sub">Nhập tên dịch vụ hoặc phụ tùng cần tìm.</p>
  <form class="inline" method="get" action="${ctx}/search">
    <input type="text" name="key" value="<c:out value="${key}"/>" placeholder="Ví dụ: Dầu, Lốp, Rửa xe..." autofocus>
    <button class="btn" type="submit">Tìm kiếm</button>
  </form>
  <c:if test="${not empty loi}"><div class="alert err"><c:out value="${loi}"/></div></c:if>
  <c:if test="${not empty thongBao}"><div class="alert info"><c:out value="${thongBao}"/></div></c:if>
  <c:if test="${daTim}">
  <table>
    <thead><tr><th>TT</th><th>Mã</th><th>Tên dịch vụ / phụ tùng</th><th>Loại</th><th>Xem chi tiết</th></tr></thead>
    <tbody>
      <c:forEach var="s" items="${listService}" varStatus="st">
        <tr><td>${st.count}</td><td><c:out value="${s.code}"/></td><td><c:out value="${s.name}"/></td>
            <td><span class="badge dv">Dịch vụ</span></td>
            <td><c:url var="u" value="/search/detail"><c:param name="type" value="service"/><c:param name="id" value="${s.id}"/><c:param name="key" value="${key}"/></c:url><a class="btn sm" href="${u}">chọn</a></td></tr>
      </c:forEach>
      <c:forEach var="p" items="${listPart}" varStatus="st">
        <tr><td>${fn:length(listService) + st.count}</td><td><c:out value="${p.code}"/></td><td><c:out value="${p.name}"/></td>
            <td><span class="badge pt">Phụ tùng</span></td>
            <td><c:url var="u" value="/search/detail"><c:param name="type" value="part"/><c:param name="id" value="${p.id}"/><c:param name="key" value="${key}"/></c:url><a class="btn sm" href="${u}">chọn</a></td></tr>
      </c:forEach>
    </tbody>
  </table>
  </c:if>
  <div class="actions"><a class="btn sec" href="${ctx}/home">Quay lại trang chủ</a></div>
</div>
</div>
</body></html>
