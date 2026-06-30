
from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QLineEdit,QPushButton,QMessageBox
from PySide6.QtCore import Qt
from ui.dashboard import BankWindow

class LoginWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db=db
        self.setWindowTitle("Fint Login")
        self.resize(420,300)
        layout=QVBoxLayout(self)
        title=QLabel("Fint"); title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:40px;font-weight:bold;")
        self.u=QLineEdit(); self.u.setPlaceholderText("Username")
        self.p=QLineEdit(); self.p.setPlaceholderText("Password"); self.p.setEchoMode(QLineEdit.Password)
        b=QPushButton("Login"); b.clicked.connect(self.login)
        layout.addWidget(title); layout.addWidget(self.u); layout.addWidget(self.p); layout.addWidget(b)
    def login(self):
        if self.db.login(self.u.text(), self.p.text()):
            self.w=BankWindow(self.db, self.u.text())
            self.w.show()
            self.close()
        else:
            QMessageBox.warning(self,"Error","Invalid credentials")
