from PyQt6.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QProgressBar
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QSize
from pathlib import Path

class DashboardSavingsCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DashboardSavingsCard")
        self.setStyleSheet(Path("src/styles/DashboardSavingsCardStyle.qss").read_text())

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(8, 4, 8, 4)
        main_layout.setSpacing(12)

        # Texts (Goal Name, Progress)
        text_layout = QVBoxLayout()
        text_layout.setSpacing(0)
        text_layout.setContentsMargins(0, 0, 0, 0)
        self.goal_label = QLabel("Goal Name")
        self.goal_label.setObjectName("title_label")
        self.amount_label = QLabel("₱0.00")
        self.amount_label.setObjectName("amount_label")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(80)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(5)
        self.progress_bar.setObjectName("progress_bar")
        percent_row = QHBoxLayout()
        self.percent_label = QLabel("80% complete")
        self.percent_label.setObjectName("percentage_label")
        self.target_label = QLabel("Target: ₱0.00")
        self.target_label.setObjectName("target_label")
        percent_row.addWidget(self.percent_label)
        percent_row.addStretch()
        percent_row.addWidget(self.target_label)
        text_layout.addWidget(self.goal_label)
        text_layout.addWidget(self.amount_label)
        text_layout.addWidget(self.progress_bar)
        text_layout.addLayout(percent_row)
        main_layout.addLayout(text_layout)

        self.setLayout(main_layout)

    def update_data(self, data):
        self.goal_label.setText(data['Name'].title())
        percent = int((data['TotalDeposits'] / data['Goal Amount']) * 100) if data['Goal Amount'] else 0
        self.percent_label.setText(f"{percent}% complete")
        self.amount_label.setText(f"₱{data['TotalDeposits']:,.2f}")
        self.target_label.setText(f"Target: ₱{data['Goal Amount']:,.2f}")
        self.progress_bar.setValue(percent)
