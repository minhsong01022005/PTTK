<%@ include file="/WEB-INF/views/common/header.jspf" %>
<!DOCTYPE html>
<html lang="vi"><head><meta charset="UTF-8"><title>Nhập số lượng, đơn giá - GaraMan</title>
<link rel="stylesheet" href="${ctx}/css/style.css"></head>
<body>
<%@ include file="/WEB-INF/views/common/topbar.jspf" %>
<div class="container">
<div class="card">
  <h1>Nhập số lượng và đơn giá</h1>
  <c:if test="${not empty loi}"><div class="alert err"><c:out value="${loi}"/></div></c:if>
  <div class="info-box">
    <span class="k">Phụ tùng</span><b><c:out value="${pt.code}"/> - <c:out value="${pt.name}"/></b>
    <span class="k">Tồn kho hiện tại</span><span>${pt.stockQuantity}</span>
    <span class="k">Đơn giá tham khảo</span><span><fmt:formatNumber value="${pt.unitPrice}" pattern="#,##0"/> VNĐ</span>
  </div>
  <c:set var="isEdit" value="${not empty index}"/>
  <form method="post" action="${ctx}/import/detail/${isEdit ? 'update' : 'add'}">
    <input type="hidden" name="partId" value="${pt.id}">
    <c:if test="${isEdit}"><input type="hidden" name="index" value="${index}"></c:if>
    <div class="form-grid">
      <label>Số lượng <span class="req">*</span></label><input type="text" name="quantity" value="<c:out value="${soLuong}"/>">
      <label>Đơn giá (VNĐ) <span class="req">*</span></label><input type="text" name="unitPrice" value="<c:out value="${donGia}"/>">
    </div>
    <div class="actions"><button class="btn" type="submit">${isEdit ? 'Cập nhật' : 'Thêm'}</button>
      <a class="btn sec" href="${ctx}/import/invoice/view">Hủy</a></div>
  </form>
</div>
</div>
</body></html>
