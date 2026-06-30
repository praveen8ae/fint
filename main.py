
import sys
from PySide6.QtWidgets import QApplication
from ui.login import LoginWindow
from database import BankDB

db = BankDB()

app = QApplication(sys.argv)
window = LoginWindow(db)
window.show()
sys.exit(app.exec())
