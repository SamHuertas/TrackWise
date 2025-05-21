from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFrame, QGridLayout, QLabel, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QProgressBar
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
from pathlib import Path

class SavingsGoalWidget(QFrame):
    def __init__(self, account, parent=None):
        super().__init__(parent)
        self.account = account
        self.setStyleSheet(Path("src/styles/SavingCardStyle.qss").read_text())
        self.setMaximumHeight(180)
        grid = QGridLayout(self)
        grid.setContentsMargins(8, 8, 8, 8)
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(6)

        # Name label (rounded)
        name_label = QLabel(self.account["name"])
        name_label.setObjectName("NameL")
        font = QFont()
        font.setPointSize(12)
        name_label.setFont(font)
        grid.addWidget(name_label, 0, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        # Amount (rounded, bold)
        amount_label = QLabel(f"${self.account['amount']:,.2f}")
        amount_label.setObjectName("AmountL")
        font = QFont()
        font.setPointSize(22)
        amount_label.setFont(font)
        grid.addWidget(amount_label, 1, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        # Target (rounded, right)
        target_label = QLabel(f"of ${self.account['target']:,.2f}")
        target_label.setObjectName("TargetL")
        font = QFont()
        font.setPointSize(12)
        target_label.setFont(font)
        grid.addWidget(target_label, 1, 2, 1, 1, alignment=Qt.AlignmentFlag.AlignRight)

        # QProgressBar (spans all columns)
        progress = self.account["progress"]
        progress_bar = QProgressBar()
        progress_bar.setObjectName("ProgressBar")
        progress_bar.setMinimum(0)
        progress_bar.setMaximum(100)
        progress_bar.setValue(int(progress))
        progress_bar.setTextVisible(False)
        progress_bar.setFixedHeight(8)
        grid.addWidget(progress_bar, 2, 0, 1, 3)

        # Action buttons (bottom right)
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        # Delete button
        delete_btn = QPushButton("")
        delete_btn.setObjectName("DeleteB")
        delete_btn.setFixedSize(28, 28)
        icon1 = QIcon()
        icon1.addPixmap(QPixmap("src/assets/trash.svg"), QIcon.Mode.Normal, QIcon.State.On)
        delete_btn.setIcon(icon1)
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        button_layout.addWidget(delete_btn)

        # Deposit button
        deposit_btn = QPushButton("+ Deposit")
        deposit_btn.setObjectName("DepositB")
        button_layout.addWidget(deposit_btn)
        deposit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        grid.addLayout(button_layout, 3, 2, 1, 1, alignment=Qt.AlignmentFlag.AlignRight) 