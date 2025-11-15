from tkinter import *
from tkinter import messagebox

import mysql.connector

from database import dang_nhap
'''import main_launcher
import main'''

# ==============================
# 🧩 Giao diện đăng nhập
# ==============================
def login():
    root = Tk()
    root.title("Đăng nhập hệ thống quản lý Tivi")
    root.geometry("400x250")
    root.configure(bg="#e3f2fd")

    Label(root, text="ĐĂNG NHẬP HỆ THỐNG", font=("Times New Roman", 16, "bold"), bg="#e3f2fd", fg="#0d47a1").pack(pady=15)

    frame = Frame(root, bg="#e3f2fd")
    frame.pack(pady=10)

    Label(frame, text="Tên đăng nhập:", font=("Times New Roman", 12), bg="#e3f2fd").grid(row=0, column=0, padx=5, pady=5, sticky=E)
    username_entry = Entry(frame, font=("Times New Roman", 12))
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    Label(frame, text="Mật khẩu:", font=("Times New Roman", 12), bg="#e3f2fd").grid(row=1, column=0, padx=5, pady=5, sticky=E)
    password_entry = Entry(frame, font=("Times New Roman", 12), show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    def xu_ly_dang_nhap():
        ten = username_entry.get().strip()
        mk = password_entry.get().strip()

        if not ten or not mk:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu!")
            return

        user = dang_nhap(ten, mk)
        if user:
            messagebox.showinfo("Thành công", f"Xin chào {user['TenNV']}!")
            import main
            root.destroy()  # đóng cửa sổ đăng nhập
            main.main_view(user)  # mở giao diện chính
        else:
            messagebox.showerror("Lỗi đăng nhập", "Sai tên đăng nhập hoặc mật khẩu!")

    Button(root, text="Đăng nhập", font=("Times New Roman", 12, "bold"), bg="#1976d2", fg="white",
           width=12, command=xu_ly_dang_nhap).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    login()