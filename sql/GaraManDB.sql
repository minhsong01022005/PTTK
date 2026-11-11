-- =====================================================================
--  GaraMan - Đề 26: Hệ thống quản lý gara ô tô
--  CSDL MySQL 8.x (sinh từ sơ đồ lớp thực thể pha thiết kế)
--  Chạy:  mysql -u root -p < GaraManDB.sql
-- =====================================================================
DROP DATABASE IF EXISTS GaraManDB;
CREATE DATABASE GaraManDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE GaraManDB;

-- ---------------- Người dùng (kế thừa: Member4 -> Customer4 / Staff4 -> ...) ----------------
CREATE TABLE tblMember4 (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    username  VARCHAR(50)  NOT NULL UNIQUE,
    password  CHAR(64)     NOT NULL,                 -- SHA-256 (hex)
    firstName VARCHAR(50)  NOT NULL,
    lastName  VARCHAR(50)  NOT NULL,
    street    VARCHAR(150),
    city      VARCHAR(80),
    phone     VARCHAR(20),
    email     VARCHAR(100),
    role      ENUM('CUSTOMER','MANAGER','SALES','INVENTORY','TECHNICIAN') NOT NULL
) ENGINE=InnoDB;

CREATE TABLE tblCustomer4 (
    memberId INT PRIMARY KEY,
    customerLevel VARCHAR(30) DEFAULT 'Thường',
    FOREIGN KEY (memberId) REFERENCES tblMember4(id)
) ENGINE=InnoDB;

CREATE TABLE tblStaff4 (
    memberId  INT PRIMARY KEY,
    hireDate  DATE,
    position  VARCHAR(50),
    FOREIGN KEY (memberId) REFERENCES tblMember4(id)
) ENGINE=InnoDB;

CREATE TABLE tblManager4        (staffId INT PRIMARY KEY, managementLevel VARCHAR(30), FOREIGN KEY (staffId) REFERENCES tblStaff4(memberId)) ENGINE=InnoDB;
CREATE TABLE tblSalesStaff4     (staffId INT PRIMARY KEY, counterId VARCHAR(20), FOREIGN KEY (staffId) REFERENCES tblStaff4(memberId)) ENGINE=InnoDB;
CREATE TABLE tblInventoryStaff4 (staffId INT PRIMARY KEY, warehouseId VARCHAR(20), FOREIGN KEY (staffId) REFERENCES tblStaff4(memberId)) ENGINE=InnoDB;
CREATE TABLE tblTechnician4     (staffId INT PRIMARY KEY, specialty VARCHAR(50), FOREIGN KEY (staffId) REFERENCES tblStaff4(memberId)) ENGINE=InnoDB;

CREATE TABLE tblCar4 (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    plate      VARCHAR(20) NOT NULL,
    brand      VARCHAR(50),
    model      VARCHAR(50),
    customerId INT NOT NULL,
    FOREIGN KEY (customerId) REFERENCES tblCustomer4(memberId)
) ENGINE=InnoDB;

-- ---------------- Danh mục ----------------
CREATE TABLE tblSupplier4 (
    id      INT AUTO_INCREMENT PRIMARY KEY,
    code    VARCHAR(20)  NOT NULL UNIQUE,
    name    VARCHAR(150) NOT NULL,
    taxCode VARCHAR(20),
    phone   VARCHAR(20)  NOT NULL,
    email   VARCHAR(100),
    street  VARCHAR(150),
    city    VARCHAR(80)
) ENGINE=InnoDB;

CREATE TABLE tblService4 (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    code        VARCHAR(20)  NOT NULL UNIQUE,
    name        VARCHAR(150) NOT NULL,
    price       DECIMAL(15,0) NOT NULL CHECK (price >= 0),
    description TEXT
) ENGINE=InnoDB;

