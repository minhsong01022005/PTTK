package gara.controller;

import gara.dao.MemberDAO4;
import gara.dao.impl.MemberDAOImpl4;
import gara.model.user.Member4;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;
import java.io.IOException;
import java.sql.SQLException;

@WebServlet("/login")
public class LoginServlet extends HttpServlet {
    private final MemberDAO4 memberDAO = new MemberDAOImpl4();

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        req.getRequestDispatcher("/WEB-INF/views/common/login.jsp").forward(req, resp);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String username = req.getParameter("username");
        String password = req.getParameter("password");
        if (username == null || username.trim().isEmpty() || password == null || password.isEmpty()) {
            req.setAttribute("loi", "Vui lòng nhập tài khoản và mật khẩu");
            req.getRequestDispatcher("/WEB-INF/views/common/login.jsp").forward(req, resp);
            return;
        }
        try {
            Member4 m = memberDAO.checkLogin(username.trim(), password);
            if (m == null) {
                req.setAttribute("loi", "Sai tài khoản hoặc mật khẩu");
                req.setAttribute("username", username);
                req.getRequestDispatcher("/WEB-INF/views/common/login.jsp").forward(req, resp);
                return;
            }
            req.getSession().invalidate();                 // chống session fixation
            req.getSession(true).setAttribute("member", m);
            resp.sendRedirect(req.getContextPath() + "/home");
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
