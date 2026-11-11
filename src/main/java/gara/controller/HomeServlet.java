package gara.controller;

import gara.model.user.Member4;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;
import java.io.IOException;

/** Trang chủ theo vai trò: nhân viên kho -> nvkho-home.jsp, khách hàng -> customer-home.jsp. */
@WebServlet("/home")
public class HomeServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        Member4 m = (Member4) req.getSession().getAttribute("member");
        String view;
        switch (m.getRole()) {
            case "INVENTORY": view = "/WEB-INF/views/inventory/nvkho-home.jsp"; break;
            case "CUSTOMER":  view = "/WEB-INF/views/customer/customer-home.jsp"; break;
            default:          view = "/WEB-INF/views/common/chua-ho-tro.jsp";
        }
        req.getRequestDispatcher(view).forward(req, resp);
    }
}