CREATE TABLE tblPart4 (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    code          VARCHAR(20)  NOT NULL UNIQUE,
    name          VARCHAR(150) NOT NULL,
    unitPrice     DECIMAL(15,0) NOT NULL CHECK (unitPrice >= 0),
    stockQuantity INT NOT NULL DEFAULT 0 CHECK (stockQuantity >= 0),
    description   TEXT
) ENGINE=InnoDB;

-- ---------------- Giao dịch ----------------
CREATE TABLE tblAppointment4 (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    appointmentTime DATETIME NOT NULL,
    content         VARCHAR(255),
    status          VARCHAR(20) NOT NULL DEFAULT 'NEW',
    customerId      INT NOT NULL,
    serviceId       INT NULL,
    FOREIGN KEY (customerId) REFERENCES tblCustomer4(memberId),
    FOREIGN KEY (serviceId)  REFERENCES tblService4(id)
) ENGINE=InnoDB;

CREATE TABLE tblImportInvoice4 (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    importDate       DATETIME NOT NULL,
    totalAmount      DECIMAL(15,0) NOT NULL,
    supplierId       INT NOT NULL,
    inventoryStaffId INT NOT NULL,
    FOREIGN KEY (supplierId)       REFERENCES tblSupplier4(id),
    FOREIGN KEY (inventoryStaffId) REFERENCES tblInventoryStaff4(staffId)
) ENGINE=InnoDB;

CREATE TABLE tblImportDetail4 (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    importInvoiceId INT NOT NULL,
    partId          INT NOT NULL,
    quantity        INT NOT NULL CHECK (quantity > 0),
    unitPrice       DECIMAL(15,0) NOT NULL CHECK (unitPrice > 0),
    FOREIGN KEY (importInvoiceId) REFERENCES tblImportInvoice4(id) ON DELETE CASCADE,
    FOREIGN KEY (partId)          REFERENCES tblPart4(id)
) ENGINE=InnoDB;

CREATE TABLE tblSalesInvoice4 (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    invoiceDate   DATETIME NOT NULL,
    totalAmount   DECIMAL(15,0) NOT NULL,
    paymentStatus VARCHAR(20) NOT NULL DEFAULT 'UNPAID',
    customerId    INT NOT NULL,
    salesStaffId  INT NOT NULL,
    carId         INT NOT NULL,
    FOREIGN KEY (customerId)   REFERENCES tblCustomer4(memberId),
    FOREIGN KEY (salesStaffId) REFERENCES tblSalesStaff4(staffId),
    FOREIGN KEY (carId)        REFERENCES tblCar4(id)
) ENGINE=InnoDB;

CREATE TABLE tblSalesDetailService4 (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    salesInvoiceId INT NOT NULL,
    serviceId      INT NOT NULL,
    technicianId   INT NULL,                          -- NULL cho tới khi được phân công
    price          DECIMAL(15,0) NOT NULL,
    FOREIGN KEY (salesInvoiceId) REFERENCES tblSalesInvoice4(id) ON DELETE CASCADE,
    FOREIGN KEY (serviceId)      REFERENCES tblService4(id),
    FOREIGN KEY (technicianId)   REFERENCES tblTechnician4(staffId)
) ENGINE=InnoDB;

CREATE TABLE tblSalesDetailPart4 (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    salesInvoiceId INT NOT NULL,
    partId         INT NOT NULL,
    quantity       INT NOT NULL CHECK (quantity > 0),
    unitPrice      DECIMAL(15,0) NOT NULL,
    FOREIGN KEY (salesInvoiceId) REFERENCES tblSalesInvoice4(id) ON DELETE CASCADE,
    FOREIGN KEY (partId)         REFERENCES tblPart4(id)
) ENGINE=InnoDB;

