from PyQt6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget, 
    QPushButton, 
    QLabel, 
    QLineEdit, 
    QComboBox, 
    QRadioButton, 
    QCheckBox, 
    QHBoxLayout, 
    QVBoxLayout, 
    QFormLayout,
    QButtonGroup,
    QFileDialog,
    QCalendarWidget
)
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QDate
import sys
import re
import mysql.connector

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 650
LABEL_WIDTH = 180
LABEL_FONTSIZE = 12
BUTTON_WIDTH = 150

class MyForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Registration Form")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setStyleSheet("""
            QWidget {
                font-family: Berlin Sans FB;
                font-size: 10pt;
                margin-bottom: 5px;
                background-color: #CCCCCC;
            }
            QLabel, QCheckBox {
                font-family: Arial;
                color: #333;
                margin-left: 20px;
                font-weight: bold;
            }
            QRadioButton {
                color: #333;
            }
            QLineEdit, QCalendarWidget, QComboBox {
                border: 1px solid rgba(40, 40, 81, 0.4);
                border-radius: 4px;
                padding: 5px;
                color: #222;
                background-color: #B1B1A5;
                margin-right: 40px;
            }
            QPushButton {
                background-color: #334444;
                color: #fff;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #111111;
            }
            QPushButton:clicked {
                background-color: #1C2822;
            }
            QComboBox::drop-down {
                subcontrol-position: left;
            }
        """)
        self.setWindowIcon(
            QIcon("D:/Python Codes/PyQt6 Tutorials/College_Registration_Form/Pictures/contact-form.ico")
        )
        
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        self.generalLayout = QVBoxLayout()
        centralWidget.setLayout(self.generalLayout)
        
        self._setUpUI()
        
        
    def loadDatabase(self):
        self.mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            passwd = "password",
            database = "student_database",
        )
        self.c = self.mydb.cursor()

    def _setUpUI(self):
        self.heading = QLabel("S T U D E N T   R E G I S T R A T I O N   F O R M")
        self.heading.setFixedHeight(100)
        self.heading.setStyleSheet(
            "font-family: High Tower Text; font-size: 15pt; font-weight: bold; margin: 10px; color: #333;"
        )
        self.heading.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.generalLayout.addWidget(self.heading)

        self.formLayout = QFormLayout()

        self.nameLabel = QLabel("Name")
        self.nameLabel.setFixedWidth(LABEL_WIDTH)
        self.nameEditLayout = QHBoxLayout()
        self.firstNameEdit = QLineEdit()
        self.firstName = self.firstNameEdit.text()
        self.firstNameEdit.setPlaceholderText("First Name")
        self.lastNameEdit = QLineEdit()
        self.lastName = self.lastNameEdit.text()
        self.lastNameEdit.setPlaceholderText("Last Name")
        self.nameEditLayout.addWidget(self.firstNameEdit)
        self.nameEditLayout.addWidget(self.lastNameEdit)
        self.formLayout.addRow(self.nameLabel, self.nameEditLayout)

        self.genderLabel = QLabel("Gender")
        self.genderLabel.setFixedWidth(LABEL_WIDTH)
        self.genderButtonLayout = QHBoxLayout()
        self.maleSelect = QRadioButton("Male")
        self.femaleSelect = QRadioButton("Female")
        self.genderGroup = QButtonGroup()
        self.genderGroup.addButton(self.maleSelect)
        self.genderGroup.addButton(self.femaleSelect)
        self.maleSelect.toggled.connect(self.onToggled)
        self.femaleSelect.toggled.connect(self.onToggled)
        self.genderButtonLayout.addWidget(self.maleSelect)
        self.genderButtonLayout.addWidget(self.femaleSelect)
        self.formLayout.addRow(self.genderLabel, self.genderButtonLayout)

        self.dateLabel = QLabel("Date of Birth")
        self.dateLabel.setFixedWidth(LABEL_WIDTH)
        self.dateEdit = QLineEdit()
        self.dateEdit.setPlaceholderText("Select Date")
        self.dateEdit.setCursor(Qt.CursorShape.ArrowCursor)

        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.selectionChanged.connect(self.onDateSelected)

        self.calendar.setWindowFlags(Qt.WindowType.Popup)

        self.calendarLayout = QVBoxLayout()
        self.calendarLayout.addWidget(self.calendar)
        self.formLayout.addRow(self.dateLabel, self.dateEdit)
        self.isCalendarOpen = False
        self.dateEdit.mousePressEvent = self.mousePressEvent

        self.ageLabel = QLabel("Age")
        self.ageLabel.setFixedWidth(LABEL_WIDTH)
        self.ageEdit = QLineEdit()
        self.age = self.ageEdit.text()
        self.formLayout.addRow(self.ageLabel, self.ageEdit)

        self.emailLabel = QLabel("Email Address")
        self.emailLabel.setFixedWidth(LABEL_WIDTH)
        self.emailEdit = QLineEdit()
        self.email = self.emailEdit.text()
        self.formLayout.addRow(self.emailLabel, self.emailEdit)

        self.passwordLabel = QLabel("Password")
        self.passwordLabel.setFixedWidth(LABEL_WIDTH)
        self.passwordEdit = QLineEdit()
        self.password = self.passwordEdit.text()
        self.formLayout.addRow(self.passwordLabel, self.passwordEdit)

        self.phoneLabel = QLabel("Phone Number")
        self.phoneLabel.setFixedWidth(LABEL_WIDTH)
        self.phoneLayout = QHBoxLayout()
        self.numberOptions = QComboBox()
        codes = ["015", "016", "017", "018", "019"]
        self.numberOptions.addItems(codes)
        self.numberOptions.setFixedWidth(100)
        self.phoneEdit = QLineEdit()
        self.phoneNo = self.numberOptions.currentText() + self.phoneEdit.text()
        self.phoneLayout.addWidget(self.numberOptions)
        self.phoneLayout.addWidget(self.phoneEdit)
        self.formLayout.addRow(self.phoneLabel, self.phoneLayout)

        self.addressLabel = QLabel("Address")
        self.addressLabel.setFixedWidth(LABEL_WIDTH)
        self.addressEditLayout = QHBoxLayout()
        self.villageEdit = QLineEdit()
        self.thanaEdit = QLineEdit()
        self.villageEdit.setPlaceholderText("Village")
        self.thanaEdit.setPlaceholderText("Thana")
        self.addressEditLayout.addWidget(self.villageEdit)
        self.addressEditLayout.addWidget(self.thanaEdit)
        self.formLayout.addRow(self.addressLabel, self.addressEditLayout)

        self.address2Label = QLabel()
        self.address2Label.setFixedWidth(LABEL_WIDTH)
        self.address2EditLayout = QHBoxLayout()
        self.postOfficeEdit = QLineEdit()
        self.districtEdit = QLineEdit()
        self.postOfficeEdit.setPlaceholderText("Post Office")
        self.districtEdit.setPlaceholderText("District")
        self.address = f"{self.villageEdit.text()}, {self.thanaEdit.text()}, {self.postOfficeEdit.text()}, {self.districtEdit.text()}"
        self.address2EditLayout.addWidget(self.postOfficeEdit)
        self.address2EditLayout.addWidget(self.districtEdit)
        self.formLayout.addRow(self.address2Label, self.address2EditLayout)

        self.hobbyLabel = QLabel("Hobbies")
        self.hobbyLabel.setFixedWidth(LABEL_WIDTH)
        self.hobbyEdit = QComboBox()
        self.hobbyEdit.setFixedSize(200, 30)
        options = ["Drawing", "Decorating", "Playing", "Singing", "Others"]
        self.hobbyEdit.addItems(options)
        self.hobbies = self.hobbyEdit.currentText()
        # self.hobbyEdit.activated.connect(self.showDropdown)
        self.formLayout.addRow(self.hobbyLabel, self.hobbyEdit)

        self.photoLayout = QHBoxLayout()
        self.photoLabel = QLabel("Upload Photo")
        self.photoLabel.setFixedWidth(LABEL_WIDTH)
        self.photoSizeLabel = QLabel("*Max Size\n 1000 KB")
        self.photoSizeLabel.setStyleSheet("font-size: 8pt; color: #FE231F; margin: 1px;")
        self.photoButton = QPushButton("Choose File")
        self.photoButton.setStyleSheet("margin-left: 5px; margin-right: 5px;")
        self.photoButton.clicked.connect(self.uploadImage)
        self.photoUploadLabel = QLabel("No File Chosen")
        self.photoUploadLabel.setStyleSheet("margin-left: 10px; margin-right: 50px;")
        self.photoLayout.addWidget(self.photoSizeLabel)
        self.photoLayout.addWidget(self.photoButton)
        self.photoLayout.addWidget(self.photoUploadLabel)
        self.formLayout.addRow(self.photoLabel, self.photoLayout)

        self.checkBox = QCheckBox("   I hereby declare that the above information provided is true and correct.")
        self.checkBox.stateChanged.connect(self.onStageChanged)

        self.buttonLayout = QHBoxLayout()
        self.submit = QPushButton("Submit")
        self.reset = QPushButton("Reset")
        self.submit.setStyleSheet("margin-top: 15px; margin-bottom: 15px;")
        self.reset.setStyleSheet("margin-top: 15px; margin-bottom: 15px;")
        self.submit.setFixedWidth(BUTTON_WIDTH)
        self.reset.setFixedWidth(BUTTON_WIDTH)
        self.submit.setEnabled(False)
        self.submit.clicked.connect(self.addProfile)
        self.buttonLayout.addWidget(self.submit)
        self.buttonLayout.addWidget(self.reset)

        self.generalLayout.addLayout(self.formLayout)
        self.generalLayout.addWidget(self.checkBox)
        self.generalLayout.addLayout(self.buttonLayout)

    def showDropdown(self):
        self.popup = QWidget()
        self.popupLayout = QVBoxLayout()
        options = ["Drawing", "Decorating", "Playing", "Singing", "Others"]
        checkboxes = []

        for option in options:
            checkbox = QCheckBox(option)
            self.popupLayout.addWidget(checkbox)
            checkboxes.append(checkbox)

        close_button = QPushButton("Close Dropdown")
        close_button.clicked.connect(self.popup.close)
        self.popupLayout.addWidget(close_button)

        combobox_bottom_left = self.hobbyEdit.geometry().bottomLeft()
        self.popup.setGeometry(combobox_bottom_left.x(), combobox_bottom_left.y() + self.hobbyEdit.height(), self.popup.sizeHint().width(), self.popup.sizeHint().height())
        self.popup.show()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.dateEdit.rect().contains(self.dateEdit.mapFromGlobal(event.globalPosition()).toPoint()):
                global_pos = self.dateEdit.mapToGlobal(self.dateEdit.rect().bottomLeft())
                self.calendar.move(global_pos)
                self.calendar.show()
            else:
                self.calendar.hide()
            
    def onDateSelected(self):
        self.selectedDate = self.calendar.selectedDate().toString("yyyy-MM-dd")
        self.dateEdit.setText(self.selectedDate)
        
    def onStageChanged(self, state):
        if state == 2:
            self.submit.setEnabled(True)
        else:
            self.submit.setEnabled(False)
            
    def onToggled(self):
        if self.maleSelect.isChecked():
            self.gender = "male"
        elif self.femaleSelect.isChecked():
            self.gender = "female"
            
    def uploadImage(self):
        imagePath, _ = QFileDialog.getOpenFileName(self, 'Open Image File', '', 'Image Files (*.png *.jpg *.bmp)')
        
        if imagePath:
            pixmap = QPixmap(imagePath)
            self.photoUploadLabel.setPixmap(pixmap)

            with open(imagePath, 'rb') as file:
                self.imageData = file.read()

            
    def addProfile(self):
        if self.submit.isEnabled:
            self.loadDatabase()
            self.c.execute("""
                    INSERT INTO students (first_name, last_name, gender, date_of_birth, age, email, password, phone_no, address, hobbies, photo)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (self.firstName, self.lastName, self.gender, self.selectedDate, self.age, self.email, self.password, self.phoneNo, self.address, self.hobbies, self.imageData,))
            self.mydb.commit()
            self.mydb.close()
        
def main():
    app = QApplication(sys.argv)
    form = MyForm()
    form.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
