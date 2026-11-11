<%@ include file="/WEB-INF/views/common/header.jspf" %>
<!DOCTYPE html>
<html lang="vi"><head><meta charset="UTF-8"><title>Trang chủ nhân viên kho - GaraMan</title>
<link rel="stylesheet" href="${ctx}/css/style.css"></head>
<body>
<%@ include file="/WEB-INF/views/common/topbar.jspf" %>
<div class="container">
<div class="card">
  <h1>Trang chủ nhân viên kho</h1>
  <p class="sub">Chọn chức năng cần thực hiện.</p>
  <div class="menu-grid">
    <a class="menu-item" href="${ctx}/import/suppliers"><b>Nhập phụ tùng</b><small>Chọn nhà cung cấp, lập hóa đơn nhập, cập nhật tồn kho</small></a>
    <a class="menu-item" href="#"><b>Quản lý nhà cung cấp</b><small>Thêm mới, cập nhật thông tin nhà cung cấp (chưa cài đặt)</small></a>
  </div>
</div>
</div>
</body></html>
