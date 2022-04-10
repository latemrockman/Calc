import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from form import *
from typing import Union, Optional
from operator import add, sub,mul,truediv

operations = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": truediv}

default_font_size = 16
default_entry_font_size = 40

error_zero_div = "Divizion by zero"
error_undefined = "Result is underfined"

class MyWin(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.lineEdit.setText("0")
        self.entry_max_len = self.ui.lineEdit.maxLength()

        self.ui.btn0.clicked.connect(self.add_digit)
        self.ui.btn1.clicked.connect(self.add_digit)
        self.ui.btn2.clicked.connect(self.add_digit)
        self.ui.btn3.clicked.connect(self.add_digit)
        self.ui.btn4.clicked.connect(self.add_digit)
        self.ui.btn5.clicked.connect(self.add_digit)
        self.ui.btn6.clicked.connect(self.add_digit)
        self.ui.btn7.clicked.connect(self.add_digit)
        self.ui.btn8.clicked.connect(self.add_digit)
        self.ui.btn9.clicked.connect(self.add_digit)

        # кнопки действия
        self.ui.btn_back.clicked.connect(self.back)
        self.ui.btn_ce.clicked.connect(self.clear_all)
        self.ui.btn_comma.clicked.connect(self.add_point)
        self.ui.btn_sign.clicked.connect(self.negate)

        # кнопки операции
        self.ui.btn_plus.clicked.connect(self.add_temp)
        self.ui.btn_minus.clicked.connect(self.add_temp)
        self.ui.btn_mult.clicked.connect(self.add_temp)
        self.ui.btn_div.clicked.connect(self.add_temp)

        self.ui.btn_eq.clicked.connect(self.calculate)

    def add_digit(self):
        btn = self.sender()
        digit_buttons = ("btn0","btn1","btn2","btn3","btn4","btn5","btn6","btn7","btn8","btn9")
        self.clear_temp_if_eqality()
        if btn.objectName() in digit_buttons:
            if self.ui.lineEdit.text() == "0":
                self.ui.lineEdit.setText(btn.text())
            else:
                self.ui.lineEdit.setText(self.ui.lineEdit.text() + btn.text())
    def back(self):
        self.remove_error()
        self.clear_temp_if_eqality()
        self.text = self.ui.lineEdit.text()
        if self.text != "0":
            self.ui.lineEdit.setText(self.text[:-1])
        if len(self.text) == 1:
            self.ui.lineEdit.setText("0")
        if len(self.text) == 2 and "-" in self.text:
            self.ui.lineEdit.setText("0")
    def clear_all(self):
        self.remove_error()
        self.ui.lineEdit.setText("0")
        self.ui.label.clear()
    def add_point(self):
        self.clear_temp_if_eqality()
        if not "." in self.ui.lineEdit.text():
            self.ui.lineEdit.setText(self.ui.lineEdit.text() + ".")
    @staticmethod
    def remove_trailing_zeros(num: str) -> str:
        n = str(float(num))
        return n[:-2] if n[-2:] == ".0" else n
    def add_temp(self) -> None:
        btn = self.sender()
        entry = self.remove_trailing_zeros(self.ui.lineEdit.text())

        if not self.ui.label.text() or self.get_math_sign() == "=":
            self.ui.label.setText(entry + f" {btn.text()} ")
            self.ui.lineEdit.setText("0")
    def get_entry_num(self) -> Union[int,float]:
        self.remove_error()
        entry = self.ui.lineEdit.text().strip(".")
        return float(entry) if "." in entry else int(entry)
    def get_temp_num(self) -> Union[int,float,None]:
        if self.ui.label.text():
            temp = self.ui.label.text().strip(".").split()[0]
            return float(temp) if "." in temp else int(temp)
    def get_math_sign(self) -> Optional[str]:
        if self.ui.label.text():
            return self.ui.label.text().strip(".").split()[-1]
    def get_entry_text_width(self) -> int:
        return self.ui.lineEdit.fontmetrics().boundingRect(self.ui.lineEdit.text().width())
    def calculate(self) -> Optional[str]:
        entry = self.ui.lineEdit.text()
        temp = self.ui.label.text()

        #if "=" in temp:
        #    return

        if temp:
            try:
                result = self.remove_trailing_zeros(
                    str(operations[self.get_math_sign()](self.get_temp_num(), self.get_entry_num())))
                self.ui.label.setText(temp + self.remove_trailing_zeros(entry) + " =")
                self.ui.lineEdit.setText(result)
                return result

            except KeyError:
                pass

            except ZeroDivisionError:
                if self.get_temp_num() == "0":
                    self.show_error(error_inderfined)
                else:
                    self.show_error(error_zero_div)
    def math_operation(self) -> None:
        temp = self.ui.label.text()
        btn = self.sender()

        if not temp:
            self.add_temp()
        else:
            if self.get_math_sign() != btn.text():
                if self.get_math_sign() == "=":
                    self.add_temp()
                else:
                    self.ui.label.setText(temp[:-2] + f"{btn.text()} ")
            else:
                self.ui.label.setText(self.calculate() + f" {btn.text()}")
    def negate(self):
        entry = self.ui.lineEdit.text()

        if not "-" in entry:
            if entry != "0":
                entry = "-" + entry
        else:
            entry = entry[1:]

        if len(entry) == self.entry_max_len + 1 and "-" in entry:
            self.ui.lineEdit.setMaxLength(self.entry_max_len + 1)
        else:
            self.ui.lineEdit.setMaxLength(self.entry_max_len)


        self.ui.lineEdit.setText(entry)
    def clear_temp_if_eqality(self) -> None:
        if self.get_math_sign() == "=":
            self.ui.label.clear()
    def show_error(self, text: str) -> None:
        self.ui.lineEdit.setMaxLength(len(text))
        self.ui.lineEdit.setText(text)
        self.disable_buttons(True)
    def remove_error(self) -> None:
        if self.ui.lineEdit.text() in (error_zero_div, error_undefined):
            self.ui.lineEdit.setMaxLength(self.entry_max_len)
            self.ui.lineEdit.setText("0")
            self.disable_buttons(False)
    def disable_buttons(self,disable: bool) -> None:
        self.ui.btn_plus.setDisabled(disable)
        self.ui.btn_minus.setDisabled(disable)
        self.ui.btn_mult.setDisabled(disable)
        self.ui.btn_div.setDisabled(disable)
        self.ui.btn_comma.setDisabled(disable)
        self.ui.btn_sign.setDisabled(disable)

        color = "color: #888;" if disable else "color: white;"

        self.change_button_color(color)
    def change_button_color(self,css_color:str) -> None:
        self.ui.btn_plus.setStyleSheet(css_color)
        self.ui.btn_minus.setStyleSheet(css_color)
        self.ui.btn_mult.setStyleSheet(css_color)
        self.ui.btn_div.setStyleSheet(css_color)
        self.ui.btn_comma.setStyleSheet(css_color)
        self.ui.btn_sign.setStyleSheet(css_color)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())