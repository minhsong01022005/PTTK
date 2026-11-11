package gara.model.catalog;

import gara.model.user.Address4;

/** Nhà cung cấp phụ tùng. */
public class Supplier4 {
    private int id;
    private String code;
    private String name;
    private String taxCode;
    private String phone;
    private String email;
    private Address4 address = new Address4();

    public Supplier4() {}

    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public String getCode() { return code; }
    public void setCode(String code) { this.code = code; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getTaxCode() { return taxCode; }
    public void setTaxCode(String taxCode) { this.taxCode = taxCode; }
    public String getPhone() { return phone; }
    public void setPhone(String phone) { this.phone = phone; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public Address4 getAddress() { return address; }
    public void setAddress(Address4 address) { this.address = address; }
}
