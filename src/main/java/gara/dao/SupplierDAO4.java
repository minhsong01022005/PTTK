package gara.dao;

import gara.model.catalog.Supplier4;
import java.sql.SQLException;
import java.util.List;

public interface SupplierDAO4 {
    /** Tìm nhà cung cấp có tên chứa key (key rỗng: lấy tất cả). */
    List<Supplier4> searchSupplier(String key) throws SQLException;
    Supplier4 getSupplierById(int id) throws SQLException;
    /** Thêm mới; trả về true nếu thành công, ném SQLException nếu trùng mã. */
    boolean addSupplier(Supplier4 s) throws SQLException;
}
