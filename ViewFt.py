from PyQt5.QtWidgets import QWidget, QFileDialog
import pyqtgraph as pg
import numpy as np
import cv2
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QSlider
from PyQt5.QtCore import Qt, QRectF, QObject, pyqtSignal
from PyQt5.QtCore import QPointF




class SignalEmitter(QObject):
    sig_ROI_changed = pyqtSignal()


class ViewFt():
      def __init__(self,imageModel, widget):  
          self.sig_emitter = SignalEmitter()
          self.imageModel = imageModel
          self.ROI_Maxbounds = QRectF(0, 0, 600,600 )    
          self.initial_roi_position = None
          self.plotFtImg = self.setupFtComponentsView(widget)
          # self.ftComponentWidgets = [self.plot_ft1, self.plot_ft2,self.plot_ft3,self.plot_ft4]
        
      

      def setupFtComponentsView(self,widget ):
        ft_view = widget.addViewBox()
        ft_view.setAspectLocked(True)
        ft_view.setMouseEnabled(x=False, y=False)

        
        imgFtComponent = pg.ImageItem()
        ft_view.addItem(imgFtComponent)

                # Testing ROI
        self.ft_roi = pg.ROI(pos = ft_view.viewRect().center(), size = (300, 300), hoverPen='b', resizable= True, invertible= True, rotatable= False, maxBounds= self.ROI_Maxbounds)
        ft_view.addItem(self.ft_roi)
        self.add_scale_handles_ROI(self.ft_roi)      
        
        self.ft_roi.sigRegionChangeFinished.connect(lambda: self.region_update(self.ft_roi,finish = True))
        return imgFtComponent
      def region_update(self,ft_roi , finish = False):
        if finish:
            self.sig_emitter.sig_ROI_changed.emit()
        new_img = ft_roi.getArrayRegion(self.imageModel.fShift,self.plotFtImg)
        self.imageModel.updateImgDims(np.fft.ifft2(np.fft.ifftshift(new_img)))

      def add_scale_handles_ROI(self, roi : pg.ROI):
        positions = np.array([[0,0], [1,0], [1,1], [0,1]])
        for pos in positions:        
            roi.addScaleHandle(pos = pos, center = 1 - pos)
