<%@ include file="/WEB-INF/views/common/header.jspf" %>
<!DOCTYPE html>
<html lang="vi"><head><meta charset="UTF-8"><title>Thêm mới phụ tùng - GaraMan</title>
<link rel="stylesheet" href="${ctx}/css/style.css"></head>
<body>
<%@ include file="/WEB-INF/views/common/topbar.jspf" %>
<div class="container">
<div class="card">
  <h1>Thêm mới phụ tùng</h1>
  <p class="sub">Phụ tùng mới được khai báo với số lượng tồn kho ban đầu bằng 0.</p>
  <c:if test="${not empty loi}"><div class="alert err"><c:out value="${loi}"/></div></c:if>
  <form method="post" action="${ctx}/import/part/insert">
    <div class="form-grid">
      <label>Mã phụ tùng <span class="req">*</span></label><input type="text" name="code" value="<c:out value="${pt.code}"/>">
      <label>Tên phụ tùng <span class="req">*</span></label><input type="text" name="name" value="<c:out value="${pt.name}"/>">
      <label>Đơn giá tham khảo (VNĐ) <span class="req">*</span></label><input type="text" name="unitPrice" value="<c:out value="${giaNhap}"/>">
      <label>Mô tả</label><textarea name="description" rows="3"><c:out value="${pt.description}"/></textarea>
    </div>
    <div class="actions"><button class="btn ok" type="submit">Lưu</button><a class="btn sec" href="${ctx}/import/parts">Hủy</a></div>
  </form>
</div>
</div>
</body></html>
