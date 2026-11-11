package gara.dao.impl;

import gara.dao.DAO;
import gara.dao.ServiceDAO4;
import gara.model.catalog.Service4;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class ServiceDAOImpl4 extends DAO implements ServiceDAO4 {

    private Service4 map(ResultSet rs) throws SQLException {
        Service4 s = new Service4();
        s.setId(rs.getInt("id"));
        s.setCode(rs.getString("code"));
        s.setName(rs.getString("name"));
        s.setPrice(rs.getLong("price"));
        s.setDescription(rs.getString("description"));
        return s;
    }

    @Override
    public List<Service4> searchService(String key) throws SQLException {
        List<Service4> list = new ArrayList<>();
        String sql = "SELECT * FROM tblService4 WHERE name LIKE ? ORDER BY code";
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
    public Service4 getServiceById(int id) throws SQLException {
        String sql = "SELECT * FROM tblService4 WHERE id = ?";
        try (Connection conn = getConnection();
             PreparedStatement pst = conn.prepareStatement(sql)) {
            pst.setInt(1, id);
            try (ResultSet rs = pst.executeQuery()) {
                return rs.next() ? map(rs) : null;
            }
        }
    }
}
