import numpy as np
import cv2
from ImageModel import ImageModel
from Modes import Modes
# weights -> sliders , init : 0 
# Mode -> mode enum
# 
class ImageMixer():
    def __init__(self):
        self.weights = [0,0,0,0]
        self.weights = [ weight/100 for  weight in self.weights]
        

    def setWeights(self, weights):
        self.weights = weights
        self.weights = [ weight/100 for  weight in self.weights]

    def generateModesWeights(self,selectedOutputComponents):
        magWeight = [0,0,0,0]
        phaseWeight = [0,0,0,0]
        for i,component in enumerate(selectedOutputComponents):
            if component == "Magnitude" or component == "Real":
                magWeight[i] = self.weights[i]
                phaseWeight[i] = 0
            elif component == "Phase" or component=="Imaginary":
                magWeight[i] = 0
                phaseWeight[i] = self.weights[i]
            elif component == "Choose Component":
                   magWeight[i] = 0
                   phaseWeight[i] = 0 
        print(magWeight)
        print(phaseWeight)
        return magWeight,phaseWeight                 


    
    def mixImageModels(self,imagesModels,mode,selectedOutputComponents):
        if mode == Modes.magnitudeAndPhase:
            magnitudeMix= 0
            phaseMix =0
            magnitudeWeights, phaseWeights = self.generateModesWeights(selectedOutputComponents)
            for i,weight in  enumerate(magnitudeWeights):
                if weight!= 0:
                    magnitudeMix += weight*imagesModels[i].editedmagnitude
            for i,weight in  enumerate(phaseWeights):
                if weight!= 0:
                    phaseMix += weight*imagesModels[i].editedphase        
            return abs(np.real(np.fft.ifft2(np.multiply(magnitudeMix,np.exp(1j * phaseMix)))))        
        elif mode == Modes.realAndImaginary:
            realMix = 0
            imaginaryMix = 0
            realWeights, imaginaryWeights = self.generateModesWeights(selectedOutputComponents)
            for i,weight in  enumerate(realWeights):
                if weight!= 0:
                    realMix += weight*imagesModels[i].editedreal
            for i,weight in  enumerate(imaginaryWeights):
                if weight!= 0:
                    imaginaryMix += weight*imagesModels[i].editedimaginary        
            return abs(np.real(np.fft.ifft2(realMix+ 1j*imaginaryMix))) 



