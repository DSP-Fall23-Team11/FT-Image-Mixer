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
        self.editedimgByte=None
        self.editedimgShape=None
        self.editeddft=None
        self.editedreal=None
        self.editedimaginary=None
        self.editedmagnitude=None 
        self.editedphase=None
        self.editedfShift=None
        self.editedmagnitudePlot=None
        self.editedphasePlot=None 
        self.editedrealPlot=None
        self.editedimaginaryPlot=None 
        

    def SetImageParams(self,imgByte,edited=False):
      if edited:
         self.editedimgByte = imgByte
         self.imgShape = self.editedimgByte.shape
         self.dft = np.fft.fft2(self.editedimgByte)
      else:
         self.imgByte = imgByte
         self.imgShape = self.imgByte.shape
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


    def setRectangleParams(self,imgByte):
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

## Getters & Setters For Encaps
    def setImgPath(self,imgPath):
       self.imgPath = imgPath
    def getImgPath(self):
       return self.imgPath

    def setImgByte(self,imgByte):
       self.imgByte = imgByte
    def getImgByte(self):
       return self.imgByte

    def setImgShape(self,imgShape):
       self.imgShape = imgShape
    def getImgShape(self):
       return self.imgShape

    def setEditedImgByte(self,editedimgByte):
       self.editedimgByte = editedimgByte
    def getEditedImgByte(self):
       return self.editedimgByte

    def setContrastedImgByte(self,contrastedimgByte):
       self.contrastedimgByte = contrastedimgByte
    def getContrastedImgByte(self):
       return self.contrastedimgByte

    def setBrightenedImgByte(self,brightenedimgByte):
       self.brightenedimgByte = brightenedimgByte
    def getBrightenedImgByte(self):
       return self.brightenedimgByte

    def setDft(self,dft):
       self.dft = dft
    def getDft(self):
       return self.dft

    def setReal(self,real):
       self.real = real
    def getReal(self):
       return self.real

    def setImaginary(self,imaginary):
       self.imaginary = imaginary
    def getImaginary(self):
       return self.imaginary

    def setMagnitude(self,magnitude):
       self.magnitude = magnitude 
    def getMagnitude(self):
       return self.magnitude

    def setPhase(self,phase):
        self.phase = phase
    def getPhase(self):
       return self.phase

    def setFshift(self,fShift):
       self.fShift = fShift
    def getFshift(self):
       return self.fShift

    def setMagnitudePlot(self,magnitudePlot):
       self.magnitudePlot = magnitudePlot
    def getMagnitudePlot(self):
       return self.magnitudePlot

    def setPhasePlot(self,phasePlot):
       self.phasePlot = phasePlot
    def getPhasePlot(self):
       return self.phasePlot

    def setRealPlot(self,realPlot):
       self.realPlot = realPlot
    def getRealPlot(self):
       return self.realPlot

    def setImaginaryPlot(self,imaginaryPlot):
       self.imaginaryPlot = imaginaryPlot
    def getImaginaryPlot(self):
       return self.imaginaryPlot

    def setEditedImgShape(self,editedimgShape):
       self.editedimgShape = editedimgShape  
    def getEditedImgShape(self):
       return self.editedimgShape


    def setEditedDft(self,editeddft):
       self.editeddft = editeddft     
    def getEditedDft(self):
       return self.editeddft

    def setEditedReal(self,editedreal):
       self.editedreal = editedreal    
    def getEditedReal(self):
       return self.editedreal

    def setEditedImaginary(self,editedimaginary):
       self.editedimaginary = editedimaginary       
    def getEditedImaginary(self):
       return self.editedimaginary

    def setEditedMagnitude(self,editedmagnitude):
       self.editedmagnitude = editedmagnitude  
    def getEditedMagnitude(self):
       return self.editedmagnitude

    def setEditedPhase(self,editedphase):
       self.editedphase = editedphase      
    def getEditedPhase(self):
       return self.editedphase

    def setEditedFshift(self,editedfShift):
       self.editedfShift = editedfShift  
    def getEditedFshift(self):
       return self.editedfShift

    def setEditedMagnitudePlot(self,editedmagnitudePlot):
       self.editedmagnitudePlot = editedmagnitudePlot 
    def getEditedMagnitudePlot(self):
       return self.editedmagnitudePlot

    def setEditedPhasePlot(self,editedphasePlot):
       self.editedphasePlot = editedphasePlot    
    def getEditedPhasePlot(self):
       return self.editedphasePlot

    def setEditedRealPlot(self,editedrealPlot):
       self.editedrealPlot = editedrealPlot    
    def getEditedRealPlot(self):
       return self.editedrealPlot

    def setEditedImaginaryPlot(self,editedimaginaryPlot):
       self.editedimaginaryPlot = editedimaginaryPlot        
    def getEditedImaginaryPlot(self):
       return self.editedimaginaryPlot


    def alterContrastAndBrightness(self, imageObject, widget,Bfactor,Cfactor,idx):
        contrastFactor = Cfactor
        brightnessFactor = Bfactor  # -1 to 1
        m = np.array(imageObject.imgByte) 
        im = (m/ 255.0 + brightnessFactor) * 255
        im = np.clip(im, 0, 255).astype(np.uint8)
        im = (im/ 255 - 0.5) * 255 * contrastFactor + 128
        im = np.clip(im, 0, 255).astype(np.uint8)
        imageObject.editedimgByte = im
        imageObject.SetImageParams(imageObject.editedimgByte,True)
        widget.setImage(imageObject.editedimgByte)
        index = idx
        widget.ui.roiPlot.hide()
        self.applyFtComponents(index+1)

    