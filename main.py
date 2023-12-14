from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel, QVBoxLayout, QWidget, QSlider, QComboBox, QGraphicsRectItem,QGraphicsView,QGraphicsScene
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QColor,QMouseEvent
from PyQt5.QtCore import Qt, QRectF,pyqtSignal,QFile,QTextStream
from PyQt5.QtCore import Qt, QRectF, QObject, pyqtSignal
import sys
import logging
import pyqtgraph as pg
import numpy as np
import cv2
import time
import matplotlib.pyplot as plt
from ImageModel import ImageModel
from ImageMixer import ImageMixer
from Modes import Modes
#Local 
from storage import Storage
from ViewFt import ViewFt

# Create and configure logger
logging.basicConfig(level=logging.DEBUG,
                    filename="app.log",
                    format='%(lineno)s - %(levelname)s - %(message)s',
                    filemode='w')

# Creating an object
logger = logging.getLogger()

class SignalEmitter(QObject):    
    sig_ROI_changed = pyqtSignal()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('mainwindow.ui', self)
        self.apply_stylesheet("ManjaroMix.qss")
        self.inputImages = [self.originalImage1, self.originalImage2,self.originalImage3,self.originalImage4]
        
        self.outputImages = [self.outputImage1, self.outputImage2]
        self.imagesModels = [..., ... , ... , ... ]
        self.imageWidgets = [self.originalImage1, self.originalImage2, self.originalImage3, self.originalImage4,
                             self.outputImage1, self.outputImage2]
        self.heights = [..., ... , ... , ...]
        self.weights = [..., ... , ... , ...]
        self.myStorage = Storage(self.imagesModels)
        self.myMixer   = ImageMixer()
        self.allComboBoxes=[self.ftComponentMenu1,self.ftComponentMenu2,self.ftComponentMenu3,self.ftComponentMenu4]
        self.outputComboBoxes = [self.outputComponentMenu1,self.outputComponentMenu2,self.outputComponentMenu3,self.outputComponentMenu4 ]
        self.outputRatioSliders = [self.componentWeightSlider1,self.componentWeightSlider2,self.componentWeightSlider3,self.componentWeightSlider4]
        self.outputRatioSlidersLabels = [self.weightSliderLabel1,self.weightSliderLabel2,self.weightSliderLabel3,self.weightSliderLabel4]
        self.x = None
        self.y = None
        self.trackIndex=0
        self.contrastFactor=1
        self.brightnessFactor=0
        init_connectors(self)
        self.setupImagesView()
        ###############################################################################
        self.ftComponentWidgets = [self.plot_ft1, self.plot_ft2,self.plot_ft3,self.plot_ft4]
        self.viewport1 = ViewFt(self.imagesModels[0],self.plot_ft1)
        self.viewport2 = ViewFt(self.imagesModels[1],self.plot_ft2)
        self.viewport3 = ViewFt(self.imagesModels[2],self.plot_ft3)
        self.viewport4 = ViewFt(self.imagesModels[3],self.plot_ft4) 
        self.viewports = [self.viewport1, self.viewport2,self.viewport3,self.viewport4]
        self.ftComponentImages = [self.viewport1.plotFtImg,self.viewport2.plotFtImg,self.viewport3.plotFtImg,self.viewport4.plotFtImg]
        self.viewport1.sig_emitter.sig_ROI_changed.connect(lambda: self.modify_all_regions(self.viewport1.ft_roi))
        self.viewport2.sig_emitter.sig_ROI_changed.connect(lambda: self.modify_all_regions(self.viewport2.ft_roi))
        self.viewport3.sig_emitter.sig_ROI_changed.connect(lambda: self.modify_all_regions(self.viewport3.ft_roi))
        self.viewport4.sig_emitter.sig_ROI_changed.connect(lambda: self.modify_all_regions(self.viewport4.ft_roi))


    def modify_all_regions(self, roi: pg.ROI):
        new_state = roi.getState()
        for view in self.viewports:
            if view.ft_roi is not roi:
                view.ft_roi.setState(new_state, update = False) # Set the state of the other views without sending update signal
                view.ft_roi.stateChanged(finish = False) # Update the views after changing without sending stateChangeFinished signal
                view.region_update(view.ft_roi,finish = False)    
        


    def apply_stylesheet(self, stylesheet_path):
        stylesheet = QFile(stylesheet_path)
        if stylesheet.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(stylesheet)
            qss = stream.readAll()
            self.setStyleSheet(qss)
        else:
            print(f"Failed to open stylesheet file: {stylesheet_path}")    
    

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
            self.viewports[imgID].setImageModel(self.imagesModels[imgID])
            self.displayImage(self.imagesModels[imgID].imgByte, self.inputImages[imgID])
            for i, img in enumerate(self.imagesModels):
                 if type(img)!=type(...):
                    #  print("ana "+str(i+1),img.imgShape)
                      self.displayImage(self.imagesModels[i].imgByte, self.inputImages[i])
                    #  self.viewports[i].setRoiMaxBounds()
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
                if not isinstance(widget, pg.ImageItem): 
                     widget.ui.roiPlot.hide()
    
    def on_mouse_click(self,idx):
           # print("Double-clicked!"+str(idx))
            self.loadFile(idx)
            self.enableOutputCombos(idx)


    def applyFtComponents(self,idx):
        selectedComponent = self.allComboBoxes[idx-1].currentIndex()
        # fShift = np.fft.fftshift(self.imagesModels[idx-1].dft)
        # magnitude = 20 * np.log(np.abs(fShift))
        # phase = np.angle(fShift)
        # real = 20 * np.log(np.real(fShift))
        # imaginary = np.imag(fShift)
        FtComponentsData = [0*self.imagesModels[idx-1].magnitudePlot,self.imagesModels[idx-1].magnitudePlot,self.imagesModels[idx-1].phasePlot,\
                            self.imagesModels[idx-1].realPlot,self.imagesModels[idx-1].imaginaryPlot]
        # self.displayImage(FtComponentsData[selectedComponent],self.ftComponentImages[idx-1])
        self.displayImage(FtComponentsData[selectedComponent],self.ftComponentImages[idx-1])

    def enableOutputRatioSlider(self,index):
        selectedOutputComponents = [  i.currentText() for i in self.outputComboBoxes] 
        if  selectedOutputComponents[index]!=Modes.chooseComponent:
            self.outputRatioSliders[index].setEnabled(True) 
    def handleOutputRatioSliderChange(self,slider,index):
        self.outputRatioSlidersLabels[index].setText(f"{slider.value()} %")

    def enableOutputCombos(self,index):
        self.allComboBoxes[index].setEnabled(True)
        self.outputComboBoxes[index].setEnabled(True)    

    def handleOutputCombosChange(self,outputMode):
        if outputMode == Modes.magnitudeAndPhase:
            for i in range(1,4):
                self.outputComboBoxes[i].clear()
                self.outputComboBoxes[i].addItem("Choose Component")
                self.outputComboBoxes[i].addItem("Magnitude")
                self.outputComboBoxes[i].addItem("Phase")
                self.outputComboBoxes[i].setEnabled(True)    
        else: 
            for i in range(1,4):
                self.outputComboBoxes[i].clear()
                self.outputComboBoxes[i].addItem("Choose Component")
                self.outputComboBoxes[i].addItem("Real")
                self.outputComboBoxes[i].addItem("Imaginary")    
                self.outputComboBoxes[i].setEnabled(True)
    def handleOutputCombos(self):
       print("mama")
       output  = ...
       outputIdx = self.outputChannelMenu.currentIndex()
      # currentMode = self.outputComboBoxes[0].currentText()
       selectedOutputComponents = [  i.currentText() for i in self.outputComboBoxes] 
       weights = [i.value() for  i in self.outputRatioSliders]
       self.myMixer.setWeights(weights)
       if selectedOutputComponents[0] == "Magnitude" or selectedOutputComponents[0] == "Phase":
            #self.handleOutputCombosChange(Modes.magnitudeAndPhase)
            output = self.myMixer.mixImageModels(self.imagesModels, Modes.magnitudeAndPhase,selectedOutputComponents)
       elif selectedOutputComponents[0] == "Real"  or selectedOutputComponents[0] == "Imaginary":
           # self.handleOutputCombosChange(Modes.realAndImaginary)
            output = self.myMixer.mixImageModels(self.imagesModels, Modes.realAndImaginary,selectedOutputComponents)
       self.displayImage(output,self.outputImages[outputIdx])     
        # Mixer Logic IFFT    
    ###########################################################################
    # Brightness/Contrast Logic 
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
        crrX, crrY = event.pos().x(), event.pos().y()
        if self.x is None:
            self.x = crrX
            self.y = crrY
        else:
            if crrX - self.x > 1:
                self.brightnessFactor+=0.05
                if self.brightnessFactor>0.75:
                    self.brightnessFactor=0.75
            elif crrX - self.x < -1: 
                self.brightnessFactor-=0.05
                if self.brightnessFactor<-0.75:
                    self.brightnessFactor=-0.75
            self.x = crrX
            if crrY - self.y > 1:
                self.contrastFactor-=0.05
                if self.contrastFactor<0.1:
                    self.contrastFactor=0.1
            elif crrY - self.y < -1:
                self.contrastFactor+=0.05
                if self.contrastFactor>1.5:
                    self.contrastFactor=1.5
            self.y = crrY
            ImageModel.editedImage(self,self.imagesModels[self.trackIndex],self.inputImages[self.trackIndex],self.brightnessFactor,self.contrastFactor,self.trackIndex)    

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_pressed = False
                
            

             
    

