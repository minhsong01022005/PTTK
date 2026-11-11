package gara.model.user;

/** Nhân viên kỹ thuật. */
public class Technician4 extends Staff4 {
    private String specialty;

    public Technician4() { setRole("TECHNICIAN"); }

    public String getSpecialty() { return specialty; }
    public void setSpecialty(String specialty) { this.specialty = specialty; }
}
