from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel, QVBoxLayout, QWidget, QSlider, QComboBox, QGraphicsRectItem
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QRectF
import sys
import logging
import numpy as np
import cv2
import time
import matplotlib.pyplot as plt
from ImageModel import ImageModel

#Local 
from storage import Storage

# Create and configure logger
logging.basicConfig(level=logging.DEBUG,
                    filename="app.log",
                    format='%(lineno)s - %(levelname)s - %(message)s',
                    filemode='w')

# Creating an object
logger = logging.getLogger()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('mainwindow.ui', self)
        self.inputImages = [self.originalImage1, self.originalImage2,self.originalImage3,self.originalImage4]
        self.ftComponentImages = [self.ftComponent1, self.ftComponent2,self.ftComponent3,self.ftComponent4]
        self.outputImages = [self.outputImage1, self.outputImage2]
        self.imagesModels = [..., ... , ... , ... ]
        self.imageWidgets = [self.originalImage1, self.originalImage2, self.originalImage3, self.originalImage4, self.ftComponent1, self.ftComponent2,
                             self.ftComponent3,self.ftComponent4,
                             self.outputImage1, self.outputImage2]
        self.heights = [..., ... , ... , ...]
        self.weights = [..., ... , ... , ...]
        self.myStorage = Storage(self.imagesModels)
        self.allComboBoxes=[self.ftComponentMenu1,self.ftComponentMenu2,self.ftComponentMenu3,self.ftComponentMenu4]
        self.brightnessSliders=[self.brightnessSlider1,self.brightnessSlider2,self.brightnessSlider3,self.brightnessSlider4]
        self.contrastSliders=[self.contrastSlider1,self.contrastSlider2,self.contrastSlider3,self.contrastSlider4]
        for i in range(4):
            self.contrastSliders[i].setMaximum(150)
            self.contrastSliders[i].setMinimum(10)
            self.contrastSliders[i].setValue(100)
            self.brightnessSliders[i].setMaximum(75)
            self.brightnessSliders[i].setMinimum(-75)
            self.brightnessSliders[i].setValue(0)
        init_connectors(self)
        self.setupImagesView()

    def loadFile(self, imgID):
            self.filename, self.format = QtWidgets.QFileDialog.getOpenFileName(None, "Load Image",
                                                                            "*.jpg;;" "*.jpeg;;" "*.png;;")
            imgName = self.filename.split('/')[-1] # for Logging
            if self.filename == "":
                return 
            image = cv2.imread(self.filename, flags=cv2.IMREAD_GRAYSCALE).T
            self.imagesModels[imgID] = ImageModel(self.filename)
           # self.heights[imgID], self.weights[imgID] = image.shape
            # self.myStorage = Storage(self.imagesModels)
            self.myStorage.setImageModels(self.imagesModels)
            self.myStorage.unifyImagesSize()
            self.displayImage(self.imagesModels[imgID].imgByte, self.inputImages[imgID])
            for i, img in enumerate(self.imagesModels):
                 if type(img)!=type(...):
                      print("ana "+str(i+1),img.imgShape)
                      self.displayImage(self.imagesModels[i].imgByte, self.inputImages[i])
                    #   cv2.imwrite("output_image"+str(i+1)+".jpg", img.imgByte)
                      self.inputImages[i].export("mama"+str(i)+".jpg")

    def setupImagesView(self):
        for widget in self.imageWidgets:
            widget.ui.histogram.hide()
            widget.ui.roiBtn.hide()
            widget.ui.menuBtn.hide()
            widget.ui.roiPlot.hide()
            widget.getView().setAspectLocked(False)
            widget.view.setAspectLocked(False)      

    def displayImage(self, data, widget):
                widget.setImage(data)
                #widget.view.setRange(xRange=[0, self.imagesModels[0].imgShape[0]], yRange=[0, self.imagesModels[0].imgShape[1]],
                #                    padding=0)
                widget.ui.roiPlot.hide()            
    def on_mouse_click(self,idx):
            print("Double-clicked!"+str(idx))
            self.loadFile(idx)
            self.enableOutputCombos(idx)
    def enableOutputCombos(self,index):
        self.allComboBoxes[index].setEnabled(True)            
    def applyFtComponents(self,idx):
        selectedComponent = self.allComboBoxes[idx].currentIndex()
        fShift = np.fft.fftshift(self.imagesModels[idx].dft)
        magnitude = 20 * np.log(np.abs(fShift))
        phase = np.angle(fShift)
        real = 20 * np.log(np.real(fShift))
        imaginary = np.imag(fShift)
        FtComponentsData = [magnitude,phase,real,imaginary]
        self.displayImage(FtComponentsData[selectedComponent],self.ftComponentImages[idx])


def init_connectors(self):
    self.originalImage1.mouseDoubleClickEvent = lambda event, idx=0: self.on_mouse_click(idx)
    self.originalImage2.mouseDoubleClickEvent = lambda event, idx=1: self.on_mouse_click(idx)
    self.originalImage3.mouseDoubleClickEvent = lambda event, idx=2: self.on_mouse_click(idx)
    self.originalImage4.mouseDoubleClickEvent = lambda event, idx=3: self.on_mouse_click(idx)
    for i in range(4):
        self.brightnessSliders[i].sliderReleased.connect(lambda i=i: ImageModel.editedImage(self,self.imagesModels[i],\
        self.inputImages[i],self.brightnessSliders[i].value()/100,self.contrastSliders[i].value()/100))
        self.contrastSliders[i].sliderReleased.connect(lambda i=i: ImageModel.editedImage(self,self.imagesModels[i],\
        self.inputImages[i],self.brightnessSliders[i].value()/100,self.contrastSliders[i].value()/100))
    self.ftComponentMenu1.activated.connect(lambda: self.applyFtComponents(0))
    self.ftComponentMenu2.activated.connect(lambda: self.applyFtComponents(1))
    self.ftComponentMenu3.activated.connect(lambda: self.applyFtComponents(2))
    self.ftComponentMenu4.activated.connect(lambda: self.applyFtComponents(3))


def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
