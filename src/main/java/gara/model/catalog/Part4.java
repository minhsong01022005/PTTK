package gara.model.catalog;

/** Phụ tùng. unitPrice tính theo VNĐ (số nguyên). */
public class Part4 {
    private int id;
    private String code;
    private String name;
    private long unitPrice;       // đơn giá nhập tham khảo
    private int stockQuantity;    // số lượng tồn kho
    private String description;

    public Part4() {}

    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public String getCode() { return code; }
    public void setCode(String code) { this.code = code; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public long getUnitPrice() { return unitPrice; }
    public void setUnitPrice(long unitPrice) { this.unitPrice = unitPrice; }
    public int getStockQuantity() { return stockQuantity; }
    public void setStockQuantity(int stockQuantity) { this.stockQuantity = stockQuantity; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
}
