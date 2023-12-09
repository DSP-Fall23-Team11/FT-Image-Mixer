from PyQt5 import QtWidgets, uic, QtCore
import sys

class ImageView(QtWidgets.QGraphicsView):
    doubleClick = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: black;")  # Set the background color to black

        # Disable scroll bars and menus
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)

    def mouseDoubleClickEvent(self, event):
        self.doubleClick.emit()  # Emit the signal on double-click event
        super().mouseDoubleClickEvent(event)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('mainwindow.ui', self)
        self.originalImage3 = ImageView()
        self.init_connectors()
        self.setCentralWidget(self.originalImage3)  # Set the ImageView as central widget

    def init_connectors(self):
        if self.originalImage3:
            self.originalImage3.doubleClick.connect(self.browseFile)
        else:
            print("Widget 'originalImage3' not found.")

    def browseFile(self):
        print("Double-clicked, invoking browse function")

def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