def init_connectors(self):
    self.originalImage1.mouseDoubleClickEvent = lambda event, idx=0: self.on_mouse_click(idx)
    self.originalImage2.mouseDoubleClickEvent = lambda event, idx=1: self.on_mouse_click(idx)
    self.originalImage3.mouseDoubleClickEvent = lambda event, idx=2: self.on_mouse_click(idx)
    self.originalImage4.mouseDoubleClickEvent = lambda event, idx=3: self.on_mouse_click(idx)
    self.ftComponentMenu1.activated.connect(lambda: self.applyFtComponents(1))
    self.ftComponentMenu2.activated.connect(lambda: self.applyFtComponents(2))
    self.ftComponentMenu3.activated.connect(lambda: self.applyFtComponents(3))
    self.ftComponentMenu4.activated.connect(lambda: self.applyFtComponents(4))
    self.outputComponentMenu1.activated.connect(self.handleOutputCombos)
    self.outputComponentMenu2.activated.connect(self.handleOutputCombos)
    self.outputComponentMenu3.activated.connect(self.handleOutputCombos)
    self.outputComponentMenu4.activated.connect(self.handleOutputCombos)
    self.componentWeightSlider1.sliderReleased.connect(self.handleOutputCombos)
    self.componentWeightSlider2.sliderReleased.connect(self.handleOutputCombos)
    self.componentWeightSlider3.sliderReleased.connect(self.handleOutputCombos)
    self.componentWeightSlider4.sliderReleased.connect(self.handleOutputCombos)
    self.outputComponentMenu1.currentIndexChanged.connect(lambda:self.enableOutputRatioSlider(0))
    self.outputComponentMenu2.currentIndexChanged.connect(lambda:self.enableOutputRatioSlider(1))
    self.outputComponentMenu3.currentIndexChanged.connect(lambda:self.enableOutputRatioSlider(2))
    self.outputComponentMenu4.currentIndexChanged.connect(lambda:self.enableOutputRatioSlider(3))
    self.componentWeightSlider1.sliderReleased.connect(lambda:self.handleOutputRatioSliderChange(self.componentWeightSlider1,0))
    self.componentWeightSlider2.sliderReleased.connect(lambda:self.handleOutputRatioSliderChange(self.componentWeightSlider2,1))
    self.componentWeightSlider3.sliderReleased.connect(lambda:self.handleOutputRatioSliderChange(self.componentWeightSlider3,2))
    self.componentWeightSlider4.sliderReleased.connect(lambda:self.handleOutputRatioSliderChange(self.componentWeightSlider4,3))



def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
