from tkinter import messagebox


def calculate_exam_mark(self):
    """Calculate the exam mark for the selected subject."""
    semester_name = self.sheet_var.get()
    subject_code = self.subject_code_entry.get()

    if not subject_code:
        messagebox.showerror("Error", "Please enter a Subject Code.")
        return

    exam_mark = self.semesters[semester_name].calculate_exam_mark(subject_code)

    self.update_treeview()
    if exam_mark is None:
        messagebox.showerror("Error", f"Subject {subject_code} not found.")
        self.update_treeview()
