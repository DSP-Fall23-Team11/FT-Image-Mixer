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

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(lineno)s - %(levelname)s - %(message)s')

FileHandler = logging.FileHandler('imageMixer.log')
FileHandler.setLevel(logging.DEBUG)
FileHandler.setFormatter(formatter)
logger.addHandler(FileHandler)

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
        self.componentWeightSliders = [self.componentWeightSlider1, self.componentWeightSlider2, self.componentWeightSlider3, self.componentWeightSlider4]
        self.x = None
        self.y = None
        self.trackIndex=0
        self.contrastFactor=1
        self.brightnessFactor=0
        self.Mode = 0    
        ###############################################################################
        self.ftComponentWidgets = [self.plot_ft1, self.plot_ft2,self.plot_ft3,self.plot_ft4]
        self.viewports = []
        self.ftComponentImages = []
        for i,imgModel in enumerate(self.imagesModels):
            viewport=ViewFt(imgModel,self.ftComponentWidgets[i])
            self.viewports.append(viewport)
            self.ftComponentImages.append(viewport.plotFtImg)
        
        for i, viewport in enumerate(self.viewports):
            viewport.sig_emitter.sig_ROI_changed.connect(lambda i=i, v=viewport: self.modify_all_regions(v.getRoi()))
            self.componentWeightSliders[i].sliderPressed.connect(lambda i=i, v=viewport: self.modify_all_regions(v.getRoi()))
        init_connectors(self)
        self.setupImagesView()


    def modify_all_regions(self, roi: pg.ROI):
        new_state = roi.getState()
        for view in self.viewports:
            if view.getRoi() is not roi:
                view.getRoi().setState(new_state, update = False) # Set the state of the other views without sending update signal
                view.getRoi().stateChanged(finish = False) # Update the views after changing without sending stateChangeFinished signal
                view.region_update(view.getRoi(),finish = False)           
        


    def apply_stylesheet(self, stylesheet_path):
        stylesheet = QFile(stylesheet_path)
        if stylesheet.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(stylesheet)
            qss = stream.readAll()
            self.setStyleSheet(qss)
        else:
            logger.error(f"Failed to open stylesheet file: {stylesheet_path}")    
    

    def loadFile(self, imgID):
            self.filename, self.format = QtWidgets.QFileDialog.getOpenFileName(None, "Load Image",
                                                                            "*.jpg;;" "*.jpeg;;" "*.png;;")
            imgName = self.filename.split('/')[-1] 
            if self.filename == "":
                logger.warning(f"No file selected for image ID {imgID}.")
                return 
            image = cv2.imread(self.filename, flags=cv2.IMREAD_GRAYSCALE).T
            self.imagesModels[imgID] = ImageModel(self.filename)
            self.myStorage.setImageModels(self.imagesModels)
            self.myStorage.unifyImagesSize()
            self.viewports[imgID].setImageModel(self.imagesModels[imgID])
            self.displayImage(self.imagesModels[imgID].getImgByte(), self.inputImages[imgID])
            for i, img in enumerate(self.imagesModels):
                 if type(img)!=type(...):
                      self.displayImage(self.imagesModels[i].getImgByte(), self.inputImages[i])
                      self.inputImages[i].export("Output"+str(i)+".jpg")
                      logger.debug(f"Loading image with ID {imgID}.")

    def setupImagesView(self):
        for widget in self.imageWidgets:
            widget.ui.histogram.hide()
            widget.ui.roiBtn.hide()
            widget.ui.menuBtn.hide()
            widget.ui.roiPlot.hide()
            widget.getView().setAspectLocked(False)
            widget.view.setAspectLocked(False)
            logger.debug("image views set up")
      

    def displayImage(self, data, widget):
                widget.setImage(data)
                if not isinstance(widget, pg.ImageItem): 
                     widget.ui.roiPlot.hide()
    
    def on_mouse_click(self,idx):
            self.loadFile(idx)
            self.enableOutputCombos(idx)


    def applyFtComponents(self,idx):
        selectedComponent = self.allComboBoxes[idx-1].currentIndex()
        FtComponentsData = [0*self.imagesModels[idx-1].getMagnitudePlot(),self.imagesModels[idx-1].getMagnitudePlot(),self.imagesModels[idx-1].getPhasePlot(),\
                            self.imagesModels[idx-1].getRealPlot(),self.imagesModels[idx-1].getImaginaryPlot()]
        self.displayImage(FtComponentsData[selectedComponent],self.ftComponentImages[idx-1])
        logger.debug("Ft components applied")

    def enableOutputRatioSlider(self,index):
        selectedOutputComponents = [  i.currentText() for i in self.outputComboBoxes] 
        if  selectedOutputComponents[index]!=Modes.chooseComponent:
            self.outputRatioSliders[index].setEnabled(True) 
    def handleOutputRatioSliderChange(self,slider,index):
        self.outputRatioSlidersLabels[index].setText(f"{slider.value()} %")

    def enableOutputCombos(self,index):
        self.allComboBoxes[index].setEnabled(True)
        self.outputComboBoxes[index].setEnabled(True)    
              
    def handleOutputCombosChange(self):
        outputMode = Modes.magnitudeAndPhase if self.outputComponentMenu1.currentText() in ["Magnitude", "Phase"] else Modes.realAndImaginary
        for i in range(1,4):
              magnitudeAndPhaseState = outputMode == Modes.magnitudeAndPhase
              realAndImaginaryState = not magnitudeAndPhaseState
              self.outputComboBoxes[i].model().item(1).setEnabled(magnitudeAndPhaseState)
              self.outputComboBoxes[i].model().item(2).setEnabled(magnitudeAndPhaseState)     
              self.outputComboBoxes[i].model().item(3).setEnabled(realAndImaginaryState)
              self.outputComboBoxes[i].model().item(4).setEnabled(realAndImaginaryState)
              self.outputComboBoxes[i].setCurrentIndex(1 if magnitudeAndPhaseState else 3)

    def handleOutputCombos(self):
       output  = ...
       outputIdx = self.outputChannelMenu.currentIndex()
       selectedOutputComponents = [  i.currentText() for i in self.outputComboBoxes] 
       weights = [i.value() for  i in self.outputRatioSliders]
       self.myMixer.setWeights(weights)
       if selectedOutputComponents[0] == "Magnitude" or selectedOutputComponents[0] == "Phase":
            output = self.myMixer.mixImageModels(self.imagesModels, Modes.magnitudeAndPhase,selectedOutputComponents,self.viewports,self.Mode)
            logger.debug(f"images mixed in magnitude and phase mode")        
         
       elif selectedOutputComponents[0] == "Real"  or selectedOutputComponents[0] == "Imaginary":
            output = self.myMixer.mixImageModels(self.imagesModels, Modes.realAndImaginary,selectedOutputComponents,self.viewports,self.Mode)
            logger.debug(f"images mixed in Real and imaginary mode")        
         
       self.displayImage(output,self.outputImages[outputIdx])     
    def handleMixerModeCombo(self):
          self.Mode = self.InnerOuterMenu.currentIndex() 
          if(self.Mode == 0):
              logger.info(f"mixing is in Inner mode")
          else:
              logger.info(f"mixing is in Outer mode ")    
        # Mixer Logic IFFT    
    ###########################################################################
    # Brightness/Contrast Logic 
    def mousePressEvent(self, event: QMouseEvent):
          for i in range(4):
            if (event.button() == Qt.MouseButton.MidButton) and (self.inputImages[i].underMouse()):
                self.contrastFactor=1
                self.brightnessFactor=0
                ImageModel.alterContrastAndBrightness(self,self.imagesModels[i],self.inputImages[i],self.brightnessFactor,self.contrastFactor,self.trackIndex)
                logger.debug("contast/brightness changed")

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
            ImageModel.alterContrastAndBrightness(self,self.imagesModels[self.trackIndex],self.inputImages[self.trackIndex],self.brightnessFactor,self.contrastFactor,self.trackIndex)
            logger.debug("contast/brightness changed")    

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_pressed = False
                
            
def init_connectors(self):

    for idx, image in enumerate(self.inputImages):
        image.mouseDoubleClickEvent = lambda event, i=idx: self.on_mouse_click(i)

    for idx, (outputMenu, weightSlider) in enumerate(zip(self.outputComboBoxes, self.componentWeightSliders)):
            outputMenu.activated.connect(self.handleOutputCombos)
            weightSlider.sliderReleased.connect(self.handleOutputCombos)
            weightSlider.sliderReleased.connect(lambda s=weightSlider, i=idx: self.handleOutputRatioSliderChange(s, i))


    self.ftComponentMenu1.activated.connect(lambda: self.applyFtComponents(1))
    self.ftComponentMenu2.activated.connect(lambda: self.applyFtComponents(2))
    self.ftComponentMenu3.activated.connect(lambda: self.applyFtComponents(3))
    self.ftComponentMenu4.activated.connect(lambda: self.applyFtComponents(4))
    self.outputComponentMenu1.currentIndexChanged.connect(lambda:self.enableOutputRatioSlider(0))
    self.outputComponentMenu2.currentIndexChanged.connect(lambda:self.enableOutputRatioSlider(1))
    self.outputComponentMenu3.currentIndexChanged.connect(lambda:self.enableOutputRatioSlider(2))
    self.outputComponentMenu4.currentIndexChanged.connect(lambda:self.enableOutputRatioSlider(3))
    self.InnerOuterMenu.currentIndexChanged.connect(lambda:self.handleMixerModeCombo())
    self.InnerOuterMenu.currentIndexChanged.connect(lambda:self.handleOutputCombos())
    self.outputComponentMenu1.activated.connect(lambda:self.handleOutputCombosChange())
    




def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
