"""
This module contains the Application class which is responsible for managing the 
user interface of the University Marks Manager application. It also includes the
ToolTip class for displaying tooltips when hovering over a Treeview cell.
"""
from datetime import datetime
from tkinter import messagebox, ttk
import tkinter as tk
from data_persistence import DataPersistence
from semester import Semester


class ToolTip:
    """
    A class to represent a tooltip for displaying 
    additional information when hovering over a widget.
    
    Args:
        widget (tk.Widget): The widget to which the tooltip is attached.
        text (str): The text to be displayed in the tooltip.
        tip_window (tk.Toplevel): The tooltip window to display the text.
    """
    def __init__(self, widget: tk.Widget, text: str):
        """
        Constructs all the necessary attributes for the tooltip window.
        
        Args:
            widget (tk.Widget): The widget to which the tooltip is attached.
            text (str): The text to be displayed in the tooltip.
        """
        self.widget = widget
        self.text = text
        self.tip_window = None

    def show_tip(self, event: tk.Event):
        """
        Displays the tooltip window with the specified text.

        Args:
            event (tk.Event): The event that triggered the tooltip display.
        """
        if self.tip_window or not self.text:
            return
        x = event.x_root + 10
        y = event.y_root + 10
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="yellow", relief=tk.SOLID, borderwidth=1)
        label.pack(ipadx=1)

    def hide_tip(self, _event):
        """
        Hides the tooltip window when the mouse leaves the widget.
        
        Args:
            _event (tk.Event): The event that triggered the tooltip hide action."""
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None


