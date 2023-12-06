from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import Qt
import sys


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('mainwindow.ui', self)
        self.init_connectors()
        self.currentfile = "ashf2.jfif"
        pixmap = QtGui.QPixmap("ashf2.jfif")
        pixmap = pixmap.scaled(self.width(), self.height(), aspectRatioMode=Qt.KeepAspectRatio)
        self.originalImage.setPixmap(pixmap)
        self.originalImage.setMinimumSize(1, 1)
        self.phaseImage.setPixmap(pixmap)
        self.phaseImage.setMinimumSize(1, 1)
        self.magnitudeImage.setPixmap(pixmap)
        self.magnitudeImage.setMinimumSize(1, 1)
        self.greyScaledImage.setPixmap(pixmap)
        self.greyScaledImage.setMinimumSize(1, 1)





    def changeContrast(self):
       print(self.contrastSlider.value())

    # def resizeEvent(self, event):
    #     try:
    #         pixmap = QtGui.QPixmap(self.currentfile)
    #     except:
    #         pixmap = QtGui.QPixmap("ashf2.jfif")
    #     pixmap =pixmap.scaled(self.width(), self.height(), aspectRatioMode=Qt.KeepAspectRatio)
    #     self.label.setPixmap(pixmap)
    #     self.label.resize(self.width(), self.height())
    
    def init_connectors(self):
       self.contrastSlider.sliderReleased.connect(self.changeContrast)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
