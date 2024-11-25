QLineEdit_styles = """
    QLineEdit{
        font-size: 18px;
        font-weight: 400;
        color: black;
        border-radius: 20px;
        padding: 15px 20px;
        border: 1px solid blue;
        margin: 8px 0px;
    }
    
    QLineEdit:focus{
        border: 2px solid blue;
    }
"""

QPushButton_styles = """
    QPushButton{
        font-size: 18px;
        color: black;
        font-weight: 400;
        padding: 15px 20px;
        border-radius: 20px;
        border: 1px solid blue;
        background-color: #ccc; 
        box-shadow: 0 0 40px black;
        margin-top: 10px;
    }
    
    QPushButton:hover{
        background-color: white;
    }
"""

QtableWidget_style = """
    QTableWidget {
        background-color: aqua;
        border: 2px solid blue;
        font-size: 18px;
        border-radius: 20px;
        margin-top: 10px;
    }
    QTableWidget::item {
        padding: 5px;
        border: none;
        font-size: 20px;
    }
    QTableWidget::item:selected {
        background-color: #3399ff;
        color: white;
    }
    QHeaderView::section {
        background-color: gray;
        color: white;
        font-weight: bold;
        padding: 4px;
        border: none;
        font-size: 18px;
    }
    QTableCornerButton::section {
        background-color: white;
        border: none;
    }
"""

QComboBox_style = """
    QComboBox{
        padding: 15px 20px;
        color: white;
        border-radius: 20px;
        font-size: 18px;
        background-color: gray;
        border: 2px solid blue;
    }
"""
