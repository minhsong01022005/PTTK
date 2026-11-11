package gara.model.user;

import java.util.Date;

/** Lớp cha của các loại nhân viên. */
public abstract class Staff4 extends Member4 {
    private Date hireDate;
    private String position;

    public Date getHireDate() { return hireDate; }
    public void setHireDate(Date hireDate) { this.hireDate = hireDate; }
    public String getPosition() { return position; }
    public void setPosition(String position) { this.position = position; }
}
