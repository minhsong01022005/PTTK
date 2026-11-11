<%@ include file="/WEB-INF/views/common/header.jspf" %>
<!DOCTYPE html>
<html lang="vi"><head><meta charset="UTF-8"><title>Đăng nhập - GaraMan</title>
<link rel="stylesheet" href="${ctx}/css/style.css"></head>
<body>
<div class="topbar"><div class="brand">Gara<span>Man</span> &nbsp;|&nbsp; Quản lý gara ô tô</div></div>
<div class="login-wrap"><div class="card">
  <h1 class="center">Đăng nhập</h1>
  <p class="sub center">Nhân viên và khách hàng đăng nhập để sử dụng hệ thống</p>
  <c:if test="${not empty loi}"><div class="alert err"><c:out value="${loi}"/></div></c:if>
  <form method="post" action="${ctx}/login">
    <div class="form-grid" style="grid-template-columns:110px 1fr">
      <label>Tài khoản</label><input type="text" name="username" value="<c:out value='${username}'/>" autofocus>
      <label>Mật khẩu</label><input type="password" name="password">
    </div>
    <div class="actions"><button class="btn" type="submit">Đăng nhập</button></div>
  </form>
</div></div>
</body></html>
