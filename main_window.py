from PyQt5.QtWidgets import (QMainWindow, QWidget, QTextEdit, QVBoxLayout, QGridLayout, QPushButton)
from PyQt5 import QtCore
from calc.parse import CalcTree, InvalidCalcString, InvalidDivisor


class MainWindow(QMainWindow):
    input_str = None
    cur_num = None
    calculated = False
    cur_operator = None
    err_msg = None
    Default_err_msg = '#Err#'

    def __init__(self):
        QMainWindow.__init__(self)
        self.calculator = CalcTree()

        widget = QWidget()

        self.input_str = []
        self.cur_num = []

        main_box = QVBoxLayout()
        self.display_area = QTextEdit(readOnly=True)
        keyboard = QGridLayout()

        self.display_area.setFixedHeight(50)

        self.button_clear = QPushButton('C')
        self.button_sign = QPushButton('+/-')
        self.button_percent = QPushButton('%')

        self.button_dot = QPushButton('.')
        self.button_0 = QPushButton('0')
        self.button_1 = QPushButton('1')
        self.button_2 = QPushButton('2')
        self.button_3 = QPushButton('3')
        self.button_4 = QPushButton('4')
        self.button_5 = QPushButton('5')
        self.button_6 = QPushButton('6')
        self.button_7 = QPushButton('7')
        self.button_8 = QPushButton('8')
        self.button_9 = QPushButton('9')

        self.button_plus = QPushButton('+')
        self.button_minus = QPushButton('-')
        self.button_mul = QPushButton('x')
        self.button_div = QPushButton('/')
        self.button_run = QPushButton('=')

        keyboard.addWidget(self.button_clear, 0, 0)
        keyboard.addWidget(self.button_sign, 0, 1)
        keyboard.addWidget(self.button_percent, 0, 2)
        keyboard.addWidget(self.button_plus, 0, 3)
        keyboard.addWidget(self.button_7, 1, 0)
        keyboard.addWidget(self.button_8, 1, 1)
        keyboard.addWidget(self.button_9, 1, 2)
        keyboard.addWidget(self.button_minus, 1, 3)
        keyboard.addWidget(self.button_4, 2, 0)
        keyboard.addWidget(self.button_5, 2, 1)
        keyboard.addWidget(self.button_6, 2, 2)
        keyboard.addWidget(self.button_mul, 2, 3)
        keyboard.addWidget(self.button_1, 3, 0)
        keyboard.addWidget(self.button_2, 3, 1)
        keyboard.addWidget(self.button_3, 3, 2)
        keyboard.addWidget(self.button_div, 3, 3)
        keyboard.addWidget(self.button_0, 4, 0, 1, 2)
        keyboard.addWidget(self.button_dot, 4, 2)
        keyboard.addWidget(self.button_run, 4, 3)

        self.set_listeners()

        main_box.addWidget(self.display_area)
        main_box.addLayout(keyboard)
        widget.setLayout(main_box)
        self.setCentralWidget(widget)

    def button_0_on_click(self):
        self.click_number('0')

    def button_1_on_click(self):
        self.click_number('1')

    def button_2_on_click(self):
        self.click_number('2')

    def button_3_on_click(self):
        self.click_number('3')

    def button_4_on_click(self):
        self.click_number('4')

    def button_5_on_click(self):
        self.click_number('5')

    def button_6_on_click(self):
        self.click_number('6')

    def button_7_on_click(self):
        self.click_number('7')

    def button_8_on_click(self):
        self.click_number('8')

    def button_9_on_click(self):
        self.click_number('9')

    def button_dot_on_click(self):
        self.click_number('.')

    def button_plus_on_click(self):
        self.click_operator('+')

    def button_minus_on_click(self):
        self.click_operator('-')

    def button_mul_on_click(self):
        self.click_operator('x')

    def button_div_on_click(self):
        self.click_operator('/')

    def button_clear_on_click(self):
        self.input_str.clear()
        self.cur_num.clear()
        self.err_msg = None
        self.refresh_display_area()

    def button_percent_on_click(self):
        if self.cur_num is None or len(self.cur_num) == 0 or self.cur_num[-1] == '.':
            return
        n = ''.join(self.cur_num)
        n = str(float(n) / 100)
        self.set_current_number(n)
        self.refresh_display_area()

    def button_sign_on_click(self):
        if len(self.cur_num) == 0 or (len(self.cur_num) == 1 and self.cur_num[0] == '0'):
            return
        n = ''.join(self.cur_num)
        if n.startswith('-'):
            n = n[1:]
        else:
            n = '-' + n
        self.set_current_number(n)
        self.refresh_display_area()

    def button_run_on_click(self):
        if len(self.cur_num) > 0:
            self.input_str.append(''.join(self.cur_num))
        else:
            return
        n = ''.join(self.input_str).replace('x', '*')
        r = None
        try:
            r = self.calculator.calculate(n)
        except InvalidCalcString:
            r = n
        except InvalidDivisor:
            self.err_msg = self.Default_err_msg
        if r:
            r = str(r)
            self.set_current_number(r)
        self.input_str.clear()
        self.calculated = True
        self.cur_operator = None
        self.refresh_display_area()

    def click_number(self, c):
        if self.calculated:
            self.cur_num.clear()
            self.calculated = False
        if c == '.':
            if '.' in self.cur_num:
                return
            else:
                if len(self.cur_num) == 0:
                    self.cur_num.append('0')
                self.cur_num.append(c)
        else:
            self.cur_num.append(c)
        self.err_msg = None
        self.refresh_display_area()

    def click_operator(self, c):
        if len(self.cur_num) == 0:
            return
        self.input_str.append(''.join(self.cur_num))
        self.input_str.append(c)
        self.cur_operator = c
        self.cur_num.clear()
        self.refresh_display_area()

    def refresh_display_area(self):
        if self.err_msg:
            display_text = self.err_msg
        else:
            display_num = ''.join(self.cur_num)
            if self.calculated:
                # remove unnecessary tailing zeroes
                if '.' in display_num:
                    display_num = display_num.rstrip('0')
                    if display_num[-1] == '.':
                        display_num = display_num[:-1]
            if '-' in display_num and self.cur_operator == '-':
                display_num = '(' + display_num + ')'
            display_text = ''.join(self.input_str) + display_num
        self.display_area.setText(display_text)
        self.display_area.setAlignment(QtCore.Qt.AlignRight)
        self.display_area.repaint()

    def set_current_number(self, s):
        i = 0
        self.cur_num.clear()
        while i < len(s):
            self.cur_num.append(s[i])
            i += 1

    def set_listeners(self):
        self.button_0.clicked.connect(self.button_0_on_click)
        self.button_1.clicked.connect(self.button_1_on_click)
        self.button_2.clicked.connect(self.button_2_on_click)
        self.button_3.clicked.connect(self.button_3_on_click)
        self.button_4.clicked.connect(self.button_4_on_click)
        self.button_5.clicked.connect(self.button_5_on_click)
        self.button_6.clicked.connect(self.button_6_on_click)
        self.button_7.clicked.connect(self.button_7_on_click)
        self.button_8.clicked.connect(self.button_8_on_click)
        self.button_9.clicked.connect(self.button_9_on_click)
        self.button_dot.clicked.connect(self.button_dot_on_click)
        self.button_plus.clicked.connect(self.button_plus_on_click)
        self.button_minus.clicked.connect(self.button_minus_on_click)
        self.button_mul.clicked.connect(self.button_mul_on_click)
        self.button_div.clicked.connect(self.button_div_on_click)
        self.button_clear.clicked.connect(self.button_clear_on_click)
        self.button_sign.clicked.connect(self.button_sign_on_click)
        self.button_run.clicked.connect(self.button_run_on_click)
        self.button_percent.clicked.connect(self.button_percent_on_click)

    # key press events
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_1:
            self.button_1_on_click()
        elif event.key() == QtCore.Qt.Key_2:
            self.button_2_on_click()
        elif event.key() == QtCore.Qt.Key_3:
            self.button_3_on_click()
        elif event.key() == QtCore.Qt.Key_4:
            self.button_4_on_click()
        elif event.key() == QtCore.Qt.Key_5:
            self.button_5_on_click()
        elif event.key() == QtCore.Qt.Key_6:
            self.button_6_on_click()
        elif event.key() == QtCore.Qt.Key_7:
            self.button_7_on_click()
        elif event.key() == QtCore.Qt.Key_8:
            self.button_8_on_click()
        elif event.key() == QtCore.Qt.Key_9:
            self.button_9_on_click()
        elif event.key() == QtCore.Qt.Key_0:
            self.button_0_on_click()
        elif event.key() == QtCore.Qt.Key_Plus:
            self.button_plus_on_click()
        elif event.key() == QtCore.Qt.Key_Minus:
            self.button_minus_on_click()
        elif event.key() == QtCore.Qt.Key_multiply or event.key() == QtCore.Qt.Key_Asterisk:
            self.button_mul_on_click()
        elif event.key() == QtCore.Qt.Key_Slash or event.key() == QtCore.Qt.Key_division:
            self.button_div_on_click()
        elif event.key() == QtCore.Qt.Key_Percent:
            self.button_percent_on_click()
        elif event.key() == QtCore.Qt.Key_Return:
            self.button_run_on_click()
        elif event.key() == QtCore.Qt.Key_Period:
            self.button_dot_on_click()
