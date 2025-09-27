import logging
import tkinter as tk

from config import DB_CONFIG, CAMERA_URL, OTP_LENGTH, SMS_API_KEY, SMS_SENDER, SMTP_USER, SMTP_APP_PASSWORD
from db_manager import DBManager
from otp import OTPManager
from notifier import Notifier
from scanner import BarcodeScanner
from student_auth import StudentAuth
from faculty_auth import FacultyAuth
from guest import GuestRegistration
from manual import ManualEntryWindow

logging.basicConfig(level=logging.INFO)


def main():
    db_manager = DBManager(DB_CONFIG)
    otp_manager = OTPManager(length=OTP_LENGTH)
    notifier = Notifier(SMS_API_KEY, SMS_SENDER, SMTP_USER, SMTP_APP_PASSWORD)
    scanner = BarcodeScanner(CAMERA_URL)

    student_flow = StudentAuth(db_manager, notifier, otp_manager, scanner)
    faculty_flow = FacultyAuth(db_manager, notifier, otp_manager, scanner)
    guest_flow = GuestRegistration(db_manager, notifier, otp_manager)
    manual_window = ManualEntryWindow(student_flow, faculty_flow)

    root = tk.Tk()
    root.title("E- Authentication")
    root.geometry("350x240")
    root.config(bg="cadet blue")
    tk.Label(root, text="WELCOME TO \n BHAVAN'S VIVEKANANDA COLLEGE", font=("Arial", 13), bg="cadet blue").place(x=15, y=20)

    tk.Button(root, text="Student", command=lambda: student_flow.read_from_camera()).place(x=45, y=100)
    tk.Button(root, text="Faculty", command=lambda: faculty_flow.read_from_camera()).place(x=125, y=100)
    tk.Button(root, text="Guest", command=lambda: guest_flow.launch_form()).place(x=205, y=100)
    tk.Button(root, text="Enter ID", command=lambda: manual_window.open()).place(x=280, y=100)

    root.mainloop()
    db_manager.close()


if __name__ == "__main__":
    main()