-- =====================================================================
--  DỮ LIỆU MẪU (khớp với kịch bản trong báo cáo)
--  Tài khoản:  kho01 / kho123  (nhân viên kho)   |  khach01 / khach123  (khách hàng)
-- =====================================================================
INSERT INTO tblMember4(username,password,firstName,lastName,street,city,phone,email,role) VALUES
 ('kho01',   SHA2('kho123',256),   'Song',  'Hoàng Minh', '96A Trần Phú',    'Hà Nội', '0912000111', 'song.kho@garaman.vn', 'INVENTORY'),
 ('khach01', SHA2('khach123',256), 'Hải',   'Nguyễn Văn', '12 Nguyễn Trãi',  'Hà Nội', '0934555666', 'hai.nv@gmail.com',    'CUSTOMER'),
 ('ql01',    SHA2('ql123',256),    'Lan',   'Trần Thị',   '5 Láng Hạ',       'Hà Nội', '0903777888', 'lan.ql@garaman.vn',   'MANAGER');

INSERT INTO tblCustomer4(memberId,customerLevel) SELECT id,'Thường' FROM tblMember4 WHERE role='CUSTOMER';
INSERT INTO tblStaff4(memberId,hireDate,position)
       SELECT id, '2024-03-01', role FROM tblMember4 WHERE role IN ('INVENTORY','MANAGER');
INSERT INTO tblInventoryStaff4(staffId,warehouseId) SELECT id,'KHO01' FROM tblMember4 WHERE role='INVENTORY';
INSERT INTO tblManager4(staffId,managementLevel) SELECT id,'Quản lý chung' FROM tblMember4 WHERE role='MANAGER';

INSERT INTO tblSupplier4(code,name,taxCode,phone,email,street,city) VALUES
 ('NCC01','Công ty Phụ tùng Auto Vina',  '0101234567','0988123456','sales@autovina.vn',   '25 Nguyễn Văn Linh', 'Hà Nội'),
 ('NCC02','Đại lý dầu nhớt Thành Phát',  '0309876543','0904987654','thanhphat@oil.vn',    '88 Lê Văn Việt',     'TP. Hồ Chí Minh'),
 ('NCC03','Công ty Lốp Michelin Việt Nam','0102468135','0977111222','contact@michelin.vn','Khu CN Quế Võ',      'Bắc Ninh');

INSERT INTO tblPart4(code,name,unitPrice,stockQuantity,description) VALUES
 ('PT101','Lốp xe Michelin 17 inch',   2000000,  5,'Lốp radial 225/50R17, chống mòn, êm ái, phù hợp sedan hạng C.'),
 ('PT105','Bình ắc quy GS 60Ah',       1250000, 12,'Ắc quy khô 12V-60Ah, bảo hành 12 tháng.'),
 ('PT203','Lọc dầu động cơ Toyota',     150000, 30,'Lọc dầu chính hãng cho Vios, Camry, Innova.'),
 ('PT03', 'Dầu Castrol 5W30',           380000, 40,'Dầu nhớt tổng hợp 5W-30, can 4 lít.'),
 ('PT204','Má phanh trước Bosch',       650000, 18,'Bộ má phanh đĩa trước, giảm tiếng ồn.');

INSERT INTO tblService4(code,name,price,description) VALUES
 ('DV01','Thay dầu động cơ',   500000,'Dịch vụ xả đáy dầu cũ, vệ sinh lọc dầu và thay mới dầu động cơ (tùy chọn loại dầu theo yêu cầu). Giúp động cơ vận hành êm ái, kéo dài tuổi thọ. Thời gian thực hiện dự kiến: 30 phút.'),
 ('DV02','Rửa xe và hút bụi',  120000,'Rửa ngoài, vệ sinh khoang nội thất, hút bụi thảm sàn và ghế. Thời gian dự kiến: 45 phút.'),
 ('DV03','Kiểm tra hệ thống phanh',300000,'Kiểm tra má phanh, đĩa phanh, dầu phanh và đường ống; cân chỉnh nếu cần. Thời gian dự kiến: 40 phút.'),
 ('DV04','Phủ ceramic',      4500000,'Phủ ceramic bảo vệ sơn, chống bám bẩn và tia UV. Thời gian dự kiến: 1 ngày.');

