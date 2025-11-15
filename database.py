# database.py
import mysql.connector
from mysql.connector import Error

# ==============================================
#  HÀM KẾT NỐI CƠ SỞ DỮ LIỆU
def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234567',
            database='tivi_store',
            charset='utf8mb4',  # để đọc ghi tiếng Việt chuẩn
            use_unicode=True
        )
        return connection
    except Error as e:
        print("❌ Lỗi kết nối MySQL:", e)
        return None


# ==============================================
#  HÀM ĐĂNG NHẬP - PHÂN QUYỀN NHÂN VIÊN
def dang_nhap(ten_dang_nhap, mat_khau):
    conn = get_connection()
    if conn is None:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM nhanvien WHERE TenDangNhap = %s AND MatKhau = %s"
        cursor.execute(query, (ten_dang_nhap, mat_khau))
        user = cursor.fetchone()
        return user  # trả về thông tin nhân viên (nếu có)
    except Error as e:
        print("❌ Lỗi khi đăng nhập:", e)
        return None
    finally:
        cursor.close()
        conn.close()


# ==============================================
#  HÀM LẤY DỮ LIỆU CHUNG (dành cho CRUD)
def fetch_all(query, params=None):
    conn = get_connection()
    if conn is None:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print("❌ Lỗi truy vấn:", e)
        return []
    finally:
        cursor.close()
        conn.close()


# ==============================================
#  HÀM THỰC HIỆN THÊM/SỬA/XÓA
def execute_query(query, params=None):
    conn = get_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        return True
    except Error as e:
        print("❌ Lỗi khi thực hiện truy vấn:", e)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


