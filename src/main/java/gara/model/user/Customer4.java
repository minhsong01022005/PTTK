package gara.model.user;

/** Khách hàng - dùng chức năng Tìm kiếm thông tin, Đặt lịch hẹn. */
public class Customer4 extends Member4 {
    private String customerLevel;

    public Customer4() { setRole("CUSTOMER"); }

    public String getCustomerLevel() { return customerLevel; }
    public void setCustomerLevel(String customerLevel) { this.customerLevel = customerLevel; }
}