-- =====================================================================
--  DỮ LIỆU MẪU BỔ SUNG (nhiều bản ghi hơn để thử tìm kiếm / nhập hàng)
--  Tài khoản thêm: kho02/kho123, khach02..khach05/khach123
-- =====================================================================
INSERT INTO tblMember4(username,password,firstName,lastName,street,city,phone,email,role) VALUES
 ('kho02',   SHA2('kho123',256),   'Dũng',  'Phạm Quốc',   '14 Hoàng Quốc Việt', 'Hà Nội',          '0912333444', 'dung.kho@garaman.vn',  'INVENTORY'),
 ('khach02', SHA2('khach123',256), 'Linh',  'Phạm Thùy',   '56 Lê Lợi',          'Đà Nẵng',         '0935111000', 'linh.pt@gmail.com',    'CUSTOMER'),
 ('khach03', SHA2('khach123',256), 'Nam',   'Trần Hoài',   '102 Pasteur',        'TP. Hồ Chí Minh', '0908222111', 'nam.th@gmail.com',     'CUSTOMER'),
 ('khach04', SHA2('khach123',256), 'Hoa',   'Đặng Thu',    '9 Hàng Bài',         'Hà Nội',          '0966333222', 'hoa.dt@gmail.com',     'CUSTOMER'),
 ('khach05', SHA2('khach123',256), 'Khoa',  'Bùi Anh',     '77 Trần Hưng Đạo',   'Hải Phòng',       '0977444333', 'khoa.ba@gmail.com',    'CUSTOMER');

INSERT INTO tblCustomer4(memberId,customerLevel)
       SELECT id, CASE username WHEN 'khach03' THEN 'VIP' WHEN 'khach05' THEN 'Thân thiết' ELSE 'Thường' END
       FROM tblMember4 WHERE role='CUSTOMER' AND id NOT IN (SELECT memberId FROM tblCustomer4);
INSERT INTO tblStaff4(memberId,hireDate,position)
       SELECT id, '2024-06-15', role FROM tblMember4
       WHERE role='INVENTORY' AND id NOT IN (SELECT memberId FROM tblStaff4);
INSERT INTO tblInventoryStaff4(staffId,warehouseId) SELECT id,'KHO02' FROM tblMember4 WHERE username='kho02';

INSERT INTO tblSupplier4(code,name,taxCode,phone,email,street,city) VALUES
 ('NCC04','Công ty TNHH Bosch Việt Nam',        '0301122334','0283456789','bosch@bosch.vn',      '10 Tân Thuận',       'TP. Hồ Chí Minh'),
 ('NCC05','Nhà phân phối Castrol Miền Bắc',     '0105566778','0243111222','castrol.mb@oil.vn',   '120 Nguyễn Xiển',    'Hà Nội'),
 ('NCC06','Công ty Ắc quy GS Việt Nam',         '0106677889','0243222333','gs@acquy.vn',         '5 KCN Sài Đồng',     'Hà Nội'),
 ('NCC07','Công ty Phụ tùng Toyota Chính Hãng', '0107788990','0243555666','parts@toyota.vn',     '1 Phạm Hùng',        'Hà Nội'),
 ('NCC08','Đại lý Lốp Bridgestone Sài Gòn',     '0308899001','0287778889','bridgestone@lop.vn',  '33 Nguyễn Thị Thập', 'TP. Hồ Chí Minh'),
 ('NCC09','Công ty Đèn & Điện ô tô Philips',    '0109900112','0243888999','philips@auto.vn',     '18 Tố Hữu',          'Hà Nội'),
 ('NCC10','Công ty Phụ tùng Hòa Phát Auto',     '0110011223','0225333444','hoaphat.auto@hp.vn',  'KCN Đình Vũ',        'Hải Phòng');

