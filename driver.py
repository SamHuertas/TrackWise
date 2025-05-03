import sys
from PyQt6.QtWidgets import QApplication
from views.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()  # Create an instance of your MainWindow
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()