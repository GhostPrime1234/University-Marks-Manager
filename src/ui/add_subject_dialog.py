from tkinter import simpledialog

import customtkinter as ctk


class AddSubjectDialog(simpledialog.Dialog):
    def __init__(self, parent, icon_path=None):
        self.icon_path = icon_path
        self.subject_code = None
        self.subject_name = None
        super().__init__(parent, title="Add Subject")

    def body(self, master):
        # Set the icon for the dialog
        if self.icon_path:
            self.iconbitmap(self.icon_path)

        button_frame = ctk.CTkFrame(master, fg_color="#0D1B2A")
        button_frame.grid(row=0, column=0, columnspan=2, pady=(10, 0), sticky="ew")
        # UI Elements
        ctk.CTkLabel(button_frame, text="Subject Code:").grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        self.entry_code = ctk.CTkEntry(button_frame, fg_color="#0D1B2A")
        self.entry_code.grid(row=0, column=1, padx=10, pady=(10, 5), sticky="ew")

        ctk.CTkLabel(button_frame, text="Subject Name:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_name = ctk.CTkEntry(button_frame, fg_color="#0D1B2A")
        self.entry_name.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        return self.entry_code  # initial focus

    def apply(self):
        self.subject_code = self.entry_code.get().strip() or None
        self.subject_name = self.entry_name.get().strip() or None


def ask_add_subject(parent, icon_path=None):
    dialog = AddSubjectDialog(parent, icon_path)
    return dialog.subject_code, dialog.subject_name
