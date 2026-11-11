package gara.dao;

import gara.model.catalog.Service4;
import java.sql.SQLException;
import java.util.List;

public interface ServiceDAO4 {
    List<Service4> searchService(String key) throws SQLException;
    Service4 getServiceById(int id) throws SQLException;
}
