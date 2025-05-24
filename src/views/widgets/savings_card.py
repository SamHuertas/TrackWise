from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFrame, QGridLayout, QLabel, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QProgressBar
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, pyqtSignal
from pathlib import Path

class SavingsGoalWidget(QFrame):
    deposit_requested = pyqtSignal(int)  # Signal for deposit action
    delete_requested = pyqtSignal(int)  # Signal for delete action

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(Path("src/styles/SavingCardStyle.qss").read_text())
        self.setMaximumHeight(180)
        
        # Create layout
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(8, 8, 8, 8)
        self.grid.setHorizontalSpacing(0)
        self.grid.setVerticalSpacing(3)

        # Create widgets with default values
        # Name label
        self.name_label = QLabel("New Goal")
        self.name_label.setObjectName("NameL")
        font = QFont()
        font.setPointSize(12)
        self.name_label.setFont(font)
        self.grid.addWidget(self.name_label, 0, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        # Amount label
        self.amount_label = QLabel("₱0.00")
        self.amount_label.setObjectName("AmountL")
        font = QFont()
        font.setPointSize(15)
        self.amount_label.setFont(font)
        self.grid.addWidget(self.amount_label, 1, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        # Target label
        self.target_label = QLabel("of ₱0.00")
        self.target_label.setObjectName("TargetL")
        font = QFont()
        font.setPointSize(12)
        self.target_label.setFont(font)
        self.grid.addWidget(self.target_label, 1, 2, 1, 1, alignment=Qt.AlignmentFlag.AlignRight)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("ProgressBar")
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(8)
        self.grid.addWidget(self.progress_bar, 2, 0, 1, 3)

        # Action buttons
        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(8)
        self.button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        # Delete button
        self.delete_btn = QPushButton("")
        self.delete_btn.setObjectName("DeleteB")
        self.delete_btn.setFixedSize(28, 28)
        icon1 = QIcon()
        icon1.addPixmap(QPixmap("src/assets/trash.svg"), QIcon.Mode.Normal, QIcon.State.On)
        self.delete_btn.setIcon(icon1)
        self.delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_btn.clicked.connect(self.on_delete_clicked)
        self.button_layout.addWidget(self.delete_btn)

        # Deposit button
        self.deposit_btn = QPushButton("+ Deposit")
        self.deposit_btn.setObjectName("DepositB")
        self.button_layout.addWidget(self.deposit_btn)
        self.deposit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.deposit_btn.clicked.connect(self.on_deposit_clicked)
        
        self.grid.addLayout(self.button_layout, 3, 2, 1, 1, alignment=Qt.AlignmentFlag.AlignRight)

    def update_data(self, data):
        """Update the widget with new data"""
        # Update name
        self.name_label.setText(data['Name'].title())
        
        # Update amount and target
        self.amount_label.setText(f"₱{data['TotalDeposits']:,.2f}")
        self.target_label.setText(f"of ₱{data['Goal Amount']:,.2f}")
        
        # Update progress
        progress = (data['TotalDeposits'] / data['Goal Amount'] * 100) if data['Goal Amount'] > 0 else 0
        self.progress_bar.setValue(int(progress))
        
        # Store the savings ID for button actions
        self.savings_id = data['SavingsID']

    def on_deposit_clicked(self):
        self.deposit_requested.emit(self.savings_id)

    def on_delete_clicked(self):
        self.delete_requested.emit(self.savings_id)