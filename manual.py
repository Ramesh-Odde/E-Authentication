import tkinter as tk


class ManualEntryWindow:
    def __init__(self, student_auth, faculty_auth):
        self.student_auth = student_auth
        self.faculty_auth = faculty_auth
        self._window = None
        self._eid_entry = None

    def open(self):
        self._window = tk.Tk()
        self._window.title("E- Authentication")
        self._window.geometry("350x240")
        self._window.config(bg="cadet blue")
        tk.Label(self._window, text="WELCOME TO \n BHAVAN'S VIVEKANANDA COLLEGE", font=("Arial", 13),
                 bg="cadet blue").place(x=15, y=20)
        tk.Label(self._window, text="Enter Your ID", bg="cadet blue").place(x=30, y=100)
        self._eid_entry = tk.Entry(self._window, width=15)
        self._eid_entry.place(x=120, y=100)
        tk.Button(self._window, text="Fetch", command=self._on_fetch).place(x=130, y=150)
        self._window.mainloop()

    def _on_fetch(self):
        eid = self._eid_entry.get().strip()
        if not eid:
            return
        self._window.destroy()
        if eid[:1].isdigit():
            self.student_auth.retrieve_by_key(eid)
        else:
            self.faculty_auth.retrieve_by_key(eid)
