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

## Getters & Setters For Encaps
    def getImgPath(self):
       return self.imgPath
    def setImgPath(self,imgPath):
       self.imgPath = imgPath

    def getImgByte(self):
       return self.imgByte
    def setImgByte(self,imgByte):
       self.imgByte = imgByte

    def getImgShape(self):
       return self.imgShape
    def setImgShape(self,imgShape):
       self.imgShape = imgShape

    def getEditedImgByte(self):
       return self.editedimgByte
    def setEditedImgByte(self,editedimgByte):
       self.editedimgByte = editedimgByte

    def getContrastedImgByte(self):
       return self.contrastedimgByte
    def setContrastedImgByte(self,contrastedimgByte):
       self.contrastedimgByte = contrastedimgByte

    def getBrightenedImgByte(self):
       return self.brightenedimgByte
    def setBrightenedImgByte(self,brightenedimgByte):
       self.brightenedimgByte = brightenedimgByte

    def getDft(self):
       return self.dft
    def setDft(self,dft):
       self.dft = dft

    def getReal(self):
       return self.real
    def setReal(self,real):
       self.real = real

    def getImaginary(self):
       return self.imaginary
    def setImaginary(self,imaginary):
       self.imaginary = imaginary

    def getMagnitude(self):
       return self.magnitude
    def setMagnitude(self,magnitude):
       self.magnitude = magnitude 

    def getPhase(self):
       return self.phase
    def setPhase(self,phase):
        self.phase = phase

    def getFshift(self):
       return self.fShift
    def setFshift(self,fShift):
       self.fShift = fShift

    def getMagnitudePlot(self):
       return self.magnitudePlot
    def setMagnitudePlot(self,magnitudePlot):
       self.magnitudePlot = magnitudePlot

    def getPhasePlot(self):
       return self.phasePlot
    def setPhasePlot(self,phasePlot):
       self.phasePlot = phasePlot

    def getRealPlot(self):
       return self.realPlot
    def setRealPlot(self,realPlot):
       self.realPlot = realPlot

    def getImaginaryPlot(self):
       return self.imaginaryPlot
    def setImaginaryPlot(self,imaginaryPlot):
       self.imaginaryPlot = imaginaryPlot

    def getEditedImgShape(self):
       return self.editedimgShape
    def setEditedImgShape(self,editedimgShape):
       self.editedimgShape = editedimgShape  

    def getEditedImgShape(self):
       return self.editedimgShape
    def setEditedImgShape(self,editedimgShape):
       self.editedimgShape = editedimgShape

    def getEditedDft(self):
       return self.editeddft
    def setEditedDft(self,editeddft):
       self.editeddft = editeddft     

    def getEditedReal(self):
       return self.editedreal
    def setEditedReal(self,editedreal):
       self.editedreal = editedreal    

    def getEditedImaginary(self):
       return self.editedimaginary
    def setEditedImaginary(self,editedimaginary):
       self.editedimaginary = editedimaginary       

    def getEditedMagnitude(self):
       return self.editedmagnitude
    def setEditedMagnitude(self,editedmagnitude):
       self.editedmagnitude = editedmagnitude  

    def getEditedPhase(self):
       return self.editedphase
    def setEditedPhase(self,editedphase):
       self.editedphase = editedphase      

    def getEditedFshift(self):
       return self.editedfShift
    def setEditedFshift(self,editedfShift):
       self.editedfShift = editedfShift  

    def getEditedMagnitudePlot(self):
       return self.editedmagnitudePlot
    def setEditedMagnitudePlot(self,editedmagnitudePlot):
       self.editedmagnitudePlot = editedmagnitudePlot 

    def getEditedPhasePlot(self):
       return self.editedphasePlot
    def setEditedPhasePlot(self,editedphasePlot):
       self.editedphasePlot = editedphasePlot    

    def getEditedRealPlot(self):
       return self.editedrealPlot
    def setEditedRealPlot(self,editedrealPlot):
       self.editedrealPlot = editedrealPlot    

    def getEditedImaginaryPlot(self):
       return self.editedimaginaryPlot
    def setEditedImaginaryPlot(self,editedimaginaryPlot):
       self.editedimaginaryPlot = editedimaginaryPlot        


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
        
