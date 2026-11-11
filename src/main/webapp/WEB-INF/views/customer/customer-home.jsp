<%@ include file="/WEB-INF/views/common/header.jspf" %>
<!DOCTYPE html>
<html lang="vi"><head><meta charset="UTF-8"><title>Trang chủ khách hàng - GaraMan</title>
<link rel="stylesheet" href="${ctx}/css/style.css"></head>
<body>
<%@ include file="/WEB-INF/views/common/topbar.jspf" %>
<div class="container">
<div class="card">
  <h1>Trang chủ khách hàng</h1>
  <p class="sub">Chào mừng bạn đến với gara. Chọn chức năng cần dùng.</p>
  <div class="menu-grid">
    <a class="menu-item" href="${ctx}/search"><b>Tìm thông tin dịch vụ / phụ tùng</b><small>Tra cứu dịch vụ, phụ tùng và giá tại gara</small></a>
    <a class="menu-item" href="#"><b>Đặt lịch hẹn trực tuyến</b><small>Chọn ngày giờ và dịch vụ (chưa cài đặt)</small></a>
  </div>
</div>
</div>
</body></html>
