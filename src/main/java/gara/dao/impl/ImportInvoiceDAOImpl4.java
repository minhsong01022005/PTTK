package gara.dao.impl;

import gara.dao.DAO;
import gara.dao.ImportInvoiceDAO4;
import gara.model.transaction.ImportDetail4;
import gara.model.transaction.ImportInvoice4;

import java.sql.*;

public class ImportInvoiceDAOImpl4 extends DAO implements ImportInvoiceDAO4 {

    @Override
    public boolean addImportInvoice(ImportInvoice4 hd) throws SQLException {
        String sqlInvoice = "INSERT INTO tblImportInvoice4(importDate, totalAmount, supplierId, inventoryStaffId) "
                          + "VALUES (?,?,?,?)";
        String sqlDetail  = "INSERT INTO tblImportDetail4(importInvoiceId, partId, quantity, unitPrice) VALUES (?,?,?,?)";
        String sqlStock   = "UPDATE tblPart4 SET stockQuantity = stockQuantity + ? WHERE id = ?";

        try (Connection conn = getConnection()) {
            conn.setAutoCommit(false);
            try {
                int invoiceId;
                try (PreparedStatement pst = conn.prepareStatement(sqlInvoice, Statement.RETURN_GENERATED_KEYS)) {
                    pst.setTimestamp(1, new Timestamp(hd.getImportDate().getTime()));
                    pst.setLong(2, hd.getTotalAmount());
                    pst.setInt(3, hd.getSupplier().getId());
                    pst.setInt(4, hd.getInventoryStaff().getId());
                    pst.executeUpdate();
                    try (ResultSet keys = pst.getGeneratedKeys()) {
                        if (!keys.next()) throw new SQLException("Không lấy được id hóa đơn");
                        invoiceId = keys.getInt(1);
                    }
                }
                try (PreparedStatement pstD = conn.prepareStatement(sqlDetail);
                     PreparedStatement pstS = conn.prepareStatement(sqlStock)) {
                    for (ImportDetail4 d : hd.getListDetail()) {
                        pstD.setInt(1, invoiceId);
                        pstD.setInt(2, d.getPart().getId());
                        pstD.setInt(3, d.getQuantity());
                        pstD.setLong(4, d.getUnitPrice());
                        pstD.executeUpdate();

                        pstS.setInt(1, d.getQuantity());
                        pstS.setInt(2, d.getPart().getId());
                        pstS.executeUpdate();
                    }
                }
                conn.commit();
                hd.setId(invoiceId);
                return true;
            } catch (SQLException ex) {
                conn.rollback();
                return false;
            } finally {
                conn.setAutoCommit(true);
            }
        }
    }
}
