package gara.model.user;

/** Nhân viên bán hàng. */
public class SalesStaff4 extends Staff4 {
    private String counterId;

    public SalesStaff4() { setRole("SALES"); }

    public String getCounterId() { return counterId; }
    public void setCounterId(String counterId) { this.counterId = counterId; }
}
