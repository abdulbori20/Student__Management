import styles
from database.database_main import init_db
from PyQt5.QtWidgets import *
import sys
from database.connection import get_connection
from windows.add_page import Add_Page
from windows.edit_page import Edit_Page

init_db()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_UI()

    def init_UI(self):
        self.setWindowTitle("Asosiy oyna")
        self.setGeometry(450, 200, 990, 790)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("search...")
        self.search_input.textChanged.connect(self.search_clicked)
        self.search_input.setStyleSheet(styles.QLineEdit_styles)

        self.add_btn = QPushButton("add")
        self.add_btn.clicked.connect(self.add_clicked)

        self.edit_btn = QPushButton("edit")
        self.edit_btn.clicked.connect(self.edit_clicked)

        self.delete_btn = QPushButton("delete")
        self.delete_btn.clicked.connect(self.delete_clicked)

        buttons = [
            self.add_btn,
            self.edit_btn,
            self.delete_btn
        ]

        for button in buttons:
            button.setStyleSheet(styles.QPushButton_styles)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["id", "full_name", "age", "phone_number", "course", "email", "location"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setStyleSheet(styles.QtableWidget_style)

        container1 = QHBoxLayout()
        container1.addWidget(self.add_btn)
        container1.addWidget(self.edit_btn)
        container1.addWidget(self.delete_btn)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.search_input)
        main_layout.addLayout(container1)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

        self.load_data()

    def load_data(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM students")
        data = cursor.fetchall()
        self.table.setRowCount(len(data))
        for row, student in enumerate(data):
            for column, data in enumerate(student):
                self.table.setItem(row, column, QTableWidgetItem(str(data)))

    def search_clicked(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT * FROM students WHERE full_name LIKE %s OR email LIKE %s
        """, ('%' + self.search_input.text() + '%', '%' + self.search_input.text() + '%'))
        data = cursor.fetchall()
        self.table.setRowCount(len(data))
        for row, student in enumerate(data):
            for column, data in enumerate(student):
                self.table.setItem(row, column, QTableWidgetItem(str(data)))

    def add_clicked(self):
        self.add_page = Add_Page()
        if self.add_page.exec_():
            self.load_data()

    def edit_clicked(self):
        selected_items = self.table.selectedItems()
        if len(selected_items) < 1:
            QMessageBox.warning(self, "Warning", "You must select any field!")
            return

        student_id = selected_items[0].text()
        self.edit_page = Edit_Page(self, student_id)

        if self.edit_page.exec_():
            self.load_data()

    def delete_clicked(self):
        connection = get_connection()
        cursor = connection.cursor()

        selected_items = self.table.selectedItems()
        if len(selected_items) < 1:
            QMessageBox.warning(self, "Warning", "You must select any field!")
        else:
            res = QMessageBox.question(self, "question", "Are you sure ?", QMessageBox.Yes | QMessageBox.No)
            if res == QMessageBox.Yes:
                student_id = selected_items[0].text()
                cursor.execute("""
                    DELETE FROM students WHERE id = %s
                """, (student_id, ))
                connection.commit()
                cursor.close()
                connection.close()

                self.load_data()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()

    sys.exit(app.exec_())
