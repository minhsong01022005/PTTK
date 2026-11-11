# GaraMan – Đề 26 (Phân tích thiết kế hệ thống thông tin)

Ứng dụng web J2EE theo mô hình **MVC: JSP + Servlet + JDBC + MySQL + DAO** cài đặt 2 module của hệ thống quản lý gara ô tô:

| Module | Tác nhân | Controller | Trang JSP |
|---|---|---|---|
| Nhập phụ tùng | Nhân viên kho | `ImportServlet` (`/import/*`) | `nvkho-home`, `chon-ncc`, `them-ncc`, `lap-hoa-don`, `chon-phu-tung`, `them-phu-tung`, `nhap-so-luong`, `in-hoa-don` |
| Tìm kiếm thông tin dịch vụ/phụ tùng | Khách hàng | `SearchServlet` (`/search`, `/search/detail`) | `customer-home`, `tim-kiem`, `chi-tiet` |

Kèm chức năng đăng nhập/đăng xuất (`LoginServlet`, `LogoutServlet`, `AuthFilter` phân quyền theo vai trò).

## Cấu trúc thư mục

```
PTTK/
├── pom.xml
├── sql/GaraManDB.sql                  tạo CSDL + dữ liệu mẫu
└── src/main
    ├── java/gara
    │   ├── model/{user,catalog,transaction}   JavaBean (lớp thực thể …4)
    │   ├── dao                                DAO (getConnection) + interface …DAO4
    │   ├── dao/impl                           …DAOImpl4 (JDBC)
    │   ├── controller                         Servlet + Filter
    │   └── util/PasswordUtil.java
    ├── resources/db.properties                cấu hình kết nối MySQL
    └── webapp
        ├── css/style.css
        └── WEB-INF/{web.xml, views/{common,inventory,customer}/*.jsp}
```

## Cách chạy

Yêu cầu: JDK 17, Maven 3.8+, MySQL 8, Apache Tomcat 9 (dùng `javax.servlet`; **không** dùng Tomcat 10+).

1. Tạo CSDL: `mysql -u root -p < sql/GaraManDB.sql`
2. Sửa `src/main/resources/db.properties` (user/password MySQL).
3. Đóng gói: `mvn clean package` → sinh `target/GaraMan.war`.
4. Chép `GaraMan.war` vào `<TOMCAT>/webapps/`, chạy Tomcat, mở `http://localhost:8080/GaraMan/`.
   (Hoặc trong Eclipse/IntelliJ: *Add project to Tomcat 9 server* rồi Run.)

Tài khoản mẫu:

| Vai trò | Tài khoản | Mật khẩu |
|---|---|---|
| Nhân viên kho | `kho01` | `kho123` |
| Khách hàng | `khach01` | `khach123` |

## Kịch bản thử nhanh

* **Nhập phụ tùng:** đăng nhập `kho01` → *Nhập phụ tùng* → tìm “NCC” → chọn *Công ty Phụ tùng Auto Vina* → *Thêm phụ tùng* → chọn *Lốp xe Michelin 17 inch* → SL `10`, đơn giá `1.950.000` → *Thêm* → *Xác nhận hóa đơn* (tồn kho PT101 tăng từ 5 lên 15).
* **Tìm kiếm:** đăng nhập `khach01` → *Tìm thông tin dịch vụ/phụ tùng* → từ khóa “Dầu” → chọn *Thay dầu động cơ*.

## Ghi chú thiết kế

* Tiền tệ lưu `DECIMAL(15,0)` (VNĐ), trong Java dùng `long`.
* Mật khẩu lưu dạng SHA-256; mọi câu SQL dùng `PreparedStatement`; mọi dữ liệu hiển thị qua `<c:out>` để tránh XSS.
* Lưu hóa đơn + dòng chi tiết + cộng dồn tồn kho nằm trong **một transaction** (`ImportInvoiceDAOImpl4`), lỗi thì rollback.
* Các thao tác POST đều redirect (Post-Redirect-Get) để tránh gửi lại form khi F5.
