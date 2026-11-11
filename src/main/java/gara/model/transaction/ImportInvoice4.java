package gara.model.transaction;

import gara.model.catalog.Supplier4;
import gara.model.user.InventoryStaff4;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

/** Hóa đơn nhập phụ tùng. Được giữ tạm trong HttpSession cho tới khi xác nhận. */
public class ImportInvoice4 {
    private int id;
    private Date importDate = new Date();
    private Supplier4 supplier;
    private InventoryStaff4 inventoryStaff;
    private List<ImportDetail4> listDetail = new ArrayList<>();
    private long totalAmount;

    public ImportInvoice4() {}

    /**
     * Thêm một dòng chi tiết. Nếu phụ tùng đã có trong hóa đơn thì cộng dồn
     * số lượng (đơn giá lấy theo lần nhập sau) để mỗi phụ tùng chỉ xuất hiện một dòng.
     */
    public void addDetail(ImportDetail4 ct) {
        for (ImportDetail4 d : listDetail) {
            if (d.getPart().getId() == ct.getPart().getId()) {
                d.setQuantity(d.getQuantity() + ct.getQuantity());
                d.setUnitPrice(ct.getUnitPrice());
                recalc();
                return;
            }
        }
        listDetail.add(ct);
        recalc();
    }

    /** Sửa số lượng, đơn giá của dòng thứ index (bắt đầu từ 0). */
    public boolean updateDetail(int index, int quantity, long unitPrice) {
        if (index < 0 || index >= listDetail.size()) return false;
        ImportDetail4 d = listDetail.get(index);
        d.setQuantity(quantity);
        d.setUnitPrice(unitPrice);
        recalc();
        return true;
    }

    /** Xóa dòng thứ index (bắt đầu từ 0). */
    public boolean removeDetail(int index) {
        if (index < 0 || index >= listDetail.size()) return false;
        listDetail.remove(index);
        recalc();
        return true;
    }

    private void recalc() {
        long sum = 0;
        for (ImportDetail4 d : listDetail) sum += d.getAmount();
        totalAmount = sum;
    }

    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public Date getImportDate() { return importDate; }
    public void setImportDate(Date importDate) { this.importDate = importDate; }
    public Supplier4 getSupplier() { return supplier; }
    public void setSupplier(Supplier4 supplier) { this.supplier = supplier; }
    public InventoryStaff4 getInventoryStaff() { return inventoryStaff; }
    public void setInventoryStaff(InventoryStaff4 inventoryStaff) { this.inventoryStaff = inventoryStaff; }
    public List<ImportDetail4> getListDetail() { return listDetail; }
    public void setListDetail(List<ImportDetail4> listDetail) { this.listDetail = listDetail; recalc(); }
    public long getTotalAmount() { return totalAmount; }
}