INSERT INTO tblPart4(code,name,unitPrice,stockQuantity,description) VALUES
 ('PT102','Lốp xe Bridgestone 16 inch',    1650000, 14,'Lốp 205/55R16, bám đường tốt, phù hợp xe hạng B.'),
 ('PT103','Lốp xe Michelin 18 inch',       2800000,  6,'Lốp 235/50R18 cho SUV, độ bền cao, giảm ồn.'),
 ('PT104','Lốp xe Dunlop 15 inch',         1350000, 20,'Lốp 185/65R15 tiết kiệm nhiên liệu cho xe nhỏ.'),
 ('PT106','Bình ắc quy GS 45Ah',            980000, 15,'Ắc quy khô 12V-45Ah cho xe cỡ nhỏ, bảo hành 12 tháng.'),
 ('PT107','Bình ắc quy Varta 70Ah',        1850000,  8,'Ắc quy 12V-70Ah cho SUV, khởi động mạnh.'),
 ('PT201','Lọc gió động cơ Honda',          220000, 25,'Lọc gió chính hãng cho City, Civic, CR-V.'),
 ('PT202','Lọc gió điều hòa Bosch',         180000, 35,'Lọc than hoạt tính, khử mùi, lọc bụi mịn.'),
 ('PT205','Má phanh sau Bosch',             580000, 16,'Bộ má phanh sau, giảm tiếng ồn và mòn đĩa.'),
 ('PT206','Đĩa phanh trước Brembo',        1900000,  4,'Đĩa phanh thông gió, chịu nhiệt tốt.'),
 ('PT301','Bugi NGK Iridium',               210000, 60,'Bugi đầu iridium, tuổi thọ 100.000 km, giá bán lẻ/1 chiếc.'),
 ('PT302','Dây curoa cam Gates',            540000, 10,'Dây cam chính hãng Gates cho động cơ 1.5L.'),
 ('PT303','Bơm nước làm mát Aisin',         890000,  7,'Bơm nước Aisin cho Toyota Vios, Altis.'),
 ('PT304','Két nước làm mát Denso',        2350000,  3,'Két nước nhôm, tản nhiệt hiệu quả.'),
 ('PT305','Nước làm mát Prestone 4L',       260000, 28,'Dung dịch làm mát pha sẵn, chống ăn mòn.'),
 ('PT401','Dầu Castrol 10W40',              340000, 45,'Dầu nhớt bán tổng hợp 10W-40, can 4 lít.'),
 ('PT402','Dầu Shell Helix 0W20',           450000, 22,'Dầu nhớt tổng hợp 0W-20 tiết kiệm nhiên liệu, can 4 lít.'),
 ('PT403','Dầu hộp số ATF Toyota',          320000, 18,'Dầu hộp số tự động ATF WS, can 1 lít.'),
 ('PT404','Dầu phanh DOT4 Bosch',            95000, 50,'Dầu phanh DOT4, can 500ml.'),
 ('PT501','Đèn pha LED Philips H4',        1200000,  9,'Bóng đèn pha LED H4, sáng trắng 6000K.'),
 ('PT502','Bóng đèn hậu Osram',              85000, 40,'Bóng đèn hậu/phanh 12V 21/5W.'),
 ('PT503','Gạt mưa Bosch Aerotwin 24 inch', 190000, 30,'Cần gạt mưa không khung, êm và sạch kính.'),
 ('PT601','Giảm xóc trước KYB',            1450000,  6,'Giảm xóc dầu KYB Excel-G, giá/1 chiếc.'),
 ('PT602','Rotuyn cân bằng Toyota',         260000, 12,'Rotuyn cân bằng trước chính hãng.'),
 ('PT603','Cao su chân máy',                780000,  5,'Cao su chân máy giảm rung, chính hãng.');

