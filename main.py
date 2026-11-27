
import json
import os
from datetime import date

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.window import Window

DATA_FILE = "students.json"


class StudentManager(App):

    def build(self):
        self.title = "Shahid Student Manager"
        Window.clearcolor = (0.92, 0.95, 1, 1)

        self.students = self.load_data()

        root = BoxLayout(
            orientation="vertical",
            padding=12,
            spacing=8
        )

        heading = Label(
            text="[b]SHAHID STUDENT MANAGER[/b]",
            markup=True,
            font_size=22,
            color=(0.05, 0.2, 0.4, 1),
            size_hint_y=None,
            height=55
        )
        root.add_widget(heading)

        self.student_name = self.make_input("Student Name")
        self.father = self.make_input("Father Name")
        self.class_name = self.make_input("Class")
        self.section = self.make_input("Section")
        self.phone = self.make_input("Mobile Number")
        self.fee = self.make_input("Fee Amount")
        self.photo = self.make_input("Photo File Path (optional)")

        for field in [
            self.student_name, self.father, self.class_name,
            self.section, self.phone, self.fee, self.photo
        ]:
            root.add_widget(field)

        self.fee_status = TextInput(
            hint_text="Fee Status: Paid or Unpaid",
            multiline=False,
            size_hint_y=None,
            height=42
        )
        root.add_widget(self.fee_status)

        self.attendance = TextInput(
            hint_text="Attendance: Present / Absent / Leave",
            multiline=False,
            size_hint_y=None,
            height=42
        )
        root.add_widget(self.attendance)

        self.search_box = self.make_input("Search Student Name")
        root.add_widget(self.search_box)

        buttons = [
            ("Add Student", self.add_student),
            ("View Students", self.view_students),
            ("Search Student", self.search_student),
            ("Mark Attendance", self.mark_attendance),
            ("Delete Student", self.delete_student),
            ("Clear Fields", self.clear_fields)
        ]

        for title, action in buttons:
            btn = Button(
                text=title,
                size_hint_y=None,
                height=45,
                background_color=(0.08, 0.3, 0.58, 1)
            )
            btn.bind(on_press=action)
            root.add_widget(btn)

        return root

    def make_input(self, hint):
        return TextInput(
            hint_text=hint,
            multiline=False,
            size_hint_y=None,
            height=42
        )

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data if isinstance(data, list) else []
            except Exception:
                return []
        return []

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(
                self.students,
                f,
                ensure_ascii=False,
                indent=4
            )

    def message(self, title, text):
        content = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )
        content.add_widget(Label(text=text))

        close = Button(
            text="OK",
            size_hint_y=None,
            height=45
        )
        content.add_widget(close)

        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.85, 0.4)
        )
        close.bind(on_press=popup.dismiss)
        popup.open()

    def add_student(self, instance):
        if not self.student_name.text.strip():
            self.message("Error", "Student name is required.")
            return

        student = {
            "id": len(self.students) + 1,
            "name": self.student_name.text.strip(),
            "father": self.father.text.strip(),
            "class": self.class_name.text.strip(),
            "section": self.section.text.strip(),
            "phone": self.phone.text.strip(),
            "fee": self.fee.text.strip(),
            "fee_status": self.fee_status.text.strip(),
            "photo": self.photo.text.strip(),
            "attendance": {}
        }

        self.students.append(student)
        self.save_data()
        self.clear_fields(None)

        self.message("Success", "Student added successfully!")

    def view_students(self, instance):
        if not self.students:
            self.message("Students", "No students found.")
            return

        lines = []

        for s in self.students:
            lines.append(
                f"Name: {s.get('name', '')}\n"
                f"Father: {s.get('father', '')}\n"
                f"Class: {s.get('class', '')} "
                f"{s.get('section', '')}\n"
                f"Phone: {s.get('phone', '')}\n"
                f"Fee: {s.get('fee', '')} "
                f"({s.get('fee_status', '')})\n"
                "----------------------"
            )

        self.show_long_text("All Students", "\n".join(lines))

    def search_student(self, instance):
        query = self.search_box.text.strip().lower()

        if not query:
            self.message("Search", "Enter a student name.")
            return

        matches = [
            s for s in self.students
            if query in s.get("name", "").lower()
        ]

        if not matches:
            self.message("Search", "Student not found.")
            return

        result = []
        for s in matches:
            result.append(
                f"Name: {s.get('name', '')}\n"
                f"Class: {s.get('class', '')}\n"
                f"Phone: {s.get('phone', '')}\n"
                f"Fee: {s.get('fee_status', '')}"
            )

        self.show_long_text("Search Results", "\n\n".join(result))

    def mark_attendance(self, instance):
        query = self.student_name.text.strip().lower()
        status = self.attendance.text.strip().title()

        if not query:
            self.message("Attendance", "Enter student name in Student Name.")
            return

        if status not in ["Present", "Absent", "Leave"]:
            self.message(
                "Attendance",
                "Enter Present, Absent or Leave."
            )
            return

        for s in self.students:
            if s.get("name", "").lower() == query:
                s.setdefault("attendance", {})
                s["attendance"][str(date.today())] = status
                self.save_data()
                self.message("Success", "Attendance saved.")
                return

        self.message("Attendance", "Student not found.")

    def delete_student(self, instance):
        query = self.search_box.text.strip().lower()

        if not query:
            self.message("Delete", "Enter name in Search Student Name.")
            return

        old_count = len(self.students)

        self.students = [
            s for s in self.students
            if s.get("name", "").lower() != query
        ]

        if len(self.students) == old_count:
            self.message("Delete", "Student not found.")
        else:
            self.save_data()
            self.message("Success", "Student deleted.")

    def clear_fields(self, instance):
        for field in [
            self.student_name, self.father, self.class_name,
            self.section, self.phone, self.fee,
            self.photo, self.fee_status,
            self.attendance, self.search_box
        ]:
            field.text = ""

    def show_long_text(self, title, text):
        layout = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        display = TextInput(
            text=text,
            readonly=True,
            size_hint_y=1
        )
        layout.add_widget(display)

        close = Button(
            text="Close",
            size_hint_y=None,
            height=45
        )
        layout.add_widget(close)

        popup = Popup(
            title=title,
            content=layout,
            size_hint=(0.92, 0.85)
        )
        close.bind(on_press=popup.dismiss)
        popup.open()


if __name__ == "__main__":
    StudentManager().run()
