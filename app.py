from PyQt5.QtWidgets import QApplication
from main_window import MainWindow


class App:

    def __init__(self):
        self.app = QApplication([])
        self.window = MainWindow()

    def run(self):
        self.window.show()
        self.app.exec_()


if __name__ == '__main__':
    app = App()
    app.run()

