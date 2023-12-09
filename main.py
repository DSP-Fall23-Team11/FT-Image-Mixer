from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QSlider, QComboBox, QGraphicsRectItem,QGraphicsView,QGraphicsScene
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QObject
import sys
import logging
import numpy as np
import cv2 
import matplotlib.pyplot as plt

# class ImageView(QGraphicsView):
#     doubleClick = pyqtSignal()

#     def __init__(self):
#         print("ImageView initialized")
#         super().__init__()        



#     def mouseDoubleClickEvent(self, event):
#         print("Double-click event detected")
#         self.doubleClick.emit()  
#         super().mouseDoubleClickEvent(event)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('mainwindow.ui', self)
        self.init_connectors()        

        image = cv2.imread("other\mask.jpeg")
        imageArr = np.asarray(image)
        self.displayImage(imageArr,self.originalImage3)

    
    def displayImage(self, data, widget):
        widget.setImage(data)
        widget.ui.roiBtn.hide()
        widget.ui.menuBtn.hide()
        widget.ui.histogram.hide()
        widget.ui.roiPlot.setVisible(False)  
        widget.update()
        widget.doubleClick.connect(self.browseFile)
        
    def init_connectors(self):
        pass
    def browseFile(self):
        print("yala ba2a pliz")

def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
