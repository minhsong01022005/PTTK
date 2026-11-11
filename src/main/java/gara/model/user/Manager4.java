package gara.model.user;

/** Nhân viên quản lí. */
public class Manager4 extends Staff4 {
    private String managementLevel;

    public Manager4() { setRole("MANAGER"); }

    public String getManagementLevel() { return managementLevel; }
    public void setManagementLevel(String managementLevel) { this.managementLevel = managementLevel; }
}
