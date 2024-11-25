from PyQt5.QtWidgets import *
from database.connection import get_connection
from PyQt5.QtCore import Qt
import styles


class Edit_Page(QDialog):
    def __init__(self, parent, student_id):
        super().__init__()

        self.id = student_id

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT * FROM students WHERE id = %s
        """, (student_id, ))
        data = cursor.fetchone()

        self.setMinimumSize(500, 600)
        self.setWindowTitle("Edit Page")

        self.title = QLabel("Edit Student")
        self.title.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("font-size: 20px; font-weight: 500;")

        self.full_name = QLineEdit()
        self.full_name.setText(data[1])

        self.age = QLineEdit()
        self.age.setText(str(data[2]))

        self.phone_number = QLineEdit()
        self.phone_number.setText(data[3])

        self.course = QLineEdit()
        self.course.setText(data[4])

        self.email = QLineEdit()
        self.email.setText(data[5])

        self.location = QLineEdit()
        self.location.setText(data[6])

        lineEdits = [
            self.full_name,
            self.age,
            self.phone_number,
            self.email,
            self.course,
            self.location
        ]

        for lineEdit in lineEdits:
            lineEdit.setStyleSheet(styles.QLineEdit_styles)

        self.submit_btn = QPushButton("submit")
        self.submit_btn.clicked.connect(self.submit_clicked)
        self.submit_btn.setStyleSheet(styles.QPushButton_styles)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title)
        main_layout.addWidget(self.full_name)
        main_layout.addWidget(self.age)
        main_layout.addWidget(self.phone_number)
        main_layout.addWidget(self.course)
        main_layout.addWidget(self.email)
        main_layout.addWidget(self.location)
        main_layout.addWidget(self.submit_btn)

        self.setLayout(main_layout)

    def submit_clicked(self):
        connection = get_connection()
        cursor = connection.cursor()

        full_name = self.full_name.text()
        age = self.age.text()
        phone_number = self.phone_number.text()
        course = self.course.text()
        email = self.email.text()
        location = self.location.text()

        if all([full_name, age, phone_number, course, email, location]):
            cursor.execute("""
                UPDATE students SET full_name = %s, age = %s, phone_number = %s, 
                course = %s, email = %s, location = %s WHERE id = %s
            """, (full_name, age, phone_number, course, email, location, self.id))
            connection.commit()
            cursor.close()
            connection.close()

            self.accept()
        else:
            QMessageBox.warning(self, "Waning", "Iltimos barcha qatorlarni to'ldiring!")