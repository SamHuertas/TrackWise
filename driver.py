from PyQt6.QtWidgets import QApplication 
from views.main_window import MainWindow

def main():
    application = QApplication([])
    application_window = MainWindow()
    application_window.show()
    application.exec()

if __name__ == "__main__":
    main()