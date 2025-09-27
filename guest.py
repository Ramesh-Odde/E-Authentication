import datetime
import tkinter as tk
from tkinter import messagebox


class GuestRegistration:
    """Guest registration form and OTP verification."""

    def __init__(self, db, notifier, otp_manager):
        self.db = db
        self.notifier = notifier
        self.otp_manager = otp_manager
        self._root = None
        self._detail_window = None
        self._verify_window = None
        self.entry_name = None
        self.entry_email = None
        self.entry_mobile = None

    def launch_form(self):
        self._root = tk.Tk()
        self._root.geometry("500x500")
        self._root.title("Registration Form")
        tk.Label(self._root, text="Registration Form", width=25, font=("bold", 20)).place(x=60, y=20)

        tk.Label(self._root, text="FullName", width=20, font=("bold", 11)).place(x=40, y=100)
        self.entry_name = tk.Entry(self._root)
        self.entry_name.place(x=250, y=100)

        tk.Label(self._root, text="Email", width=20, font=("bold", 11)).place(x=28, y=150)
        self.entry_email = tk.Entry(self._root)
        self.entry_email.place(x=250, y=150)

        tk.Label(self._root, text="Contact Number", width=20, font=("bold", 11)).place(x=58, y=200)
        self.entry_mobile = tk.Entry(self._root)
        self.entry_mobile.place(x=250, y=200)

        tk.Button(self._root, text="submit", width=20, bg="brown", fg="white", command=self._on_submit).place(x=100, y=280)
        tk.Button(self._root, text="cancel", width=20, bg="brown", fg="white", command=self._root.destroy).place(x=280, y=280)

        self._root.mainloop()

    def _on_submit(self):
        name = self.entry_name.get().strip()
        email = self.entry_email.get().strip()
        mobile = self.entry_mobile.get().strip()
        if name and email and mobile:
            self._show_details_window(name, email, mobile)
        else:
            tk.Label(self._root, text="All details Required", width=20, font=("bold", 13)).place(x=135, y=250)

    def _show_details_window(self, name: str, email: str, mobile: str):
        self._detail_window = tk.Tk()
        self._detail_window.title("Details of Particular")
        self._detail_window.geometry("400x300")

        tk.Label(self._detail_window, text="Name").place(x=90, y=10)
        tk.Label(self._detail_window, text=name).place(x=190, y=10)

        tk.Label(self._detail_window, text="Mobile Number").place(x=90, y=40)
        tk.Label(self._detail_window, text=mobile).place(x=190, y=40)

        tk.Label(self._detail_window, text="Email").place(x=90, y=70)
        tk.Label(self._detail_window, text=email).place(x=190, y=70)

        tk.Button(self._detail_window, text="Send OTP", command=lambda: self._start_otp_flow(name, mobile, email)).place(x=120, y=200)
        tk.Button(self._detail_window, text="Cancel", command=self._detail_window.destroy).place(x=220, y=200)
        self._detail_window.mainloop()

    def _start_otp_flow(self, name: str, mobile: str, email: str):
        otp_value = self.otp_manager.get_otp()
        msg = f"hello, your otp is {otp_value}Regards, BVC"
        self.notifier.send_sms(mobile, msg)
        self.notifier.send_email(email, msg)

        self._verify_window = tk.Tk()
        self._verify_window.title("Verification")
        tk.Label(self._verify_window, text="Enter your OTP ").place(x=20, y=40)
        otp_entry = tk.Entry(self._verify_window, width=10)
        otp_entry.place(x=120, y=40)

        def verify_action():
            entered = otp_entry.get()
            if self.otp_manager.verify(entered):
                messagebox.showinfo("Authenticity", "You are authorized to enter")
                timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                insert_sql = "INSERT INTO guest VALUES (%s,%s,%s,%s)"
                self.db.cursor.execute(insert_sql, (name, mobile, email, timestamp))
                self.db.commit()
                self._verify_window.destroy()
            else:
                messagebox.showinfo("Authenticity", "Not Authorised")
                self._verify_window.destroy()

            self.otp_manager.regenerate()
            if self._root:
                self._root.destroy()
            if self._detail_window:
                self._detail_window.destroy()

        tk.Button(self._verify_window, text="Verify", command=verify_action).place(x=60, y=80)
        tk.Button(self._verify_window, text="Close", command=verify_action).place(x=120, y=80)
        self._verify_window.mainloop()
