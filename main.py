
import os
import json
from datetime import date

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE_DIR, "students.json")
LOGO = os.path.join(BASE_DIR, "logo png.png")

def load_data():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as f:
                data = json.load(f)
                for s in data:
                    s.setdefault("class", "")
                    s.setdefault("section", "")
                    s.setdefault("fee", 0)
                    s.setdefault("fee_status", "Unpaid")
                    s.setdefault("photo", "")
                    s.setdefault("attendance", {})
                return data
        except:
            return []
    return []

students = load_data()

def save_data():
    with open(FILE, "w") as f:
        json.dump(students, f, indent=4)

KV = """
ScreenManager:
    HomeScreen:
    AddScreen:
    ViewScreen:
    SearchScreen:
    DeleteScreen:
    FeeScreen:
    AttendanceScreen:

<HomeScreen>:
    name: "home"
    BoxLayout:
        orientation: "vertical"
        padding: 15
        spacing: 8

        canvas.before:
            Color:
                rgba: 0.94, 0.97, 1, 1
            Rectangle:
                pos: self.pos
                size: self.size

        Image:
            id: logo
            size_hint_y: None
            height: 125
            allow_stretch: True
            keep_ratio: True

        Label:
            text: "SHAHID STUDENT MANAGER"
            font_size: 21
            bold: True
            color: 0.05, 0.20, 0.45, 1
            size_hint_y: None
            height: 40

        Button:
            text: "ADD STUDENT"
            on_press: root.manager.current = "add"

        Button:
            text: "VIEW STUDENTS"
            on_press:
                root.manager.get_screen("view").refresh()
                root.manager.current = "view"

        Button:
            text: "SEARCH STUDENT"
            on_press: root.manager.current = "search"

        Button:
            text: "FEE MANAGEMENT"
            on_press: root.manager.current = "fee"

        Button:
            text: "ATTENDANCE"
            on_press: root.manager.current = "attendance"

        Button:
            text: "DELETE STUDENT"
            background_color: 0.8, 0.2, 0.2, 1
            on_press: root.manager.current = "delete"

<AddScreen>:
    name: "add"
    BoxLayout:
        orientation: "vertical"
        padding: 15
        spacing: 8

        Label:
            text: "ADD NEW STUDENT"
            font_size: 22
            bold: True
            size_hint_y: None
            height: 45

        TextInput:
            id: student_name
            hint_text: "Student Name"
            multiline: False
            size_hint_y: None
            height: 48

        TextInput:
            id: father_name
            hint_text: "Father Name"
            multiline: False
            size_hint_y: None
            height: 48

        TextInput:
            id: roll_no
            hint_text: "Roll Number"
            multiline: False
            size_hint_y: None
            height: 48

        TextInput:
            id: student_class
            hint_text: "Class (e.g. 5)"
            multiline: False
            size_hint_y: None
            height: 48

        TextInput:
            id: section
            hint_text: "Section (e.g. A)"
            multiline: False
            size_hint_y: None
            height: 48

        TextInput:
            id: fee
            hint_text: "Monthly Fee"
            input_filter: "int"
            multiline: False
            size_hint_y: None
            height: 48

        TextInput:
            id: photo
            hint_text: "Photo file name (optional)"
            multiline: False
            size_hint_y: None
            height: 48

        Label:
            text: "Put student photo in this same folder"
            font_size: 12
            size_hint_y: None
            height: 25

        Button:
            text: "SAVE STUDENT"
            size_hint_y: None
            height: 50
            on_press: root.add_student()

        Label:
            id: message
            text: ""
            size_hint_y: None
            height: 35

        Button:
            text: "BACK HOME"
            size_hint_y: None
            height: 45
            on_press: root.manager.current = "home"

<ViewScreen>:
    name: "view"
    BoxLayout:
        orientation: "vertical"
        padding: 15
        spacing: 10

        Label:
            text: "STUDENT RECORDS"
            font_size: 22
            bold: True
            size_hint_y: None
            height: 45

        ScrollView:
            Label:
                id: records
                text: ""
                size_hint_y: None
                height: self.texture_size[1] + 30
                text_size: self.width, None
                halign: "left"
                valign: "top"

        Button:
            text: "REFRESH"
            size_hint_y: None
            height: 48
            on_press: root.refresh()

        Button:
            text: "BACK HOME"
            size_hint_y: None
            height: 48
            on_press: root.manager.current = "home"

<SearchScreen>:
    name: "search"
    BoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 12

        Label:
            text: "SEARCH STUDENT"
            font_size: 22
            bold: True

        TextInput:
            id: search_roll
            hint_text: "Enter Roll Number"
            multiline: False
            size_hint_y: None
            height: 50

        Button:
            text: "SEARCH"
            size_hint_y: None
            height: 50
            on_press: root.search_student()

        Label:
            id: result
            text: ""
            halign: "left"
            valign: "middle"

        Button:
            text: "BACK HOME"
            size_hint_y: None
            height: 48
            on_press: root.manager.current = "home"

<FeeScreen>:
    name: "fee"
    BoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 12

        Label:
            text: "FEE MANAGEMENT"
            font_size: 22
            bold: True

        TextInput:
            id: fee_roll
            hint_text: "Student Roll Number"
            multiline: False
            size_hint_y: None
            height: 50

        TextInput:
            id: fee_amount
            hint_text: "Fee Amount"
            input_filter: "int"
            multiline: False
            size_hint_y: None
            height: 50

        Spinner:
            id: fee_status
            text: "Paid"
            values: ["Paid", "Unpaid"]
            size_hint_y: None
            height: 50

        Button:
            text: "SAVE FEE RECORD"
            size_hint_y: None
            height: 55
            on_press: root.save_fee()

        Label:
            id: fee_message
            text: ""

        Button:
            text: "BACK HOME"
            size_hint_y: None
            height: 48
            on_press: root.manager.current = "home"

<AttendanceScreen>:
    name: "attendance"
    BoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 12

        Label:
            text: "STUDENT ATTENDANCE"
            font_size: 22
            bold: True

        Label:
            text: "Date: " + root.today
            size_hint_y: None
            height: 35

        TextInput:
            id: attendance_roll
            hint_text: "Student Roll Number"
            multiline: False
            size_hint_y: None
            height: 50

        Spinner:
            id: attendance_status
            text: "Present"
            values: ["Present", "Absent", "Leave"]
            size_hint_y: None
            height: 50

        Button:
            text: "SAVE ATTENDANCE"
            size_hint_y: None
            height: 55
            on_press: root.mark_attendance()

        Label:
            id: attendance_message
            text: ""

        Button:
            text: "BACK HOME"
            size_hint_y: None
            height: 48
            on_press: root.manager.current = "home"

<DeleteScreen>:
    name: "delete"
    BoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 12

        Label:
            text: "DELETE STUDENT"
            font_size: 22
            bold: True

        TextInput:
            id: delete_roll
            hint_text: "Enter Roll Number"
            multiline: False
            size_hint_y: None
            height: 50

        Button:
            text: "DELETE RECORD"
            size_hint_y: None
            height: 55
            background_color: 0.8, 0.2, 0.2, 1
            on_press: root.delete_student()

        Label:
            id: delete_message
            text: ""

        Button:
            text: "BACK HOME"
            size_hint_y: None
            height: 48
            on_press: root.manager.current = "home"
"""

