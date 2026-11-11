<%@ page isErrorPage="true" %>
<%@ include file="/WEB-INF/views/common/header.jspf" %>
<!DOCTYPE html>
<html lang="vi"><head><meta charset="UTF-8"><title>Lỗi - GaraMan</title>
<link rel="stylesheet" href="${ctx}/css/style.css"></head>
<body>
<%@ include file="/WEB-INF/views/common/topbar.jspf" %>
<div class="container"><div class="card center">
  <h1>Đã xảy ra lỗi</h1>
  <div class="alert err">Đã xảy ra lỗi kết nối, vui lòng thử lại sau</div>
  <a class="btn" href="${ctx}/home">Về trang chủ</a>
</div></div>
</body></html>
