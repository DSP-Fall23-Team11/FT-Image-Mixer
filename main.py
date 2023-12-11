from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel, QVBoxLayout, QWidget, QSlider, QComboBox, QGraphicsRectItem,QGraphicsView,QGraphicsScene
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QColor,QMouseEvent
from PyQt5.QtCore import Qt, QRectF,pyqtSignal
import sys
import logging
import numpy as np
import cv2
import time
import matplotlib.pyplot as plt
from ImageModel import ImageModel
from ImageMixer import ImageMixer
from Modes import Modes
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
        self.myMixer   = ImageMixer()
        self.allComboBoxes=[self.ftComponentMenu1,self.ftComponentMenu2,self.ftComponentMenu3,self.ftComponentMenu4]
        self.outputComboBoxes = [self.outputComponentMenu1,self.outputComponentMenu2,self.outputComponentMenu3,self.outputComponentMenu4 ]
        self.outputRatioSliders = [self.componentWeightSlider1,self.componentWeightSlider2,self.componentWeightSlider3,self.componentWeightSlider4]
        self.brightnessSliders=[self.brightnessSlider1,self.brightnessSlider2,self.brightnessSlider3,self.brightnessSlider4]
        self.contrastSliders=[self.contrastSlider1,self.contrastSlider2,self.contrastSlider3,self.contrastSlider4]
        for i in range(4):
            self.contrastSliders[i].setMaximum(150)
            self.contrastSliders[i].setMinimum(10)
            self.contrastSliders[i].setValue(100)
            self.brightnessSliders[i].setMaximum(75)
            self.brightnessSliders[i].setMinimum(-75)
            self.brightnessSliders[i].setValue(0)
        self.x = None
        self.y = None
        self.trackIndex=0
        self.contrastFactor=1
        self.brightnessFactor=0
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
                    #  print("ana "+str(i+1),img.imgShape)
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
           # print("Double-clicked!"+str(idx))
            self.loadFile(idx)
            self.enableOutputCombos(idx)

    def enableOutputCombos(self,index):
        self.allComboBoxes[index].setEnabled(True)
        self.outputComboBoxes[index].setEnabled(True)
        self.outputRatioSliders[index].setEnabled(True)  

    def applyFtComponents(self,idx):
        selectedComponent = self.allComboBoxes[idx-1].currentIndex()
        fShift = np.fft.fftshift(self.imagesModels[idx-1].dft)
        magnitude = 20 * np.log(np.abs(fShift))
        phase = np.angle(fShift)
        real = 20 * np.log(np.real(fShift))
        imaginary = np.imag(fShift)
        FtComponentsData = [0*magnitude,magnitude,phase,real,imaginary]
        self.displayImage(FtComponentsData[selectedComponent],self.ftComponentImages[idx-1])
    def handleOutputCombosChange(self):
         pass
    def handleOutputCombos(self):
       print("mama")
       output  = ...
       outputIdx = self.outputChannelMenu.currentIndex()
      # currentMode = self.outputComboBoxes[0].currentText()
       selectedOutputComponents = [  i.currentText() for i in self.outputComboBoxes] 
       weights = [i.value() for  i in self.outputRatioSliders]
       self.myMixer.setWeights(weights)
       if selectedOutputComponents[0] == "Magnitude" or selectedOutputComponents[0] == "Phase":
            output = self.myMixer.mixImageModels(self.imagesModels, Modes.magnitudeAndPhase)
       elif selectedOutputComponents[0] == "Real"  or selectedOutputComponents[0] == "Imaginary":
            output = self.myMixer.mixImageModels(self.imagesModels, Modes.realAndImaginary)
       self.displayImage(output,self.outputImages[outputIdx])     
        # Mixer Logic IFFT    

    def mousePressEvent(self, event: QMouseEvent):

          for i in range(4):
            if (
                event.button() == Qt.MouseButton.RightButton
                and (self.inputImages[i].underMouse())    
            ):  

                self.inputImages[i].setEnabled(False)
                self.mouse_pressed = True
                self.trackIndex=i
                self.track_mouse_position(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        for i in range(4):
            if self.mouse_pressed and (self.inputImages[i].underMouse()): self.track_mouse_position(event)
            
    def track_mouse_position(self, event: QMouseEvent):
        # Track mouse position when clicking and holding on label1
        crrX, crrY = event.pos().x(), event.pos().y()
        # print(f"Mouse Position: ({crrX}, {crrY})")
        if self.x is None:
            self.x = crrX
            self.y = crrY
        else:
            if crrX - self.x > 1: #Right higher brightness 
                #print("Right")
                self.brightnessFactor+=0.05
                if self.brightnessFactor>0.75:
                    self.brightnessFactor=0.75
            elif crrX - self.x < -1: #Left Lower brightness
                #print("Left")
                self.brightnessFactor-=0.05
                if self.brightnessFactor<-0.75:
                    self.brightnessFactor=-0.75
            self.x = crrX
            if crrY - self.y > 1:
                self.contrastFactor-=0.05
                if self.contrastFactor<0.1:
                    self.contrastFactor=0.1
                #print("Down")
            elif crrY - self.y < -1:
                self.contrastFactor+=0.05
                if self.contrastFactor>1.5:
                    self.contrastFactor=1.5
                #print("Up")
            self.y = crrY
            ImageModel.editedImage(self,self.imagesModels[self.trackIndex],self.inputImages[self.trackIndex],self.brightnessFactor,self.contrastFactor,self.trackIndex)    
        # print(f"Mouse Position: ({self.x}, {self.y})")

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_pressed = False
                
            

             
    

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
    self.ftComponentMenu1.activated.connect(lambda: self.applyFtComponents(1))
    self.ftComponentMenu2.activated.connect(lambda: self.applyFtComponents(2))
    self.ftComponentMenu3.activated.connect(lambda: self.applyFtComponents(3))
    self.ftComponentMenu4.activated.connect(lambda: self.applyFtComponents(4))
    self.outputComponentMenu1.activated.connect(self.handleOutputCombos)
    self.outputComponentMenu2.activated.connect(self.handleOutputCombos)
    self.outputComponentMenu3.activated.connect(self.handleOutputCombos)
    self.outputComponentMenu4.activated.connect(self.handleOutputCombos)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