class HomeScreen(Screen):
    pass

class AddScreen(Screen):
    def add_student(self):
        name = self.ids.student_name.text.strip()
        father = self.ids.father_name.text.strip()
        roll = self.ids.roll_no.text.strip()

        if not name or not father or not roll:
            self.ids.message.text = "Fill name, father name and roll!"
            return

        if any(s["roll"] == roll for s in students):
            self.ids.message.text = "Roll number already exists!"
            return

        students.append({
            "name": name,
            "father": father,
            "roll": roll,
            "class": self.ids.student_class.text.strip(),
            "section": self.ids.section.text.strip(),
            "fee": int(self.ids.fee.text or 0),
            "fee_status": "Unpaid",
            "photo": self.ids.photo.text.strip(),
            "attendance": {}
        })

        save_data()
        self.ids.message.text = "Student Saved Successfully!"

        for field in ("student_name", "father_name", "roll_no",
                      "student_class", "section", "fee", "photo"):
            self.ids[field].text = ""

class ViewScreen(Screen):
    def refresh(self):
        if not students:
            self.ids.records.text = "No students found."
            return

        lines = []
        for s in students:
            lines.append(
                "Name: " + s["name"] +
                "\nFather: " + s["father"] +
                "\nRoll: " + s["roll"] +
                "\nClass: " + s.get("class", "") +
                "\nSection: " + s.get("section", "") +
                "\nMonthly Fee: " + str(s.get("fee", 0)) +
                "\nFee Status: " + s.get("fee_status", "Unpaid") +
                "\nPhoto: " + s.get("photo", "") +
                "\n------------------------"
            )
        self.ids.records.text = "\n\n".join(lines)

class SearchScreen(Screen):
    def search_student(self):
        roll = self.ids.search_roll.text.strip()
        found = next((s for s in students if s["roll"] == roll), None)

        if found:
            self.ids.result.text = (
                "Name: " + found["name"] +
                "\nFather: " + found["father"] +
                "\nRoll: " + found["roll"] +
                "\nClass: " + found.get("class", "") +
                "\nSection: " + found.get("section", "") +
                "\nFee: " + str(found.get("fee", 0)) +
                "\nFee Status: " + found.get("fee_status", "Unpaid")
            )
        else:
            self.ids.result.text = "Student not found!"

class FeeScreen(Screen):
    def save_fee(self):
        roll = self.ids.fee_roll.text.strip()
        amount = self.ids.fee_amount.text.strip()
        status = self.ids.fee_status.text

        found = next((s for s in students if s["roll"] == roll), None)

        if not found:
            self.ids.fee_message.text = "Student not found!"
            return

        if not amount:
            self.ids.fee_message.text = "Enter fee amount!"
            return

        found["fee"] = int(amount)
        found["fee_status"] = status
        save_data()
        self.ids.fee_message.text = "Fee record saved!"

class AttendanceScreen(Screen):
    @property
    def today(self):
        return date.today().isoformat()

    def mark_attendance(self):
        roll = self.ids.attendance_roll.text.strip()
        status = self.ids.attendance_status.text

        found = next((s for s in students if s["roll"] == roll), None)

        if not found:
            self.ids.attendance_message.text = "Student not found!"
            return

        found.setdefault("attendance", {})
        found["attendance"][self.today] = status
        save_data()
        self.ids.attendance_message.text = "Attendance saved!"

class DeleteScreen(Screen):
    def delete_student(self):
        roll = self.ids.delete_roll.text.strip()
        found = next((s for s in students if s["roll"] == roll), None)

        if found:
            students.remove(found)
            save_data()
            self.ids.delete_message.text = "Student Deleted!"
        else:
            self.ids.delete_message.text = "Student Not Found!"

class StudentApp(App):
    def build(self):
        self.title = "Shahid Student Manager"
        self.icon = LOGO

        root = Builder.load_string(KV)
        logo_widget = root.get_screen("home").ids.logo

        if os.path.exists(LOGO):
            logo_widget.source = LOGO
            logo_widget.reload()
        else:
            print("Logo not found:", LOGO)

        return root

if __name__ == "__main__":
    StudentApp().run()
