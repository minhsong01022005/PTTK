package gara.model.user;

/** Họ tên - thành phần (composition) của Member4. */
public class FullName4 {
    private String firstName;
    private String lastName;

    public FullName4() {}
    public FullName4(String firstName, String lastName) {
        this.firstName = firstName;
        this.lastName = lastName;
    }
    public String getFirstName() { return firstName; }
    public void setFirstName(String firstName) { this.firstName = firstName; }
    public String getLastName() { return lastName; }
    public void setLastName(String lastName) { this.lastName = lastName; }

    @Override
    public String toString() {
        return ((lastName == null ? "" : lastName + " ") + (firstName == null ? "" : firstName)).trim();
    }
}
