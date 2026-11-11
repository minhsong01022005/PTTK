package gara.controller;

import gara.dao.PartDAO4;
import gara.dao.ServiceDAO4;
import gara.dao.impl.PartDAOImpl4;
import gara.dao.impl.ServiceDAOImpl4;
import gara.model.catalog.Part4;
import gara.model.catalog.Service4;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;
import java.io.IOException;
import java.sql.SQLException;
import java.util.List;

/**
 * Controller của module "Tìm kiếm thông tin dịch vụ/phụ tùng".
 *   GET /search                      -> trang tìm kiếm trống
 *   GET /search?key=...              -> tìm dịch vụ + phụ tùng
 *   GET /search/detail?type=&id=     -> chi tiết một dịch vụ hoặc phụ tùng
 */
@WebServlet(urlPatterns = {"/search", "/search/*"})
public class SearchServlet extends HttpServlet {
    private static final String V = "/WEB-INF/views/customer/";
    private final ServiceDAO4 serviceDAO = new ServiceDAOImpl4();
    private final PartDAO4 partDAO = new PartDAOImpl4();

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String path = req.getPathInfo();
        try {
            if (path == null || path.equals("/")) {
                if (req.getParameter("key") == null) showSearchForm(req, resp);
                else search(req, resp);
            } else if (path.equals("/detail")) {
                showDetail(req, resp);
            } else {
                resp.sendError(HttpServletResponse.SC_NOT_FOUND);
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        doGet(req, resp);
    }

    private void showSearchForm(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        req.getRequestDispatcher(V + "tim-kiem.jsp").forward(req, resp);
    }

    private void search(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException, SQLException {
        String key = req.getParameter("key");
        key = key == null ? "" : key.trim();
        req.setAttribute("key", key);
        if (key.isEmpty()) {                                   // ngoại lệ: bỏ trống từ khóa
            req.setAttribute("loi", "Vui lòng nhập từ khóa dịch vụ/phụ tùng cần tìm");
            showSearchForm(req, resp);
            return;
        }
        List<Service4> listService = serviceDAO.searchService(key);
        List<Part4> listPart = partDAO.searchPart(key);
        req.setAttribute("listService", listService);
        req.setAttribute("listPart", listPart);
        req.setAttribute("daTim", Boolean.TRUE);
        if (listService.isEmpty() && listPart.isEmpty()) {     // ngoại lệ: không có kết quả
            req.setAttribute("thongBao", "Không tìm thấy kết quả phù hợp");
        }
        showSearchForm(req, resp);
    }

    private void showDetail(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException, SQLException {
        String type = req.getParameter("type");
        int id;
        try {
            id = Integer.parseInt(req.getParameter("id"));
        } catch (NumberFormatException e) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "id không hợp lệ");
            return;
        }
        String key = req.getParameter("key");
        req.setAttribute("key", key == null ? "" : key);
        if ("service".equals(type)) {
            Service4 sv = serviceDAO.getServiceById(id);
            if (sv == null) { resp.sendError(HttpServletResponse.SC_NOT_FOUND); return; }
            req.setAttribute("loai", "Dịch vụ");
            req.setAttribute("ma", sv.getCode());
            req.setAttribute("ten", sv.getName());
            req.setAttribute("gia", sv.getPrice());
            req.setAttribute("moTa", sv.getDescription());
        } else if ("part".equals(type)) {
            Part4 p = partDAO.getPartById(id);
            if (p == null) { resp.sendError(HttpServletResponse.SC_NOT_FOUND); return; }
            req.setAttribute("loai", "Phụ tùng");
            req.setAttribute("ma", p.getCode());
            req.setAttribute("ten", p.getName());
            req.setAttribute("gia", p.getUnitPrice());
            req.setAttribute("moTa", p.getDescription());
            req.setAttribute("tonKho", p.getStockQuantity());
        } else {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "type không hợp lệ");
            return;
        }
        req.getRequestDispatcher(V + "chi-tiet.jsp").forward(req, resp);
    }
}
