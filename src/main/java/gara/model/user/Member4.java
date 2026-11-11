package gara.model.user;

/** Lớp cha của mọi người dùng hệ thống (khách hàng và nhân viên). */
public class Member4 {
    private int id;
    private String username;
    private String password;      // lưu dạng băm SHA-256 trong CSDL
    private FullName4 fullName = new FullName4();
    private Address4 address = new Address4();
    private String phone;
    private String email;
    private String role;          // CUSTOMER | MANAGER | SALES | INVENTORY | TECHNICIAN

    public Member4() {}

    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }
    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }
    public FullName4 getFullName() { return fullName; }
    public void setFullName(FullName4 fullName) { this.fullName = fullName; }
    public Address4 getAddress() { return address; }
    public void setAddress(Address4 address) { this.address = address; }
    public String getPhone() { return phone; }
    public void setPhone(String phone) { this.phone = phone; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public String getRole() { return role; }
    public void setRole(String role) { this.role = role; }
}
