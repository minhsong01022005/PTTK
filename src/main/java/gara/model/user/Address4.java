package gara.model.user;

/** Địa chỉ - thành phần (composition) của Member4 và Supplier4. */
public class Address4 {
    private String street;
    private String city;

    public Address4() {}
    public Address4(String street, String city) {
        this.street = street;
        this.city = city;
    }
    public String getStreet() { return street; }
    public void setStreet(String street) { this.street = street; }
    public String getCity() { return city; }
    public void setCity(String city) { this.city = city; }

    @Override
    public String toString() {
        String s = street == null ? "" : street;
        String c = city == null ? "" : city;
        if (s.isEmpty()) return c;
        if (c.isEmpty()) return s;
        return s + ", " + c;
    }
}
