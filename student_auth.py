from base_auth import BaseAuthWindow
from models import PersonRecord


class StudentAuth(BaseAuthWindow):
    """Student authentication flow: camera scanning and manual lookup.

    Responsibilities:
    - Read barcode from camera (via injected scanner)
    - Retrieve student record by admission number and show OTP/UI flow
    """

    def __init__(self, db, notifier, otp_manager, scanner):
        super().__init__(db, notifier, otp_manager)
        self.scanner = scanner

    def read_from_camera(self):
        """Start camera scanning and process the first decoded barcode."""
        decoded = self.scanner.scan()
        if decoded:
            self.retrieve_by_key(decoded)

    def retrieve_by_key(self, admission_no: str):
        """Fetch a student record from DB and display it.

        The DB column indexes are kept consistent with the original application to avoid logic changes.
        """
        select_sql = "SELECT * FROM student WHERE AdmNo = %s;"
        self.db.cursor.execute(select_sql, (admission_no,))
        rows = self.db.cursor.fetchall()
        if rows:
            row = rows[0]
            record = PersonRecord(
                id_value=admission_no,
                name=str(row[3]),
                phone=str(row[7]),
                email=str(row[6]),
                extra1=str(row[2]),  # roll no
                extra2=str(row[5]),  # course
            )
            self._show_person_record(record)
        else:
            from tkinter import messagebox
            messagebox.showinfo("Authenticity", "Details Not Found")