class Application:
    """
    A class to represent the main application window for the University Marks Manager.
    This class is responsible for managing the user interface of the application,
    including adding, deleting, and calculating marks for subjects.
    
    Args:
        application_root (tk.Tk): The main application window.
        storage_handler (DataPersistence): An instance of the DataPersistence class.
    """
    def __init__(self, application_root: tk.Tk, storage_handler: DataPersistence):
        self.root = application_root
        self.data_persistence = storage_handler
        self.semesters = {
            sem: Semester(sem, storage_handler.year, storage_handler)
            for sem in ["Autumn", "Spring", "Annual"]
        }

        current_year = datetime.now().year
        self.year_list = [str(year) for year in range(current_year - 2, current_year + 2, 1)]

        self.year_var = tk.StringVar()
        self.year_var.set(str(current_year))  # This sets the default year to current_year
        print(f"Current year in init: {datetime.now().year}")

        self.sheet_var = tk.StringVar()
        self.sheet_var.set("Autumn")

        # Initialise current tooltip to None
        self.current_tooltip = None
        print(current_year)

        self.setup_gui()

        self.root.bind("<Configure>", self.on_window_resize)

    def setup_gui(self):
        self.root.title("University Marks Manager")
        self.root.geometry("1500x900")

        style = ttk.Style(self.root)
        style.theme_use("clam")  # Start with the 'clam' theme and customize it

        # Customize the styles for dark mode
        dark_bg = "#2e2e2e"
        dark_fg = "#ffffff"
        accent_color = "#0078D7"

        style.configure("TFrame", background=dark_bg)
        style.configure("TLabel", background=dark_bg, foreground=dark_fg, font=("Helvetica", 12))
        style.configure("TButton", background=accent_color, foreground=dark_fg, font=("Helvetica", 12))
        style.configure("Treeview", background=dark_bg, foreground=dark_fg, fieldbackground=dark_bg)
        style.configure("Treeview.Heading", background=accent_color, foreground=dark_fg)

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        form_frame = ttk.Frame(main_frame)
        form_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        sheet_label = ttk.Label(form_frame, text="Select Semester:")
        sheet_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        sheet_menu = ttk.OptionMenu(form_frame, self.sheet_var, list(self.semesters.keys())[0], *list(self.semesters.keys()), command=self.update_semester)
        print(f"Semesters: {self.semesters.keys()}")
        sheet_menu.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        year_label = ttk.Label(form_frame, text="Select Year:")
        year_label.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

        # Set the year_var to the current year
        current_year = datetime.now().year
        self.year_var.set(str(current_year))

        year_menu = ttk.OptionMenu(form_frame, self.year_var, current_year, *self.year_list, command=self.update_year)
        year_menu.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)

        self.treeview = ttk.Treeview(main_frame, columns=("Subject Code", "Subject Name", "Subject Assessment", "Unweighted Mark",
                                                          "Weighted Mark", "Mark Weight", "Total Mark"),
                                     show="headings", height=15)
        self.treeview.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        headings = {
            "Subject Code": "Subject Code",
            "Subject Name": "Subject Name",
            "Subject Assessment": "Subject Assessment",
            "Unweighted Mark": "Mark (Out of Full Score)",
            "Weighted Mark": "Weighted Contribution (%)",
            "Mark Weight": "Assessment Weight (e.g., 30%)",
            "Total Mark": "Total Mark"
        }

        for col, description in headings.items():
            self.treeview.heading(col, text=description)
            self.treeview.column(col, anchor=tk.CENTER)

        entry_frame = ttk.Frame(main_frame)
        entry_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        fields = [
            ("Subject Code", "subject_code_entry"),
            ("Subject Name", "subject_name_entry"),
            ("Subject Assessment", "subject_assessment_entry"),
            ("Weighted Mark", "weighted_mark_entry"),
            ("Mark Weight", "mark_weight_entry"),
            ("Total Mark", "total_mark_entry"),
        ]

        for i, (field, attr) in enumerate(fields):
            label = ttk.Label(entry_frame, text=f"{field}:")
            label.grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
            entry = ttk.Entry(entry_frame, width=50)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky=tk.W)
            setattr(self, attr, entry)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=10)

        add_btn = ttk.Button(button_frame, text="Add Entry", compound=tk.LEFT, command=self.add_entry)
        add_btn.grid(row=0, column=0, padx=5, pady=5)

        del_btn = ttk.Button(button_frame, text="Delete Entry", compound=tk.LEFT, command=self.delete_entry)
        del_btn.grid(row=0, column=1, padx=5, pady=5)

        calc_btn = ttk.Button(button_frame, text="Calculate Exam Mark", compound=tk.LEFT, command=self.calculate_exam_mark)
        calc_btn.grid(row=0, column=2, padx=5, pady=5)

        sync_btn = ttk.Button(button_frame, text="Sync All Semesters", compound=tk.LEFT, command=self.sync_all_semesters)
        sync_btn.grid(row=0, column=3, padx=5, pady=5)

        self.treeview.bind("<Motion>", self.on_treeview_motion)
        self.treeview.bind("<<TreeviewSelect>>", self.on_treeview_select)

        self.update_semester()

        # Make the main frame expandable
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

    def on_treeview_select(self, _event=None):
        """
        Handles the selection event on the Treeview widget.
        
        Args:
            _event (tk.Event): The event that triggered the selection.
        """
        selected_item = self.treeview.selection()
        if selected_item:
            selected_item_id = selected_item[0]
            values = self.treeview.item(selected_item_id, "values")
            
            entries = [
                (self.subject_code_entry, values[0]),
                (self.subject_assessment_entry, values[1]),
                (self.weighted_mark_entry, values[3]),
                (self.mark_weight_entry, values[4].replace("%", ""))
            ]

            for entry, value in entries:
                entry.delete(0, tk.END)
                entry.insert(0, value)

    def on_treeview_motion(self, event):
        """
        Handles the mouse motion event on the Treeview widget.
        
        Args:
            event (tk.Event): The event that triggered the mouse motion.
        """
        region = self.treeview.identify("region", event.x, event.y)
        if (region == "cell"):
            column = self.treeview.identify_column(event.x)
            row_id = self.treeview.identify_row(event.y)

            if column in [f"#{i}" for i in range(1, 3)]:  # Check if the column is Subject Assessment
                values = self.treeview.item(row_id, "values")

                if any("=" in value or "Assessments:" in value for value in values):
                    return
                if len(values) > 1:
                    text = values[1]
                    if self.current_tooltip:
                        self.current_tooltip.hide_tip(event)
                    self.current_tooltip = ToolTip(self.treeview, text)
                    self.current_tooltip.show_tip(event)
            else:
                if self.current_tooltip:
                    self.current_tooltip.hide_tip(event)
                    self.current_tooltip = None
        else:
            if self.current_tooltip:
                self.current_tooltip.hide_tip(event)
                self.current_tooltip = None

    def on_window_resize(self, _event=None):
        """
        Handles the window resize event and adjusts the column width of the Treeview widget.
        
        Args:
            event (tk.Event): The event that triggered the window resize.
        """
        total_width = self.root.winfo_width()
        column_count = len(self.treeview["columns"])
        column_width = total_width // column_count
        for col in self.treeview["columns"]:
            self.treeview.column(col, width=column_width)

    def update_year(self, _event=None):
        """
        Updates the year in the application.

        Args:
            event (tk.Event): The event that triggered the year update.
        """
        selected_year = self.year_var.get()
        self.data_persistence = DataPersistence(selected_year)
        self.semesters = {sem: Semester(sem, self.data_persistence.year, self.data_persistence)
                          for sem in self.semesters.keys()}
        self.update_semester()
        self.update_treeview()
        print(f"Year set in update_year: {selected_year}")

    def update_semester(self, _event=None):
        """
        Updates the semester in the application.
        
        Args:
            event (tk.Event): The event that triggered the semester update.
        """
        selected_sheet = self.sheet_var.get()
        selected_year = self.year_var.get()
        if self.semesters[selected_sheet] is None:
            self.semesters[selected_sheet] = Semester(selected_sheet, 
                                                      selected_year, self.data_persistence)
        self.update_treeview()

    def update_treeview(self):
        """Updates the Treeview widget with the data from the selected semester."""
        semester_name = self.sheet_var.get()
        semester = self.semesters[semester_name]
        treeview_data = semester.view_data()
        for row in self.treeview.get_children():
            self.treeview.delete(row)
        for row in treeview_data:
            self.treeview.insert("", "end", values=row)

    def add_entry(self):
        """Adds a new entry to the selected semester with assignment details."""
        subject_code = self.subject_code_entry.get()
        subject_name = self.subject_name_entry.get()
        subject_assessment = self.subject_assessment_entry.get()
        weighted_mark = self.weighted_mark_entry.get()
        mark_weight = self.mark_weight_entry.get()
        total_mark = self.total_mark_entry.get()
        semester_name = self.sheet_var.get()
        try:
            self.semesters[semester_name].add_entry(
                semester=semester_name,
                subject_code=subject_code,
                subject_name=subject_name,
                subject_assessment=subject_assessment,
                weighted_mark=weighted_mark,
                mark_weight=mark_weight,
                total_mark=total_mark
            )
        except ValueError as error:
            messagebox.showerror("Error", f"Failed to add entry: {error}")
        self.update_treeview()

    def delete_entry(self):
        """
        Deletes the selected entry from the Treeview widget and the data structure.
        
        Returns:
            int: -1 if no item is selected, 0 if the item is deleted successfully.
        """
        selected_items = self.treeview.selection()
        if not selected_items:
            messagebox.showerror("Error", "Please select an item to delete.")
            return

        semester_name = self.sheet_var.get()
        semester = self.semesters[semester_name]
        for selected_item in selected_items:
            values = self.treeview.item(selected_item, "values")
            if len(values) < 2:
                continue  # Skip if values are not sufficient

            subject_code = values[0]
            subject_assessment = values[1]

            # Remove the entry from the data structure
            if subject_code in semester.data_persistence.data[semester_name]:
                assessments = semester.data_persistence.data[semester_name][subject_code]["Assignments"]
                updated_assessments = [assessment for assessment in assessments if
                                       assessment["Subject Assessment"] != subject_assessment]

                semester.data_persistence.data[semester_name][subject_code]["Assignments"] = updated_assessments

                # Remove the entry from the tree view
                self.treeview.delete(selected_item)

            # Save the updated data structure
            semester.data_persistence.save_data()

            # Parse 'Examinations'
            try:
                mark_weight = float(self.mark_weight_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Mark Weight must be a valid number.")
                return

            # Fetch the current exam weight
            current_exam_weight = float(
                semester.data_persistence.data[semester_name][subject_code]["Examinations"].get("Exam Weight", 0))

            # Add the mark weight to the current exam weight
            exam_weight = current_exam_weight + mark_weight

            # Print statements for debugging
            print(f"Current Exam Weight for {subject_code}: {current_exam_weight}")
            print(f"Added Mark Weight: {mark_weight}")
            print(f"New Calculated Exam Weight for {subject_code}: {exam_weight}")

            # Ensure the data structure for 'Examinations' exists before adding to it
            if "Examinations" not in semester.data_persistence.data[semester_name][subject_code]:
                semester.data_persistence.data[semester_name][subject_code]["Examinations"] = {}

            # Update only the "Exam Weight" field for the specific subject
            semester.data_persistence.data[semester_name][subject_code]["Examinations"]["Exam Weight"] = exam_weight

            messagebox.showinfo("Success", "Selected entry has been deleted.")

            # Save the updated data structure again
            semester.data_persistence.save_data()

        self.update_treeview()

    def sort_subjects(self, sort_by="Subject Code"):
        """
        Sorts the subjects in the Treeview widget based on the selected field.
        
        Args:
            sort_by (str, optional):
                The field by which the subjects are sorted. Defaults to "Subject Code".
        """
        semester_name = self.sheet_var.get()
        semester = self.semesters[semester_name]
        semester.sort_subjects(sort_by)
        # Get the data to be sorted
        treeview_data = semester.view_data()

        # Sort by the chosen field (Subject Code, Subject Assessment, Weighted Mark, Mark Weight)
        if sort_by == "Subject Code":
            treeview_data.sort(key=lambda row: row[0])  # Sort by Subject Code
        elif sort_by == "Subject Assessment":
            treeview_data.sort(key=lambda row: row[1])  # Sort by Subject Assessment
        elif sort_by == "Weighted Mark":
            treeview_data.sort(key=lambda row:
                               float(row[3]) if row[3] else 0)  # Sort by Weighted Mark
        elif sort_by == "Mark Weight":
            treeview_data.sort(key=lambda row:
                               float(row[4].replace("%", ""))
                               if row[4] else 0)  # Sort by Mark Weight

        # Optionally, display a success message
        messagebox.showinfo("Sorted", f"Subjects sorted by {sort_by}.")


    def calculate_exam_mark(self):
        """Synchronises all semesters' data into a single data structure."""
        semester_name = self.sheet_var.get()
        subject_code = self.subject_code_entry.get()
        if not subject_code:
            messagebox.showerror("Error", "Please enter a Subject Code.")
            return
        exam_mark = self.semesters[semester_name].calculate_exam_mark(subject_code)

        self.update_treeview()
        if exam_mark is not None:
            messagebox.showinfo("Success", f"Exam Mark for {subject_code}: {exam_mark}")
        else:
            messagebox.showerror("Error", f"Subject {subject_code} not found.")
            self.update_treeview()

    def sync_all_semesters(self):
        """Synchronises all semesters' data into a single data structure."""
        combined_data = {
            "Autumn": self.data_persistence.data.get("Autumn", {}).copy(),
            "Spring": self.data_persistence.data.get("Spring", {}).copy(),
            "Annual": self.data_persistence.data.get("Annual", {}).copy()
        }

        # Add Annual data to Autumn and Spring for display purposes
        for subject, details in combined_data["Annual"].items():
            if subject not in combined_data["Autumn"]:
                combined_data["Autumn"][subject] = details
            if subject not in combined_data["Spring"]:
                combined_data["Spring"][subject] = details

        self.data_persistence.data = combined_data
        self.update_treeview()
