package gara.dao.impl;

import gara.dao.DAO;
import gara.dao.PartDAO4;
import gara.model.catalog.Part4;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class PartDAOImpl4 extends DAO implements PartDAO4 {

    private Part4 map(ResultSet rs) throws SQLException {
        Part4 p = new Part4();
        p.setId(rs.getInt("id"));
        p.setCode(rs.getString("code"));
        p.setName(rs.getString("name"));
        p.setUnitPrice(rs.getLong("unitPrice"));
        p.setStockQuantity(rs.getInt("stockQuantity"));
        p.setDescription(rs.getString("description"));
        return p;
    }

    @Override
    public List<Part4> searchPart(String key) throws SQLException {
        List<Part4> list = new ArrayList<>();
        String sql = "SELECT * FROM tblPart4 WHERE name LIKE ? ORDER BY code";
        try (Connection conn = getConnection();
             PreparedStatement pst = conn.prepareStatement(sql)) {
            pst.setString(1, "%" + (key == null ? "" : key.trim()) + "%");
            try (ResultSet rs = pst.executeQuery()) {
                while (rs.next()) list.add(map(rs));
            }
        }
        return list;
    }

    @Override
    public Part4 getPartById(int id) throws SQLException {
        String sql = "SELECT * FROM tblPart4 WHERE id = ?";
        try (Connection conn = getConnection();
             PreparedStatement pst = conn.prepareStatement(sql)) {
            pst.setInt(1, id);
            try (ResultSet rs = pst.executeQuery()) {
                return rs.next() ? map(rs) : null;
            }
        }
    }

    @Override
    public boolean addPart(Part4 p) throws SQLException {
        String sql = "INSERT INTO tblPart4(code, name, unitPrice, stockQuantity, description) VALUES (?,?,?,0,?)";
        try (Connection conn = getConnection();
             PreparedStatement pst = conn.prepareStatement(sql)) {
            pst.setString(1, p.getCode());
            pst.setString(2, p.getName());
            pst.setLong(3, p.getUnitPrice());
            pst.setString(4, p.getDescription());
            return pst.executeUpdate() == 1;
        }
    }
}
