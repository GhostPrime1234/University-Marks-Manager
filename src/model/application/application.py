"""
This module contains the Application class which is responsible for managing the
user interface of the University Marks Manager application. It also includes the
ToolTip class for displaying tooltips when hovering over a Treeview cell.
"""

import tkinter as tk
from datetime import datetime

from controller import (
    add_entry,
    add_semester,
    add_total_mark,
    calculate_exam_mark,
    delete_entry,
    on_treeview_motion,
    on_treeview_select,
    on_window_resize,
    remove_semester,
    remove_subject,
    update_semester,
    update_semester_menu,
    update_treeview,
    update_year,
)
from controller.subject.subject_logic import (
    add_subject as add_subject_logic,  # Rename the import to avoid conflict
)
from view import (
    configure_styles,
    create_button_frames,
    create_entry_frame,
    create_main_frame,
    create_treeview,
)
from view import create_form_frame as create_form_func


class Application:
    """
    A class to represent the main application window for the University Marks Manager.
    This class is responsible for managing the user interface of the application,
    including adding, deleting, and calculating marks for subjects.

    Args:
        application_root (tk.Tk): The main application window.
        storage_handler (DataPersistence): An instance of the DataPersistence class.
        icon_path (str): The path to the icon file to be used for the application and dialogs.
    """

    def __init__(self, application_root: tk.Tk, storage_handler, icon_path: str):
        # Import DataPersistence and Semester locally to avoid circular import
        from model.semester.semester import Semester

        self.root = application_root
        self.data_persistence = storage_handler
        self.icon_path = icon_path  # Store the icon path
        self.semesters = {
            sem: Semester(sem, storage_handler.year, storage_handler)
            for sem in sorted(self.data_persistence.data.keys())
        }
        current_year = datetime.now().year
        self.year_list = [str(year) for year in range(current_year - 2, current_year + 2, 1)]
        self.year_var = tk.StringVar()
        self.year_var.set(str(current_year))

        self.semester_menu = None

        default_sheet = None
        for sheet in sorted(self.data_persistence.data.keys()):
            subjects = self.data_persistence.data.get(sheet, {})
            if subjects:
                if all(not subj.get("Sync Source", False) for subj in subjects.values()):
                    default_sheet = sheet
                    break
            else:
                default_sheet = sheet
                break

        if default_sheet is None:
            default_sheet = sorted(self.data_persistence.data.keys())[0]

        # Create treeview widget
        self.main_frame = create_main_frame(self.root)
        self.create_treeview()

        self.sheet_var = tk.StringVar(value=default_sheet)
        self.sync_source_var = tk.BooleanVar()
        self.current_tooltip = None  # Initialize current_tooltip to None

        self.setup_gui()
        self.root.bind("<Configure>", self.on_window_resize)

    def setup_gui(self):
        self.root.title("University Marks Manager")
        self.root.geometry("1850x800")

        configure_styles(self.root)
        self.create_form_frame()
        self.create_entry_frame()
        self.create_button_frames()
        self.bind_events()
        self.configure_grid()

        self.update_semester()

        # Set the application icon
        self.root.iconbitmap(self.icon_path)

    def create_form_frame(self):
        create_form_func(
            self,
            main_frame=self.main_frame,
            sheet_var=self.sheet_var,
            year_var=self.year_var,
            semesters=self.semesters,
            year_list=self.year_list,
            update_year=self.update_year,
            update_semester=self.update_semester,
        )
        # self.update_semester_menu()  # Call update_semester_menu after creating the form frame

    def create_treeview(self):
        self.treeview = create_treeview(self.main_frame)

    def create_entry_frame(self):
        self.subject_name_entry = None
        create_entry_frame(main_frame=self.main_frame, application_self=self)

    def create_button_frames(self):
        create_button_frames(
            main_frame=self.main_frame,
            add_subject_func=self.add_subject,
            remove_subject_func=self.remove_subject,
            add_semester_func=self.add_semester,
            remove_semester_func=self.remove_semester,
            add_entry_func=self.add_entry,
            delete_entry_func=self.delete_entry,
            calculate_exam_mark_func=self.calculate_exam_mark,
            add_total_mark_func=self.add_total_mark,
        )

    def bind_events(self):
        self.treeview.bind("<Motion>", lambda event: on_treeview_motion(self, event))
        self.treeview.bind("<<TreeviewSelect>>", lambda event: on_treeview_select(self, event))

    def configure_grid(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

    def update_year(self, event=None):
        update_year(self, event)
        # self.update_semester_menu()  # Update the semester menu after changing the year

    def update_semester(self, event=None):
        update_semester(self, event)
        # update_semester_menu(self)

    def add_semester(self):
        add_semester(self)
        self.update_semester_menu()  # Update the semester menu after adding a semester

    def remove_semester(self):
        remove_semester(self)
        self.update_semester_menu()  # Update the semester menu after removing a semester

    def update_semester_menu(self):
        update_semester_menu(self)

    def add_subject(self):
        # Open the AddSubjectDialog
        add_subject_logic(self)  # Use the renamed import

    def remove_subject(self):
        remove_subject(self)

    def add_entry(self):
        add_entry(self)

    def delete_entry(self):
        delete_entry(self)

    def calculate_exam_mark(self):
        calculate_exam_mark(self)

    def add_total_mark(self):
        add_total_mark(self)

    def update_treeview(self):
        update_treeview(self)

    def on_treeview_select(self, event):
        on_treeview_select(self, event)

    def on_treeview_motion(self, event):
        on_treeview_motion(self, event)

    def on_window_resize(self, event):
        on_window_resize(self, event)
