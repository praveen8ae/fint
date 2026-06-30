
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

class BankWindow(QWidget):
    def __init__(self, db, username):
        super().__init__()
        self.db=db; self.username=username
        self.setWindowTitle("Fint")
        self.resize(1200,900); self.setMinimumSize(900,700)
        self.setStyleSheet("""
        QWidget{background:#0D1117;color:#E6EDF3;font-family:Arial;}
        QPushButton{background:#21262D;border-radius:14px;padding:14px;color:white;}
        QListWidget,QTextEdit{background:#161B22;border-radius:14px;}
        """)
        root=QVBoxLayout(self)
        top=QHBoxLayout()
        m=QPushButton("☰"); m.clicked.connect(self.toggle_drawer)
        t=QLabel("Welcome"); t.setStyleSheet("font-size:28px;font-weight:bold;")
        u=QPushButton("👤"); u.clicked.connect(self.show_user_menu)
        top.addWidget(m); top.addWidget(t); top.addStretch(); top.addWidget(u)
        root.addLayout(top)

        body=QHBoxLayout()
        self.drawer=QListWidget(); self.drawer.addItems(["Savings Account","Analysis","History"]); self.drawer.hide()
        body.addWidget(self.drawer)

        main=QVBoxLayout()
        self.balance=QLabel(); self.balance.setStyleSheet("font-size:42px;font-weight:bold;")
        self.refresh()
        main.addWidget(self.balance)

        dep=QPushButton("Deposit"); dep.clicked.connect(self.deposit)
        wd=QPushButton("Withdraw"); wd.clicked.connect(self.withdraw)
        main.addWidget(dep); main.addWidget(wd)

        self.hist=QTextEdit(); self.hist.setReadOnly(True)
        main.addWidget(self.hist)
        self.load_history()

        body.addLayout(main)
        root.addLayout(body)

    def toggle_drawer(self): self.drawer.setVisible(not self.drawer.isVisible())

    def show_user_menu(self):
        menu=QMenu(self)
        act=menu.addAction("Logout")
        if menu.exec(self.cursor().pos()) == act:
            from ui.login import LoginWindow
            self.l=LoginWindow(self.db); self.l.show(); self.close()

    def refresh(self):
        self.balance.setText(f"Balance: ${self.db.get_balance(self.username):,.2f}")

    def deposit(self):
        amt,ok=QInputDialog.getDouble(self,"Deposit","Amount:",0,0)
        if ok and amt>0:
            b=self.db.get_balance(self.username)+amt
            self.db.update_balance(self.username,b); self.db.add_history("Deposit",amt)
            self.refresh(); self.load_history()

    def withdraw(self):
        amt,ok=QInputDialog.getDouble(self,"Withdraw","Amount:",0,0)
        if ok and amt>0:
            bal=self.db.get_balance(self.username)
            if bal-amt<10000:
                QMessageBox.warning(self,"No Balance","No balance"); return
            self.db.update_balance(self.username, bal-amt); self.db.add_history("Withdraw",amt)
            self.refresh(); self.load_history()

    def load_history(self):
        self.hist.setText("\n".join([f"{t} | {a}: ${amt}" for a,amt,t in self.db.get_history()]))
