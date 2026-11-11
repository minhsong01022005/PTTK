package gara.dao;

import gara.model.transaction.ImportInvoice4;
import java.sql.SQLException;

public interface ImportInvoiceDAO4 {
    /**
     * Lưu hóa đơn + các dòng chi tiết và cộng dồn tồn kho trong MỘT transaction.
     * Trả về false (và rollback) nếu có lỗi khi ghi.
     */
    boolean addImportInvoice(ImportInvoice4 hd) throws SQLException;
}
