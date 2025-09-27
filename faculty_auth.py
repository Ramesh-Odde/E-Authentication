from base_auth import BaseAuthWindow
from models import PersonRecord


class FacultyAuth(BaseAuthWindow):
    """Faculty authentication flow: camera scanning and manual lookup."""

    def __init__(self, db, notifier, otp_manager, scanner):
        super().__init__(db, notifier, otp_manager)
        self.scanner = scanner

    def read_from_camera(self):
        decoded = self.scanner.scan()
        if decoded:
            self.retrieve_by_key(decoded)

    def retrieve_by_key(self, emp_id: str):
        select_sql = "SELECT * FROM Faculty WHERE EmpID = %s;"
        self.db.cursor.execute(select_sql, (emp_id,))
        rows = self.db.cursor.fetchall()
        if rows:
            row = rows[0]
            record = PersonRecord(
                id_value=emp_id,
                name=str(row[2]),
                phone=str(row[5]),
                email=str(row[6]),
                extra1=str(row[3]),  # department
                extra2=str(row[4]),  # designation
            )
            self._show_person_record(record)
        else:
            from tkinter import messagebox
            messagebox.showinfo("Authenticity", "Details Not Found")
