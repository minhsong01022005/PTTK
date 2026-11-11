package gara.model.transaction;

import gara.model.catalog.Part4;

/** Một dòng chi tiết của hóa đơn nhập (composition của ImportInvoice4). */
public class ImportDetail4 {
    private int id;
    private Part4 part;
    private int quantity;
    private long unitPrice;

    public ImportDetail4() {}
    public ImportDetail4(Part4 part, int quantity, long unitPrice) {
        this.part = part;
        this.quantity = quantity;
        this.unitPrice = unitPrice;
    }

    /** Thành tiền của dòng = số lượng x đơn giá. */
    public long getAmount() { return (long) quantity * unitPrice; }

    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public Part4 getPart() { return part; }
    public void setPart(Part4 part) { this.part = part; }
    public int getQuantity() { return quantity; }
    public void setQuantity(int quantity) { this.quantity = quantity; }
    public long getUnitPrice() { return unitPrice; }
    public void setUnitPrice(long unitPrice) { this.unitPrice = unitPrice; }
}
