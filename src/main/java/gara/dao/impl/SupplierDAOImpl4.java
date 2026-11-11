package gara.dao.impl;

import gara.dao.DAO;
import gara.dao.SupplierDAO4;
import gara.model.catalog.Supplier4;
import gara.model.user.Address4;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class SupplierDAOImpl4 extends DAO implements SupplierDAO4 {

    private Supplier4 map(ResultSet rs) throws SQLException {
        Supplier4 s = new Supplier4();
        s.setId(rs.getInt("id"));
        s.setCode(rs.getString("code"));
        s.setName(rs.getString("name"));
        s.setTaxCode(rs.getString("taxCode"));
        s.setPhone(rs.getString("phone"));
        s.setEmail(rs.getString("email"));
        s.setAddress(new Address4(rs.getString("street"), rs.getString("city")));
        return s;
    }

    @Override
    public List<Supplier4> searchSupplier(String key) throws SQLException {
        List<Supplier4> list = new ArrayList<>();
        String sql = "SELECT * FROM tblSupplier4 WHERE name LIKE ? OR code LIKE ? ORDER BY code";
        try (Connection conn = getConnection();
             PreparedStatement pst = conn.prepareStatement(sql)) {
            String like = "%" + (key == null ? "" : key.trim()) + "%";
            pst.setString(1, like);
            pst.setString(2, like);
            try (ResultSet rs = pst.executeQuery()) {
                while (rs.next()) list.add(map(rs));
            }
        }
        return list;
    }

    @Override
    public Supplier4 getSupplierById(int id) throws SQLException {
        String sql = "SELECT * FROM tblSupplier4 WHERE id = ?";
        try (Connection conn = getConnection();
             PreparedStatement pst = conn.prepareStatement(sql)) {
            pst.setInt(1, id);
            try (ResultSet rs = pst.executeQuery()) {
                return rs.next() ? map(rs) : null;
            }
        }
    }

    @Override
    public boolean addSupplier(Supplier4 s) throws SQLException {
        String sql = "INSERT INTO tblSupplier4(code, name, taxCode, phone, email, street, city) "
                   + "VALUES (?,?,?,?,?,?,?)";
        try (Connection conn = getConnection();
             PreparedStatement pst = conn.prepareStatement(sql)) {
            pst.setString(1, s.getCode());
            pst.setString(2, s.getName());
            pst.setString(3, s.getTaxCode());
            pst.setString(4, s.getPhone());
            pst.setString(5, s.getEmail());
            pst.setString(6, s.getAddress().getStreet());
            pst.setString(7, s.getAddress().getCity());
            return pst.executeUpdate() == 1;
        }
    }
}
