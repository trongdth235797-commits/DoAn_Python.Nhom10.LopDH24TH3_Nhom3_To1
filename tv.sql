-- Chú ý: KHÔNG CHẠY PHẦN CODE PYTHON/SQLITE NẰM NGOÀI KHỐI LỆNH NÀY!

-- 1. Tạo CSDL và sử dụng
CREATE DATABASE IF NOT EXISTS tivi_store CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE tivi_store;
CREATE TABLE loai (
    MaLoai VARCHAR(50) NOT NULL PRIMARY KEY,
    TenLoai VARCHAR(200) NOT NULL,
    Hangsx VARCHAR(200) NOT NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE sanpham (
    MaSP VARCHAR(50) NOT NULL PRIMARY KEY,
    TenSP VARCHAR(200) NOT NULL,
    Gia DECIMAL(18,2) NOT NULL,
    SoLuong INT NOT NULL,
    MaLoai VARCHAR(50) NOT NULL,
    FOREIGN KEY (MaLoai) REFERENCES loai(MaLoai)
        ON DELETE CASCADE ON UPDATE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE khachhang (
    MaKhach VARCHAR(50) NOT NULL PRIMARY KEY,
    TenKhach VARCHAR(200) NOT NULL,
    DiaChi VARCHAR(200),
    DienThoai VARCHAR(50)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE nhanvien (
    MaNV VARCHAR(50) NOT NULL PRIMARY KEY,
    TenNV VARCHAR(200) NOT NULL,
    GioiTinh VARCHAR(50),
    DiaChi VARCHAR(200),
    DienThoai VARCHAR(50),
    NgaySinh DATETIME,
    TenDangNhap VARCHAR(50) UNIQUE NOT NULL,
    MatKhau VARCHAR(200) NOT NULL,
    VaiTro ENUM('Quan Ly', 'Nhân viên') NOT NULL DEFAULT 'Nhân viên'
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE hoadon (
    MaHD VARCHAR(50) NOT NULL PRIMARY KEY,
    MaNV VARCHAR(50) NOT NULL,
    MaKhach VARCHAR(50) NOT NULL,
    NgayBan DATETIME NOT NULL,
    FOREIGN KEY (MaNV) REFERENCES nhanvien(MaNV)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (MaKhach) REFERENCES khachhang(MaKhach)
        ON DELETE CASCADE ON UPDATE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE cthd (
    MaHD VARCHAR(50) NOT NULL,
    MaSP VARCHAR(50) NOT NULL,
    SL INT NOT NULL,
    DonGia DECIMAL(18,2) NOT NULL,
    ThanhTien DECIMAL(18,2) NOT NULL,
    PRIMARY KEY (MaHD, MaSP),
    FOREIGN KEY (MaHD) REFERENCES hoadon(MaHD)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (MaSP) REFERENCES sanpham(MaSP)
        ON DELETE CASCADE ON UPDATE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

INSERT INTO loai VALUES
('L01', 'OLED', 'Samsung'),
('L02', 'QLED TV', 'Hinsense'),
('L03', 'QLED TV', 'Samsung'),
('L04', 'NanoCell', 'LG'),
('L05', 'MiniLED', 'Samsung'),
('L06', 'MiniLED', 'TCL'),
('L07', 'ULED', 'Hinsense');

INSERT INTO sanpham VALUES
('SP01','Samsung Smart TV OLED',30190000,10,'L01'),
('SP02','Samsung Smart TV OLED',42590000,9,'L01'),
('SP03','Samsung Smart TV QLED',16490000,9,'L03'),
('SP04','Hinsense Smart TV QLED',4490000,8,'L02'),
('SP05','LG Smart TV NanoCell 55',14390000,8,'L04'),
('SP06','LG Smart TV NanoCell 65',15990000,6,'L04'),
('SP07','Samsung Smart TV NeoQLED',19000000,5,'L05'),
('SP08','TCL Google TV',7990000,4,'L06'),
('SP09','TCL Google TV QD-MiniLED',14990000,3,'L06'),
('SP010','Hinsense Smart TV ',7990000,3,'L07'),
('SP011','Hinsense Smart TV ',8690000,2,'L07');


                     
                     
INSERT INTO khachhang VALUES
('KH001', 'Nguyễn Văn A', '123 Lê Lợi, Đà Nẵng', '0905123456'),
('KH002', 'Trần Thị B', '56 Nguyễn Văn Linh, Huế', '0906789123'),
('KH003', 'Phạm Minh C', '24 Nguyễn Huệ, Hà Nội', '0909123456');

INSERT INTO nhanvien VALUES
('NV01', 'NV01', 'Nam', '45 Hoàng Diệu, Đà Nẵng', '0905345678', '2005-03-15','nv01','123456','Nhân viên'),
('NV02', 'Nguyễn Ngọc Thảo', 'Nữ', '78 Trưng Nữ Vương, Huế', '0906789123', '2005-07-20','admin','1234567','Quan Ly'),
('NV03', 'Phạm Đức Anh', 'Nam', '12 Nguyễn Văn Cừ, Hà Nội', '0901234567', '2000-09-10','nv03','123456','Nhân viên');

INSERT INTO hoadon VALUES
('HD01', 'NV01', 'KH001', '2025-10-01'),
('HD02', 'NV02', 'KH003', '2025-11-01'),
('HD03', 'NV03', 'KH002', '2025-11-02');

INSERT INTO cthd VALUES
('HD01', 'SP01', 1, 30190000, 30190000),
('HD01', 'SP04', 2, 4490000, 8980000),
('HD02', 'SP02', 1, 42590000, 42590000),
('HD03', 'SP05', 3, 14390000, 43170000);