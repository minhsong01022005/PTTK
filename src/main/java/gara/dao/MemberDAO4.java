package gara.dao;

import gara.model.user.Member4;
import java.sql.SQLException;

public interface MemberDAO4 {
    /** Trả về thành viên nếu đúng tài khoản/mật khẩu, ngược lại trả null. */
    Member4 checkLogin(String username, String password) throws SQLException;
}