'''CREATE TABLE loai
(
	[MaLoai] NVARCHAR(50) NOT NULL PRIMARY KEY, 
    [TenLoai] NVARCHAR(MAX) NULL, 
    [Hangsx] NVARCHAR(MAX) NOT NULL
);
                CREATE TABLE sanpham
(
	[MaSP] NVARCHAR(50) NOT NULL PRIMARY KEY, 
    [TenSP] NVARCHAR(MAX) NOT NULL, 
    [Gia] FLOAT NOT NULL, 
    [SoLuong] INT NOT NULL, 
    [MaLoai] NVARCHAR(50) NOT NULL, 
    [Anh] NVARCHAR(MAX) NULL
);
                CREATE TABLE nhanvien
(
	[MaNV] NVARCHAR(50) NOT NULL PRIMARY KEY, 
    [TenNV] NVARCHAR(MAX) NOT NULL, 
    [GioiTinh] NVARCHAR(50) NOT NULL, 
    [DiaChi] NVARCHAR(MAX) NOT NULL, 
    [DienThoai] NVARCHAR(50) NOT NULL, 
    [NgaySinh] DATETIME NOT NULL
);
                CREATE TABLE khachhang
(
	[MaKhach] NVARCHAR(50) NOT NULL PRIMARY KEY, 
    [TenKhach] NVARCHAR(MAX) NOT NULL, 
    [DiaChi] NVARCHAR(MAX) NOT NULL, 
    [DienThoai] NVARCHAR(50) NOT NULL
);
                CREATE TABLE hoadon
(
	MaHD NVARCHAR(50) NOT NULL PRIMARY KEY, 
    MaNV NVARCHAR(50) NOT NULL, 
    MaKhach NVARCHAR(50) NOT NULL, 
    NgayBan DATETIME NOT NULL,
    FOREIGN KEY (MaNV) REFERENCES nhanvien(MaNV),
    FOREIGN KEY (MaKhach) REFERENCES khachhang(MaKhach)
);
                CREATE TABLE cthd
(
	MaHD NVARCHAR(50) NOT NULL , 
    MaSP NVARCHAR(50) NOT NULL, 
    SL INT NOT NULL, 
    DonGia FLOAT NOT NULL, 
    ThanhTien FLOAT NOT NULL, 
    PRIMARY KEY (MaHD, MaSP),
    FOREIGN KEY (MaSP) REFERENCES sanpham(MaSP),
    FOREIGN KEY (MaHD) REFERENCES hoadon(MaHD)
);
                CREATE TABLE khachhang
(
	MaKhach NVARCHAR(50) NOT NULL PRIMARY KEY, 
    TenKhach NVARCHAR(200) NOT NULL, 
    DiaChi NVARCHAR(200) NOT NULL, 
    DienThoai NVARCHAR(50) NOT NULL
);
                CREATE TABLE loai
(
	MaLoai NVARCHAR(50) NOT NULL PRIMARY KEY, 
    TenLoai NVARCHAR(200) NULL, 
    Hangsx NVARCHAR(200) NOT NULL
);
                CREATE TABLE nhanvien
(
	MaNV NVARCHAR(50) NOT NULL PRIMARY KEY, 
    TenNV NVARCHAR(200) NOT NULL, 
    GioiTinh NVARCHAR(50) NOT NULL, 
    DiaChi NVARCHAR(200) NOT NULL, 
    DienThoai NVARCHAR(50) NOT NULL, 
    NgaySinh DATETIME NOT NULL
);
                CREATE TABLE sanpham
(
	MaSP NVARCHAR(50) NOT NULL PRIMARY KEY, 
    TenSP NVARCHAR(200) NOT NULL, 
    Gia FLOAT NOT NULL, 
    SoLuong INT NOT NULL, 
    MaLoai NVARCHAR(50) NOT NULL, 
    Anh NVARCHAR(200) NULL,
    FOREIGN KEY (MaLoai) REFERENCES loai(MaLoai)
);






    """
    #Thêm dữ liệu
    cur.execute("SELECT COUNT(*) FROM tivi")
    if cur.fetchone()[0]==0:
        sample_data=[("Samsung Smart TV OLED QA55S85F","Samsung","55","30.190.000"),
                     ("Samsung Smart TV OLED QA65S85F","Samsung","65","42.590.000"),
                     ("Samsung Smart TV QLED QA65Q8F5","Samsung","65","16.490.000"),
                     ("Hinsense Smart TV QLED 32Q5S","Hinsense","32","4.490.000"),
                     ("LG Smart TV NanoCell 55 NANO80ASA","LG","55","14.390.000"),
                     ("LG Smart TV NanoCell 65 NANO80ASA","LG","65","15.990.000"),
                     ("Samsung Smart TV NeoQLED QA55QN70F","Samsung","55","19.000.000"),
                     ("TCL Google TV 55P635","TCL","55","7.990.000"),
                     ("TCL Google TV QD-MiniLED 65C6KS","TCL","65","14.990.000"),
                     ("Hinsense Smart TV 55U6Q","Hinsense","55","7.990.000"),
                     ("Hinsense Smart TV 58A6Q","Hinsense","58","8.690.000")]
        cur.executemany("INSERT INTO tivi (ten,hang,kich_thuoc,gia)VALUES(?,?,?,?)",sample_data)
    conn.commit()
    conn.close()

def insert_tivi(ten, hang, kich_thuoc, gia):
    conn = sqlite3.connect("tivi_store.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO tivi (ten, hang, kich_thuoc, gia) VALUES (?, ?, ?, ?)",
                (ten, hang, kich_thuoc, gia))
    conn.commit()
    conn.close()

def view_tivi():
    conn = sqlite3.connect("tivi_store.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM tivi")
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_tivi(id):
    conn = sqlite3.connect("tivi_store.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM tivi WHERE id=?", (id,))
    conn.commit()
    conn.close()

def update_tivi(id, ten, hang, kich_thuoc, gia):
    conn = sqlite3.connect("tivi_store.db")
    cur = conn.cursor()
    cur.execute("UPDATE tivi SET ten=?, hang=?, kich_thuoc=?, gia=? WHERE id=?",
                (ten, hang, kich_thuoc, gia, id))
    conn.commit()
    conn.close()

def search_tivi(keyword):
    conn = sqlite3.connect("tivi_store.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM tivi 
        WHERE ten LIKE ? OR hang LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%"))
    rows = cur.fetchall()
    conn.close()
    return rows'''

