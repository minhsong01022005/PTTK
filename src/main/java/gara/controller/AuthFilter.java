package gara.controller;

import gara.model.user.Member4;

import javax.servlet.*;
import javax.servlet.annotation.WebFilter;
import javax.servlet.http.*;
import java.io.IOException;

/**
 * Chặn truy cập khi chưa đăng nhập hoặc sai vai trò:
 *  /import/*  chỉ dành cho nhân viên kho (INVENTORY),
 *  /search/*  chỉ dành cho khách hàng (CUSTOMER),
 *  /home      cần đăng nhập.
 */
@WebFilter(urlPatterns = {"/import/*", "/search/*", "/search", "/home"})
public class AuthFilter implements Filter {
    @Override
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {
        HttpServletRequest request = (HttpServletRequest) req;
        HttpServletResponse response = (HttpServletResponse) res;
        HttpSession session = request.getSession(false);
        Member4 m = session == null ? null : (Member4) session.getAttribute("member");
        String ctx = request.getContextPath();
        if (m == null) {
            response.sendRedirect(ctx + "/login");
            return;
        }
        String path = request.getServletPath();
        boolean ok = true;
        if (path.startsWith("/import")) ok = "INVENTORY".equals(m.getRole());
        else if (path.startsWith("/search")) ok = "CUSTOMER".equals(m.getRole());
        if (!ok) {
            response.sendError(HttpServletResponse.SC_FORBIDDEN, "Bạn không có quyền dùng chức năng này");
            return;
        }
        chain.doFilter(req, res);
    }
}
