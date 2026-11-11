package gara.model.user;

/** Nhân viên kho - tác nhân của chức năng Nhập phụ tùng. */
public class InventoryStaff4 extends Staff4 {
    private String warehouseId;

    public InventoryStaff4() { setRole("INVENTORY"); }

    public String getWarehouseId() { return warehouseId; }
    public void setWarehouseId(String warehouseId) { this.warehouseId = warehouseId; }
}
