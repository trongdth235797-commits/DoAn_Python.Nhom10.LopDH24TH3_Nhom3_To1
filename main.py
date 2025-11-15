from tkinter import *
from tkinter import messagebox
from login_view import login
def main_view(user=None):
    if user is None:
        user = {"TenNV": "Admin", "TenDangNhap": "admin"}
    root = Tk()
    root.title("QUẢN LÝ CỬA HÀNG TIVI")
    root.geometry("900x600")
    root.configure(bg="#f1f8e9")

    Label(root, text=f"Xin chào, {user['TenNV']} ({user['TenDangNhap']})",
          font=("Times New Roman", 14, "bold"), bg="#c5e1a5", fg="#1b5e20", anchor="w").pack(fill=X)

    frame = Frame(root, bg="#f1f8e9")
    frame.pack(pady=20)

    def mo_quan_ly_san_pham():
        import sanpham
        sanpham.show()

    def mo_quan_ly_loai():
        import loai
        loai.show()

    def mo_quan_ly_khachhang():
        import khachhang
        khachhang.show()

    def mo_quan_ly_nhanvien():
        if user['TenDangNhap'] != 'admin':
            messagebox.showwarning("Cảnh báo", "Chỉ admin mới được quản lý nhân viên!")
            return
        import nhanvien
        nhanvien.show()

    def mo_hoa_don():
        import hoadon
        hoadon.show()

    def thoat():
        if messagebox.askyesno("Thoát", "Bạn có chắc chắn muốn thoát không?"):
            root.destroy()

    buttons = [
        ("📺 Quản lý sản phẩm", mo_quan_ly_san_pham),
        ("📂 Quản lý loại", mo_quan_ly_loai),
        ("👥 Quản lý khách hàng", mo_quan_ly_khachhang),
        ("🧑‍💼 Quản lý nhân viên", mo_quan_ly_nhanvien),
        ("🧾 Quản lý hóa đơn", mo_hoa_don),
        ("🚪 Thoát", thoat)
    ]

    for i, (text, cmd) in enumerate(buttons):
        Button(frame, text=text, font=("Times New Roman", 14, "bold"),
               bg="#81c784", fg="black", width=25, height=2, command=cmd).grid(row=i, column=0, pady=10)

    root.mainloop()
if __name__ == "__main__":
    '''main_view()'''
    login()
