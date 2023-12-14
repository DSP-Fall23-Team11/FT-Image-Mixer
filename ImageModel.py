import numpy as np
import cv2
# GLobals
global index
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
        self.fShift = np.fft.fftshift(self.dft)
        self.magnitudePlot = 20 * np.log(np.abs(self.fShift))
        self.phasePlot = np.angle(self.fShift)
        self.realPlot = 20 * np.log(np.real(self.fShift))
        self.imaginaryPlot = np.imag(self.fShift)
    
    def updateImgDims(self,imgByte):
      self.editedimgByte = imgByte
      self.editedimgShape = self.editedimgByte.shape
      self.editeddft = np.fft.fft2(self.editedimgByte)
      self.editedreal = np.real(self.editeddft)
      self.editedimaginary = np.imag(self.editeddft)
      self.editedmagnitude = np.abs(self.editeddft)
      self.editedphase = np.angle(self.editeddft)
      self.editedfShift = np.fft.fftshift(self.editeddft)
      self.editedmagnitudePlot = 20 * np.log(np.abs(self.editedfShift))
      self.editedphasePlot = np.angle(self.editedfShift)
      self.editedrealPlot = 20 * np.log(np.real(self.editedfShift))
      self.editedimaginaryPlot = np.imag(self.editedfShift)


    def editedImage(self, imageObject, widget,Bfactor,Cfactor,idx):
        contrastFactor = Cfactor
        brightnessFactor = Bfactor  # -1 to 1
        m = np.array(imageObject.imgByte) 
        im = (m/ 255.0 + brightnessFactor) * 255
        im = np.clip(im, 0, 255).astype(np.uint8)
        im = (im/ 255 - 0.5) * 255 * contrastFactor + 128
        im = np.clip(im, 0, 255).astype(np.uint8)
        imageObject.editedimgByte = im
        imageObject.editedUpdateImgDims(imageObject.editedimgByte)
        widget.setImage(imageObject.editedimgByte)
        index = idx
        widget.ui.roiPlot.hide()
        self.applyFtComponents(index+1)

    def editedUpdateImgDims(self,imgByte):
        self.editedimgByte = imgByte
        self.imgShape = self.editedimgByte.shape
        self.dft = np.fft.fft2(self.editedimgByte)
        self.real = np.real(self.dft)
        self.imaginary = np.imag(self.dft)
        self.magnitude = np.abs(self.dft)
        self.phase = np.angle(self.dft)