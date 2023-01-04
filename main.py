from GUI import GUI, QApplication
import sys

def main():

    app = QApplication([])
    window = GUI()
    app.exec_()
    
if __name__ == '__main__':
    main()