INSERT INTO tblService4(code,name,price,description) VALUES
 ('DV05','Bảo dưỡng định kỳ 10.000 km',  1200000,'Thay dầu, lọc dầu, lọc gió, kiểm tra tổng quát 30 hạng mục. Thời gian dự kiến: 2 giờ.'),
 ('DV06','Cân chỉnh thước lái',            350000,'Cân chỉnh góc đặt bánh xe (độ chụm, camber) bằng máy 3D. Thời gian dự kiến: 45 phút.'),
 ('DV07','Cân bằng động lốp',              200000,'Cân bằng động 4 bánh, khắc phục rung vô lăng ở tốc độ cao. Thời gian dự kiến: 30 phút.'),
 ('DV08','Vá lốp / thay lốp',              150000,'Vá lốp không săm hoặc thay lốp mới (chưa gồm tiền lốp). Thời gian dự kiến: 30 phút.'),
 ('DV09','Kiểm tra và nạp gas điều hòa',   450000,'Kiểm tra rò rỉ, nạp gas R134a, vệ sinh dàn lạnh. Thời gian dự kiến: 1 giờ.'),
 ('DV10','Vệ sinh khoang máy',             250000,'Rửa và bảo dưỡng khoang máy, phủ dưỡng nhựa, chống chuột. Thời gian dự kiến: 40 phút.'),
 ('DV11','Thay ắc quy',                    150000,'Tháo lắp, kiểm tra hệ thống sạc, đo dòng rò (chưa gồm tiền ắc quy). Thời gian dự kiến: 20 phút.'),
 ('DV12','Đánh bóng và phục hồi sơn',     1800000,'Đánh bóng xóa xước nhẹ, phục hồi độ bóng lớp sơn. Thời gian dự kiến: 4 giờ.'),
 ('DV13','Chẩn đoán lỗi bằng máy OBD',     300000,'Đọc và xóa lỗi, đánh giá hệ thống điện - động cơ bằng máy chẩn đoán. Thời gian dự kiến: 40 phút.'),
 ('DV14','Dán phim cách nhiệt',           3500000,'Dán phim cách nhiệt chính hãng toàn xe, chống tia UV, bảo hành 5 năm. Thời gian dự kiến: 5 giờ.');

-- Hóa đơn nhập mẫu
INSERT INTO tblImportInvoice4(importDate,totalAmount,supplierId,inventoryStaffId) VALUES
 ('2026-09-05 09:30:00', 0, (SELECT id FROM tblSupplier4 WHERE code='NCC01'), (SELECT id FROM tblMember4 WHERE username='kho01')),
 ('2026-09-18 14:10:00', 0, (SELECT id FROM tblSupplier4 WHERE code='NCC05'), (SELECT id FROM tblMember4 WHERE username='kho01')),
 ('2026-10-02 10:00:00', 0, (SELECT id FROM tblSupplier4 WHERE code='NCC03'), (SELECT id FROM tblMember4 WHERE username='kho02')),
 ('2026-10-20 15:45:00', 0, (SELECT id FROM tblSupplier4 WHERE code='NCC06'), (SELECT id FROM tblMember4 WHERE username='kho02'));

INSERT INTO tblImportDetail4(importInvoiceId,partId,quantity,unitPrice)
SELECT (SELECT id FROM tblImportInvoice4 WHERE importDate=d), (SELECT id FROM tblPart4 WHERE code=c), q, p FROM (
  SELECT '2026-09-05 09:30:00' d,'PT203' c,20 q,120000 p UNION ALL
  SELECT '2026-09-05 09:30:00','PT204',10,520000 UNION ALL
  SELECT '2026-09-05 09:30:00','PT201',15,170000 UNION ALL
  SELECT '2026-09-18 14:10:00','PT03', 30,300000 UNION ALL
  SELECT '2026-09-18 14:10:00','PT401',30,270000 UNION ALL
  SELECT '2026-10-02 10:00:00','PT101',10,1600000 UNION ALL
  SELECT '2026-10-02 10:00:00','PT103', 6,2300000 UNION ALL
  SELECT '2026-10-20 15:45:00','PT105',10,1000000 UNION ALL
  SELECT '2026-10-20 15:45:00','PT106',10,780000) t;

UPDATE tblImportInvoice4 i
   SET totalAmount = (SELECT COALESCE(SUM(quantity*unitPrice),0) FROM tblImportDetail4 WHERE importInvoiceId=i.id)
 WHERE totalAmount = 0;
