package gara.dao;

import gara.model.catalog.Part4;
import java.sql.SQLException;
import java.util.List;

public interface PartDAO4 {
    /** Tìm phụ tùng có tên chứa key (key rỗng: lấy tất cả). */
    List<Part4> searchPart(String key) throws SQLException;
    Part4 getPartById(int id) throws SQLException;
    /** Khai báo phụ tùng mới (tồn kho ban đầu = 0). */
    boolean addPart(Part4 p) throws SQLException;
}
