<%@ include file="/WEB-INF/views/common/header.jspf" %>
<!DOCTYPE html>
<html lang="vi"><head><meta charset="UTF-8"><title>Thêm mới nhà cung cấp - GaraMan</title>
<link rel="stylesheet" href="${ctx}/css/style.css"></head>
<body>
<%@ include file="/WEB-INF/views/common/topbar.jspf" %>
<div class="container">
<div class="card">
  <h1>Thêm mới nhà cung cấp</h1>
  <p class="sub">Các ô có dấu <span class="req">*</span> là bắt buộc.</p>
  <c:if test="${not empty loi}"><div class="alert err"><c:out value="${loi}"/></div></c:if>
  <form method="post" action="${ctx}/import/supplier/insert">
    <div class="form-grid">
      <label>Mã nhà cung cấp <span class="req">*</span></label><input type="text" name="code" value="<c:out value="${ncc.code}"/>">
      <label>Tên nhà cung cấp <span class="req">*</span></label><input type="text" name="name" value="<c:out value="${ncc.name}"/>">
      <label>Mã số thuế</label><input type="text" name="taxCode" value="<c:out value="${ncc.taxCode}"/>">
      <label>Số điện thoại <span class="req">*</span></label><input type="text" name="phone" value="<c:out value="${ncc.phone}"/>">
      <label>Email</label><input type="text" name="email" value="<c:out value="${ncc.email}"/>">
      <label>Địa chỉ (số nhà, đường)</label><input type="text" name="street" value="<c:out value="${ncc.address.street}"/>">
      <label>Tỉnh / thành phố</label><input type="text" name="city" value="<c:out value="${ncc.address.city}"/>">
    </div>
    <div class="actions"><button class="btn ok" type="submit">Lưu</button><a class="btn sec" href="${ctx}/import/suppliers">Hủy</a></div>
  </form>
</div>
</div>
</body></html>
