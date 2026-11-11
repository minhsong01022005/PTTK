package gara.dao.impl;

import gara.dao.DAO;
import gara.dao.MemberDAO4;
import gara.model.user.*;
import gara.util.PasswordUtil;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class MemberDAOImpl4 extends DAO implements MemberDAO4 {

    @Override
    public Member4 checkLogin(String username, String password) throws SQLException {
        String sql = "SELECT id, username, firstName, lastName, street, city, phone, email, role "
                   + "FROM tblMember4 WHERE username = ? AND password = ?";
        try (Connection conn = getConnection();
             PreparedStatement pst = conn.prepareStatement(sql)) {
            pst.setString(1, username);
            pst.setString(2, PasswordUtil.sha256(password));
            try (ResultSet rs = pst.executeQuery()) {
                if (!rs.next()) return null;
                String role = rs.getString("role");
                Member4 m;
                if ("INVENTORY".equals(role)) m = new InventoryStaff4();
                else if ("CUSTOMER".equals(role)) m = new Customer4();
                else m = new Member4();
                m.setId(rs.getInt("id"));
                m.setUsername(rs.getString("username"));
                m.setFullName(new FullName4(rs.getString("firstName"), rs.getString("lastName")));
                m.setAddress(new Address4(rs.getString("street"), rs.getString("city")));
                m.setPhone(rs.getString("phone"));
                m.setEmail(rs.getString("email"));
                m.setRole(role);
                return m;
            }
        }
    }
}
