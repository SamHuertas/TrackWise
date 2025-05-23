from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QSize
from pathlib import Path

class TransactionCard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("TransactionCard")
        self.setStyleSheet(Path("src/styles/TransactionCardStyle.qss").read_text())
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 0, 10, 0)
        main_layout.setSpacing(20)

        # Icon container (like ExpensesIcon)
        icon_widget = QWidget(self)
        icon_widget.setMinimumSize(QSize(39, 39))
        icon_widget.setMaximumSize(QSize(39, 39))
        icon_widget.setObjectName("icon_widget")
        icon_label = QLabel()
        icon_label.setGeometry(5, 5, 30, 30)
        icon_label.setText("")
        icon_label.setObjectName("icon_label")
        icon_label.setPixmap(QPixmap("src/assets/Tag.svg"))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(icon_widget)

        # Texts (Category, Description)
        text_layout = QVBoxLayout()
        text_layout.setSpacing(0)
        self.category_label = QLabel("Category")                     ##input
        self.category_label.setObjectName("category_label")
        self.description_label = QLabel("Description")               ##input
        self.description_label.setObjectName("description_label")
        text_layout.addWidget(self.category_label)
        text_layout.addWidget(self.description_label)
        main_layout.addLayout(text_layout)

        # Spacer
        main_layout.addStretch(1)

        # Amount and Date
        right_layout = QVBoxLayout()
        right_layout.setSpacing(0)
        self.amount_label = QLabel(f"-₱0.00")                         ##input 
        self.amount_label.setObjectName("amount_label")
        self.amount_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.date_label = QLabel("2023-10-01")                        ##input
        self.date_label.setObjectName("date_label")
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        right_layout.addWidget(self.amount_label)
        right_layout.addWidget(self.date_label)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

    def update_data(self, data):
        # Update the card with new data
        self.category_label.setText(data['Category'])
        self.description_label.setText(data['Description'])
        self.amount_label.setText(f"-₱{data['Amount']:.2f}")
        # Ensure date is a string
        date_str = str(data['Date'])
        self.date_label.setText(date_str)
