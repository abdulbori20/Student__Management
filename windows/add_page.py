from PyQt5.QtWidgets import *
from database.connection import get_connection
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QIcon
import styles
from PyQt5.QtWebEngineWidgets import QWebEngineView
import webbrowser


class Add_Page(QDialog):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(500, 600)
        self.setWindowTitle("Add Page")

        self.title = QLabel("Add Student")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 20px; font-weight: 500;")

        self.full_name = QLineEdit()
        self.full_name.setPlaceholderText("Enter student's full name")

        self.age = QLineEdit()
        self.age.setPlaceholderText("Enter student's age")

        self.phone_number = QComboBox()
        self.phone_number.setIconSize(QSize(35, 35))
        self.phone_number.setStyleSheet(styles.QComboBox_style)

        self.countries = {
            "Uzbekistan": {"code": "+998", "flag": "flags/uzbekistan.png"},
            "Kirgizistan": {"code": "+996", "flag": "flags/kyrgyzstan.png"},
            "Russiya": {"code": "+7", "flag": "flags/russia.png"},
        }

        for country, info in self.countries.items():
            self.phone_number.addItem(QIcon(info["flag"]), f"{country}")

        self.phone_input = QLineEdit(self)
        self.phone_input.setPlaceholderText("Telefon raqamini kiriting")
        self.phone_input.setText(self.countries["Uzbekistan"]["code"])
        self.phone_number.currentIndexChanged.connect(self.update_phone_code)

        self.course = QComboBox()
        self.course.addItems(["1-kurs", "2-kurs", "3-kurs", "4-kurs"])
        self.course.setStyleSheet(styles.QComboBox_style)

        self.email = QLineEdit()
        self.email.setPlaceholderText("Enter student's email")

        self.location = QLineEdit()
        self.location.setPlaceholderText("Enter student's location")

        self.location_btn = QPushButton("Select on Map")
        self.location_btn.setStyleSheet(styles.QPushButton_styles)
        self.location_btn.clicked.connect(self.open_google_maps)

        self.submit_btn = QPushButton("Submit")
        self.submit_btn.clicked.connect(self.submit_clicked)
        self.submit_btn.setStyleSheet(styles.QPushButton_styles)

        lineEdits = [
            self.full_name,
            self.age,
            self.phone_input,
            self.email,
            self.location
        ]

        for lineEdit in lineEdits:
            lineEdit.setStyleSheet(styles.QLineEdit_styles)

        container = QHBoxLayout()
        container.addWidget(self.phone_number)
        container.addWidget(self.phone_input)

        container1 = QHBoxLayout()
        container1.addWidget(self.location)
        container1.addWidget(self.location_btn)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title)
        main_layout.addWidget(self.full_name)
        main_layout.addWidget(self.age)
        main_layout.addLayout(container)
        main_layout.addWidget(self.course)
        main_layout.addWidget(self.email)
        main_layout.addLayout(container1)
        main_layout.addWidget(self.submit_btn)

        self.setLayout(main_layout)

    def submit_clicked(self):
        cursor = None
        connection = None
        try:
            connection = get_connection()
            cursor = connection.cursor()

            full_name = self.full_name.text().strip()
            age = self.age.text().strip()
            phone_number = self.phone_input.text().strip()
            course = self.course.currentText().strip()
            email = self.email.text().strip()
            location = self.location.text().strip()

            if not age.isdigit():
                QMessageBox.warning(self, "Warning", "Iltimos yoshni raqam sifatida kiriting!")
                return

            age = int(age)
            if age < 15 or age > 70:
                QMessageBox.warning(self, "Warning", "Yosh 15 dan kichik 70 dan katta bo'lishi mumkin emas!")
                return

            if not email.endswith("@gmail.com"):
                QMessageBox.warning(self, "Warning", "Email manzili faqat @gmail.com bilan tugashi kerak")
                return

            if all([full_name, age, phone_number, course, email, location]):
                cursor.execute("""
                    INSERT INTO students (full_name, age, phone_number, course, email, location) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (full_name, age, phone_number, course, email, location))
                connection.commit()
                QMessageBox.information(self, "Muvaffaqiyatli", "Student ma'lumotlari muvaffaqiyatli saqlandi")
                self.accept()
            else:
                QMessageBox.warning(self, "Warning", "Iltimos, barcha qatorlarni to‘ldiring!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ma'lumotlar bazasi bilan bog‘lanishda xatolik:\n{e}")
        finally:
            cursor.close()
            connection.close()

    def update_phone_code(self):
        selected_country = self.phone_number.currentText()
        if selected_country in self.countries:
            self.phone_input.setText(self.countries[selected_country]["code"])

    def open_google_maps(self):
        """
        Open Google Maps in the default web browser for the user to select a location.
        """

        url = "https://www.google.com/maps"
        webbrowser.open(url)

        QMessageBox.information(
            self,
            "Select Location",
            "Please select a location on Google Maps, copy the address, and paste it here."
        )