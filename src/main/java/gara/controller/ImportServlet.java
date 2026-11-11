package gara.controller;

import gara.dao.ImportInvoiceDAO4;
import gara.dao.PartDAO4;
import gara.dao.SupplierDAO4;
import gara.dao.impl.ImportInvoiceDAOImpl4;
import gara.dao.impl.PartDAOImpl4;
import gara.dao.impl.SupplierDAOImpl4;
import gara.model.catalog.Part4;
import gara.model.catalog.Supplier4;
import gara.model.transaction.ImportDetail4;
import gara.model.transaction.ImportInvoice4;
import gara.model.user.Address4;
import gara.model.user.InventoryStaff4;
import gara.model.user.Member4;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;
import java.io.IOException;
import java.sql.SQLException;
import java.util.List;

/**
 * Controller của module "Nhập phụ tùng" (/import/*).
 * Hóa đơn đang lập được giữ trong HttpSession với khóa "hoaDon".
 * Các thao tác ghi (POST) đều kết thúc bằng redirect (Post-Redirect-Get).
 */
@WebServlet("/import/*")
public class ImportServlet extends HttpServlet {
    private static final String V = "/WEB-INF/views/inventory/";
    private final SupplierDAO4 supplierDAO = new SupplierDAOImpl4();
    private final PartDAO4 partDAO = new PartDAOImpl4();
    private final ImportInvoiceDAO4 invoiceDAO = new ImportInvoiceDAOImpl4();

