package gara.model.catalog;

/** Dịch vụ của gara. price tính theo VNĐ (số nguyên). */
public class Service4 {
    private int id;
    private String code;
    private String name;
    private long price;
    private String description;

    public Service4() {}

    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public String getCode() { return code; }
    public void setCode(String code) { this.code = code; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public long getPrice() { return price; }
    public void setPrice(long price) { this.price = price; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
}
