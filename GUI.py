from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication
from PyQt5 import uic
from data import DataGetter

class GUI(QMainWindow):
    convert_intervals = {
        -3:'DAILY',
        -4:'WEEKLY',
        -5:'MONTHLY'
    }

    convert_intraday_intervals = {
        '1 Min':'1',
        '5 Min':'5',
        '15 Min':'15',
        '30 Min':'30',
        '60 Min':'60'
    }

    def __init__(self):
        super(GUI, self).__init__()
        uic.loadUi('interface.ui', self)
        self.show()

        self.submit_button.clicked.connect(self.canSubmit)
        self.actionQuit.triggered.connect(exit)

    def canSubmit(self):
        selected_interval = self.interval_group.checkedButton()
        if self.symbol_lineedit.text() != '' and selected_interval is not None:
            self.show_data()
        else:
            message = QMessageBox()
            message.setText('Please fill out all entries')
            message.exec_()

    def show_data(self):
        stock = self.symbol_lineedit.text()
        interval = self.interval_group.checkedId() #intraday = -2, daily = -3, weekly = -4, monthly = -5

        if interval == -2:
            interval = self.interval_options.currentText()
            interval = self.convert_intraday_intervals[interval]
        else:
            interval = self.convert_intervals[interval]

        high = self.high.isChecked()
        low = self.low.isChecked()

        data = DataGetter(stock, interval=interval, high=high, low=low)
        data.showPlot()