    // ------------------------------------------------------------------ GET
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String path = req.getPathInfo() == null ? "" : req.getPathInfo();
        try {
            switch (path) {
                case "/suppliers":        listSupplier(req, resp); break;
                case "/supplier/new":     forward(req, resp, "them-ncc.jsp"); break;
                case "/invoice/new":      newInvoice(req, resp); break;
                case "/invoice/view":     viewInvoice(req, resp); break;
                case "/parts":            listPart(req, resp); break;
                case "/part/new":         forward(req, resp, "them-phu-tung.jsp"); break;
                case "/detail/form":      showDetailForm(req, resp); break;
                case "/invoice/print":    printInvoice(req, resp); break;
                default:                  resp.sendError(HttpServletResponse.SC_NOT_FOUND);
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }

    // ----------------------------------------------------------------- POST
    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String path = req.getPathInfo() == null ? "" : req.getPathInfo();
        try {
            switch (path) {
                case "/supplier/insert":  addSupplier(req, resp); break;
                case "/part/insert":      addPart(req, resp); break;
                case "/detail/add":       saveDetail(req, resp, false); break;
                case "/detail/update":    saveDetail(req, resp, true); break;
                case "/detail/remove":    removeDetail(req, resp); break;
                case "/invoice/confirm":  confirmInvoice(req, resp); break;
                case "/invoice/cancel":   cancelInvoice(req, resp); break;
                default:                  resp.sendError(HttpServletResponse.SC_NOT_FOUND);
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }

    // ------------------------------------------------- chọn nhà cung cấp
    private void listSupplier(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException, SQLException {
        String key = nz(req.getParameter("key"));
        List<Supplier4> list = supplierDAO.searchSupplier(key);
        req.setAttribute("key", key);
        req.setAttribute("listSupplier", list);
        if (list.isEmpty()) req.setAttribute("thongBao", "Không tìm thấy nhà cung cấp. Bạn có thể thêm mới.");
        forward(req, resp, "chon-ncc.jsp");
    }

    private void addSupplier(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException, SQLException {
        Supplier4 s = new Supplier4();
        s.setCode(nz(req.getParameter("code")));
        s.setName(nz(req.getParameter("name")));
        s.setTaxCode(nz(req.getParameter("taxCode")));
        s.setPhone(nz(req.getParameter("phone")));
        s.setEmail(nz(req.getParameter("email")));
        s.setAddress(new Address4(nz(req.getParameter("street")), nz(req.getParameter("city"))));
        req.setAttribute("ncc", s);
        if (s.getCode().isEmpty()) s.setCode(autoCode("NCC"));          // mã để trống -> hệ thống tự sinh
        if (s.getName().isEmpty() || s.getPhone().isEmpty()) {
            req.setAttribute("loi", "Tên và số điện thoại nhà cung cấp là bắt buộc");
            forward(req, resp, "them-ncc.jsp");
            return;
        }
        if (!s.getPhone().matches("[0-9 .+\\-]{8,15}")) {
            req.setAttribute("loi", "Số điện thoại không hợp lệ");
            forward(req, resp, "them-ncc.jsp");
            return;
        }
        try {
            supplierDAO.addSupplier(s);
        } catch (SQLException e) {
            if (isDuplicate(e)) {
                req.setAttribute("loi", "Mã nhà cung cấp \"" + s.getCode() + "\" đã tồn tại");
                forward(req, resp, "them-ncc.jsp");
                return;
            }
            throw e;
        }
        resp.sendRedirect(req.getContextPath() + "/import/suppliers?key=" + enc(s.getCode()));
    }

    // ------------------------------------------------- lập hóa đơn
    private void newInvoice(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException, SQLException {
        Integer supplierId = parseInt(req.getParameter("supplierId"));
        Supplier4 ncc = supplierId == null ? null : supplierDAO.getSupplierById(supplierId);
        if (ncc == null) {
            resp.sendRedirect(req.getContextPath() + "/import/suppliers");
            return;
        }
        HttpSession session = req.getSession();
        ImportInvoice4 hoaDon = new ImportInvoice4();
        hoaDon.setSupplier(ncc);
        hoaDon.setInventoryStaff(toInventoryStaff((Member4) session.getAttribute("member")));
        session.setAttribute("hoaDon", hoaDon);
        resp.sendRedirect(req.getContextPath() + "/import/invoice/view");
    }

    private void viewInvoice(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        if (currentInvoice(req) == null) {
            resp.sendRedirect(req.getContextPath() + "/import/suppliers");
            return;
        }
        moveFlash(req);
        forward(req, resp, "lap-hoa-don.jsp");
    }

    // ------------------------------------------------- chọn phụ tùng
    private void listPart(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException, SQLException {
        if (currentInvoice(req) == null) { resp.sendRedirect(req.getContextPath() + "/import/suppliers"); return; }
        String key = nz(req.getParameter("key"));
        List<Part4> list = partDAO.searchPart(key);
        req.setAttribute("key", key);
        req.setAttribute("listPart", list);
        if (list.isEmpty()) req.setAttribute("thongBao", "Không tìm thấy phụ tùng. Bạn có thể thêm mới.");
        forward(req, resp, "chon-phu-tung.jsp");
    }

    private void addPart(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException, SQLException {
        Part4 p = new Part4();
        p.setCode(nz(req.getParameter("code")));
        p.setName(nz(req.getParameter("name")));
        p.setDescription(nz(req.getParameter("description")));
        Long price = parseMoney(req.getParameter("unitPrice"));
        req.setAttribute("pt", p);
        req.setAttribute("giaNhap", nz(req.getParameter("unitPrice")));
        if (p.getCode().isEmpty()) p.setCode(autoCode("PT"));           // mã để trống -> hệ thống tự sinh
        if (p.getName().isEmpty()) {
            req.setAttribute("loi", "Tên phụ tùng là bắt buộc");
            forward(req, resp, "them-phu-tung.jsp");
            return;
        }
        boolean blankPrice = nz(req.getParameter("unitPrice")).isEmpty();
        if (!blankPrice && (price == null || price <= 0)) {
            req.setAttribute("loi", "Đơn giá tham khảo phải là số dương");
            forward(req, resp, "them-phu-tung.jsp");
            return;
        }
        p.setUnitPrice(blankPrice ? 0L : price);
        try {
            partDAO.addPart(p);
        } catch (SQLException e) {
            if (isDuplicate(e)) {
                req.setAttribute("loi", "Mã phụ tùng \"" + p.getCode() + "\" đã tồn tại");
                forward(req, resp, "them-phu-tung.jsp");
                return;
            }
            throw e;
        }
        resp.sendRedirect(req.getContextPath() + "/import/parts?key=" + enc(p.getName()));
    }

    // ------------------------------------------------- nhập số lượng, đơn giá
    private void showDetailForm(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException, SQLException {
        ImportInvoice4 hd = currentInvoice(req);
        if (hd == null) { resp.sendRedirect(req.getContextPath() + "/import/suppliers"); return; }
        Integer index = parseInt(req.getParameter("index"));          // có index: đang sửa dòng
        if (index != null && index >= 0 && index < hd.getListDetail().size()) {
            ImportDetail4 d = hd.getListDetail().get(index);
            req.setAttribute("pt", d.getPart());
            req.setAttribute("index", index);
            req.setAttribute("soLuong", d.getQuantity());
            req.setAttribute("donGia", d.getUnitPrice());
        } else {
            Integer partId = parseInt(req.getParameter("partId"));
            Part4 pt = partId == null ? null : partDAO.getPartById(partId);
            if (pt == null) { resp.sendRedirect(req.getContextPath() + "/import/parts"); return; }
            req.setAttribute("pt", pt);
            req.setAttribute("donGia", pt.getUnitPrice());
        }
        forward(req, resp, "nhap-so-luong.jsp");
    }

    /** Thêm (update=false) hoặc sửa (update=true) một dòng chi tiết. */
    private void saveDetail(HttpServletRequest req, HttpServletResponse resp, boolean update)
            throws ServletException, IOException, SQLException {
        ImportInvoice4 hd = currentInvoice(req);
        if (hd == null) { resp.sendRedirect(req.getContextPath() + "/import/suppliers"); return; }
        Integer partId = parseInt(req.getParameter("partId"));
        Part4 pt = partId == null ? null : partDAO.getPartById(partId);
        if (pt == null) { resp.sendRedirect(req.getContextPath() + "/import/parts"); return; }

        String sl = nz(req.getParameter("quantity"));
        String dg = nz(req.getParameter("unitPrice"));
        if (!validate(sl, dg)) {                                         // ngoại lệ: dữ liệu không hợp lệ
            boolean slOk = validate(sl, "1");
            req.setAttribute("loi", slOk ? "Đơn giá phải là số dương" : "Số lượng phải là số nguyên dương");
            req.setAttribute("loiTruong", slOk ? "unitPrice" : "quantity");
            req.setAttribute("pt", pt);
            req.setAttribute("soLuong", sl);
            req.setAttribute("donGia", dg);
            if (update) req.setAttribute("index", parseInt(req.getParameter("index")));
            forward(req, resp, "nhap-so-luong.jsp");
            return;
        }
        int quantity = Integer.parseInt(sl.trim());
        long unitPrice = parseMoney(dg);
        if (update) {
            Integer index = parseInt(req.getParameter("index"));
            if (index == null || !hd.updateDetail(index, quantity, unitPrice)) {
                resp.sendError(HttpServletResponse.SC_BAD_REQUEST);
                return;
            }
        } else {
            hd.addDetail(new ImportDetail4(pt, quantity, unitPrice));
        }
        resp.sendRedirect(req.getContextPath() + "/import/invoice/view");
    }

    private void removeDetail(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        ImportInvoice4 hd = currentInvoice(req);
        Integer index = parseInt(req.getParameter("index"));
        if (hd != null && index != null) hd.removeDetail(index);
        resp.sendRedirect(req.getContextPath() + "/import/invoice/view");
    }

    // ------------------------------------------------- xác nhận / hủy
    private void confirmInvoice(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException, SQLException {
        ImportInvoice4 hd = currentInvoice(req);
        if (hd == null) { resp.sendRedirect(req.getContextPath() + "/import/suppliers"); return; }
        HttpSession session = req.getSession();
        if (hd.getListDetail().isEmpty()) {
            session.setAttribute("flashLoi", "Hóa đơn chưa có phụ tùng nào");
            resp.sendRedirect(req.getContextPath() + "/import/invoice/view");
            return;
        }
        boolean ok = invoiceDAO.addImportInvoice(hd);
        if (!ok) {                                                       // ngoại lệ: lỗi khi lưu (đã rollback)
            session.setAttribute("flashLoi", "Lưu hóa đơn thất bại, vui lòng thử lại");
            resp.sendRedirect(req.getContextPath() + "/import/invoice/view");
            return;
        }
        session.removeAttribute("hoaDon");
        session.setAttribute("hoaDonDaLuu", hd);
        resp.sendRedirect(req.getContextPath() + "/import/invoice/print");
    }

    private void printInvoice(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        Object hd = req.getSession().getAttribute("hoaDonDaLuu");
        if (hd == null) { resp.sendRedirect(req.getContextPath() + "/home"); return; }
        req.setAttribute("hoaDon", hd);
        forward(req, resp, "in-hoa-don.jsp");
    }

    private void cancelInvoice(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        req.getSession().removeAttribute("hoaDon");
        resp.sendRedirect(req.getContextPath() + "/home");
    }

    // ------------------------------------------------- tiện ích
    /** Số lượng và đơn giá phải là số nguyên dương (đơn giá cho phép dấu chấm/phẩy ngăn cách hàng nghìn). */
    static boolean validate(String soLuong, String donGia) {
        Integer sl = parseInt(soLuong);
        Long dg = parseMoney(donGia);
        return sl != null && sl > 0 && sl <= 1_000_000 && dg != null && dg > 0;
    }

    static Integer parseInt(String s) {
        if (s == null) return null;
        try { return Integer.valueOf(s.trim()); } catch (NumberFormatException e) { return null; }
    }

    /** "1.950.000" | "1,950,000" | "1950000" -> 1950000; chuỗi sai -> null. */
    static Long parseMoney(String s) {
        if (s == null) return null;
        String t = s.trim();
        // chỉ nhận số nguyên, hoặc số có dấu . / , ngăn cách đúng từng nhóm 3 chữ số
        if (!t.matches("[0-9]{1,15}|[0-9]{1,3}([.,][0-9]{3}){1,4}")) return null;
        return Long.valueOf(t.replace(".", "").replace(",", ""));
    }

    private static String nz(String s) { return s == null ? "" : s.trim(); }

    private static String enc(String s) {
        try { return java.net.URLEncoder.encode(s, "UTF-8"); } catch (java.io.UnsupportedEncodingException e) { return s; }
    }

    private static boolean isDuplicate(SQLException e) {
        return e.getSQLState() != null && e.getSQLState().startsWith("23");
    }

    private static ImportInvoice4 currentInvoice(HttpServletRequest req) {
        HttpSession s = req.getSession(false);
        return s == null ? null : (ImportInvoice4) s.getAttribute("hoaDon");
    }

    private static InventoryStaff4 toInventoryStaff(Member4 m) {
        InventoryStaff4 st = new InventoryStaff4();
        st.setId(m.getId());
        st.setUsername(m.getUsername());
        st.setFullName(m.getFullName());
        return st;
    }

    /** Chuyển thông báo "flash" từ session sang request (hiển thị một lần). */
    private static void moveFlash(HttpServletRequest req) {
        HttpSession s = req.getSession();
        Object loi = s.getAttribute("flashLoi");
        if (loi != null) { req.setAttribute("loi", loi); s.removeAttribute("flashLoi"); }
    }

    /** Sinh mã tự động (ví dụ NCC48213) khi người dùng để trống ô mã. */
    private static String autoCode(String prefix) {
        return prefix + String.format("%05d", (System.currentTimeMillis() / 1000) % 100000);
    }

    private void forward(HttpServletRequest req, HttpServletResponse resp, String jsp)
            throws ServletException, IOException {
        req.getRequestDispatcher(V + jsp).forward(req, resp);
    }
}
