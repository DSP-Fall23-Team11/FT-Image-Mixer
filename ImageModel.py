import numpy as np
import cv2

class ImageModel():
    def __init__(self, imgPath: str):
        self.imgPath = imgPath
        self.imgByte = cv2.imread(self.imgPath, flags=cv2.IMREAD_GRAYSCALE).T
        self.imgShape = self.imgByte.shape
        self.editedimgByte = self.imgByte.copy()
        self.contrastedimgByte = self.imgByte
        self.brightenedimgByte = self.imgByte
        print("hh",self.imgShape)
        self.dft = np.fft.fft2(self.imgByte)
        self.real = np.real(self.dft)
        self.imaginary = np.imag(self.dft)
        self.magnitude = np.abs(self.dft)
        self.phase = np.angle(self.dft)
        self.uniformMagnitude = np.ones(self.imgByte.shape)
        self.uniformPhase = np.zeros(self.imgByte.shape)
    
    def updateImgDims(self,imgByte):
      self.imgByte = imgByte
      self.imgShape = self.imgByte.shape
      self.dft = np.fft.fft2(self.imgByte)
      self.real = np.real(self.dft)
      self.imaginary = np.imag(self.dft)
      self.magnitude = np.abs(self.dft)
      self.phase = np.angle(self.dft)
      self.uniformMagnitude = np.ones(self.imgByte.shape)
      self.uniformPhase = np.zeros(self.imgByte.shape)


    def editedImage(self, imageObject, widget,Bfactor,Cfactor):
        contrastFactor = Cfactor
        brightnessFactor = Bfactor  # -1 to 1
        m = np.array(imageObject.imgByte) 
        im = (m/ 255.0 + brightnessFactor) * 255
        im = np.clip(im, 0, 255).astype(np.uint8)
        im = (im/ 255 - 0.5) * 255 * contrastFactor 
        im = np.clip(im, 0, 255).astype(np.uint8)
        imageObject.editedimgByte = im
        widget.setImage(imageObject.editedimgByte)
        # widget.view.setRange(xRange=[0, imageObject.imgShape[0]], yRange=[0, imageObject.imgShape[1]], padding=0)
        widget.ui.roiPlot.hide()
        #print("B",Bfactor)
        #print("C",Cfactor)

