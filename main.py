from GUI import GUI, QApplication

def main():

    app = QApplication([])
    window = GUI()
    app.exec_()
    
if __name__ == '__main__':
    main()
