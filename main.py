from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel, QVBoxLayout, QWidget, QSlider, QComboBox, QGraphicsRectItem
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QRectF
import sys
import logging
import numpy as np
import cv2
import matplotlib.pyplot as plt
from ImageModel import ImageModel


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
        self.setupImagesView()
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

    def loadFile(self, imgID):
            """
            Load the File from User
            :param imgID: 0 or 1
            :return:
            """
            # Open File & Check if it was loaded correctly
            logger.info("Browsing the files...")
            repo_path = "D:\Study\Courses\Python\DSP Tasks - 3rd Year\sbe309-2020-task3-Abdullah-Alrefaey\images"
            self.filename, self.format = QtWidgets.QFileDialog.getOpenFileName(None, "Load Image", repo_path,
                                                                            "*.jpg;;" "*.jpeg;;" "*.png;;")
            imgName = self.filename.split('/')[-1]
            if self.filename == "":
                pass
            else:
                image = cv2.imread(self.filename, flags=cv2.IMREAD_GRAYSCALE).T
                self.heights[imgID], self.weights[imgID] = image.shape
                self.imagesModels[imgID] = ImageModel(self.filename)

                if type(self.imagesModels[~imgID]) == type(...):
                    # Create and Display Original Image
                    self.displayImage(self.imagesModels[imgID].imgByte, self.inputImages[imgID])
                   # self.updateCombos[imgID].setEnabled(True)
                   # logger.info(f"Added Image{imgID + 1}: {imgName} successfully")
                else:
                    if self.heights[1] != self.heights[0] or self.weights[1] != self.weights[0]:
                        self.showMessage("Warning!!", "Image sizes must be the same, please upload another image",
                                        QMessageBox.Ok, QMessageBox.Warning)
                      #  logger.warning("Warning!!. Image sizes must be the same, please upload another image")
                    else:
                        self.displayImage(self.imagesModels[imgID].imgByte, self.inputImages[imgID])
                     #   self.updateCombos[imgID].setEnabled(True)
                     #   logger.info(f"Added Image{imgID + 1}: {imgName} successfully")

                # if self.updateCombos[0].isEnabled() and self.updateCombos[1].isEnabled():
                #    self.enableOutputCombos()
                #    logger.info("ComboBoxes have been enabled successfully")
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
                widget.view.setRange(xRange=[0, self.imagesModels[0].imgShape[0]], yRange=[0, self.imagesModels[0].imgShape[1]],
                                    padding=0)
                widget.ui.roiPlot.hide()            
    def on_mouse_click(self,idx):
            print("Double-clicked!"+str(idx))
            self.enableOutputCombos(idx)
            self.loadFile(idx)

    def enableOutputCombos(self,index):
        self.allComboBoxes[index].setEnabled(True)
         
         

def init_connectors(self):
    self.originalImage1.mouseDoubleClickEvent = lambda event, idx=0: self.on_mouse_click(idx)
    self.originalImage2.mouseDoubleClickEvent = lambda event, idx=1: self.on_mouse_click(idx)
    self.originalImage3.mouseDoubleClickEvent = lambda event, idx=2: self.on_mouse_click(idx)
    self.originalImage4.mouseDoubleClickEvent = lambda event, idx=3: self.on_mouse_click(idx)

    for i in range(4):
        self.brightnessSliders[i].sliderReleased.connect(lambda i=i: ImageModel.editedImage(self,self.imagesModels[i],self.inputImages[i],self.brightnessSliders[i].value()/100,self.contrastSliders[i].value()/100))
        self.contrastSliders[i].sliderReleased.connect(lambda i=i: ImageModel.editedImage(self,self.imagesModels[i],self.inputImages[i],self.brightnessSliders[i].value()/100,self.contrastSliders[i].value()/100))
def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
