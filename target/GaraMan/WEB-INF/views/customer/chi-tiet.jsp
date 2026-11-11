<%@ include file="/WEB-INF/views/common/header.jspf" %>
<!DOCTYPE html>
<html lang="vi"><head><meta charset="UTF-8"><title>Chi tiết - GaraMan</title>
<link rel="stylesheet" href="${ctx}/css/style.css"></head>
<body>
<%@ include file="/WEB-INF/views/common/topbar.jspf" %>
<div class="container">
<div class="card">
  <h1>Chi tiết <c:out value="${loai}"/></h1>
  <table style="max-width:760px">
    <tbody>
      <tr><td style="width:170px;color:#5b6b7b">Mã</td><td><b><c:out value="${ma}"/></b></td></tr>
      <tr><td style="color:#5b6b7b">Tên</td><td><b><c:out value="${ten}"/></b></td></tr>
      <tr><td style="color:#5b6b7b">Loại</td><td><c:out value="${loai}"/></td></tr>
      <tr><td style="color:#5b6b7b">Đơn giá</td><td><fmt:formatNumber value="${gia}" pattern="#,##0"/> VNĐ</td></tr>
      <c:if test="${not empty tonKho}"><tr><td style="color:#5b6b7b">Số lượng tồn</td><td>${tonKho}</td></tr></c:if>
      <tr><td style="color:#5b6b7b">Mô tả chi tiết</td><td><c:out value="${moTa}"/></td></tr>
    </tbody>
  </table>
  <div class="actions">
    <c:url var="back" value="/search"><c:param name="key" value="${key}"/></c:url>
    <a class="btn sec" href="${back}">Quay lại</a>
    <a class="btn" href="#">Đặt lịch hẹn</a>
  </div>
</div>
</div>
</body></html>
