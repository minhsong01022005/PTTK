package gara.dao;

import java.io.IOException;
import java.io.InputStream;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Properties;

/** Lớp cha của mọi DAO: giữ phương thức getConnection() (đọc cấu hình trong db.properties). */
public class DAO {
    private static final Properties CFG = new Properties();

    static {
        try (InputStream in = DAO.class.getClassLoader().getResourceAsStream("db.properties")) {
            if (in != null) CFG.load(in);
            Class.forName("com.mysql.cj.jdbc.Driver");
        } catch (IOException | ClassNotFoundException e) {
            throw new ExceptionInInitializerError(e);
        }
    }

    protected Connection getConnection() throws SQLException {
        return DriverManager.getConnection(
                CFG.getProperty("db.url"),
                CFG.getProperty("db.user"),
                CFG.getProperty("db.password", ""));
    }
}
