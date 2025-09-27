import datetime
import tkinter as tk
from tkinter import messagebox
from typing import Optional
from models import PersonRecord

class BaseAuthWindow:
    def __init__(self, db, notifier, otp_manager):
        self.db = db
        self.notifier = notifier
        self.otp_manager = otp_manager
        self._info_window: Optional[tk.Tk] = None
        self._verify_window: Optional[tk.Tk] = None

    def _open_info_window(self, title: str = "Details", geometry: str = "400x300"):
        self._info_window = tk.Tk()
        self._info_window.title(title)
        self._info_window.geometry(geometry)


    def _show_person_record(self, record: PersonRecord):
        self._open_info_window("Details of Particular", "400x300")
        tk.Label(self._info_window, text="Name").place(x=90, y=10)
        tk.Label(self._info_window, text=record.name).place(x=190, y=10)


        tk.Label(self._info_window, text="Mobile Number").place(x=90, y=100)
        tk.Label(self._info_window, text=record.phone).place(x=190, y=100)


        tk.Label(self._info_window, text="Email").place(x=90, y=130)
        tk.Label(self._info_window, text=record.email).place(x=190, y=130)


        if record.extra1:
            tk.Label(self._info_window, text="Extra1").place(x=90, y=40)
            tk.Label(self._info_window, text=record.extra1).place(x=190, y=40)
        if record.extra2:
            tk.Label(self._info_window, text="Extra2").place(x=90, y=70)
            tk.Label(self._info_window, text=record.extra2).place(x=190, y=70)


        tk.Button(self._info_window, text="Send OTP", command=lambda: self._start_otp_flow(record)).place(x=120, y=200)
        tk.Button(self._info_window, text="Cancel", command=self._cancel_info).place(x=220, y=200)
        self._info_window.mainloop()

    def _cancel_info(self):
        if self._info_window:
            self._info_window.destroy()

    def _start_otp_flow(self, record: PersonRecord):
        otp_value = self.otp_manager.get_otp()
        msg = f"Hello, \nYour otp to enter the College is {otp_value} \nRegards, BVC"
        self.notifier.send_sms(record.phone, msg)
        self.notifier.send_email(record.email, msg)


        self._verify_window = tk.Tk()
        self._verify_window.title("Verification")
        tk.Label(self._verify_window, text="Enter your OTP ").place(x=20, y=40)
        otp_entry = tk.Entry(self._verify_window, width=10)
        otp_entry.place(x=120, y=40)


        def verify_action():
            entered = otp_entry.get()
            if self.otp_manager.verify(entered):
                timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                insert_sql = "INSERT INTO resultset VALUES (%s,%s,%s,%s,%s);"
                self.db.cursor.execute(insert_sql, (record.id_value, record.name, record.phone, record.email, timestamp))
                self.db.commit()
                messagebox.showinfo("Authenticity", "You are authorized to enter")
                self._verify_window.destroy()
            else:
                messagebox.showinfo("Authenticity", "Not Authorised")
                self._verify_window.destroy()


            self.otp_manager.regenerate()
            if self._info_window:
                self._info_window.destroy()

        tk.Button(self._verify_window, text="Verify", command=verify_action).place(x=60, y=80)
        tk.Button(self._verify_window, text="Close", command=verify_action).place(x=120, y=80)
        self._verify_window.mainloop()