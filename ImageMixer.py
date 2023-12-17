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
            for i, (mag_weight, phase_weight) in enumerate(zip(magnitudeWeights, phaseWeights)):
                if mag_weight != 0:
                    print(imagesModels[i].getEditedMagnitude(),"a7aaaaaa")
                    magnitudeMix += mag_weight * imagesModels[i].getEditedMagnitude()
                if phase_weight != 0:
                    phaseMix += phase_weight * imagesModels[i].getEditedPhase()
            return abs(np.fft.ifft2(np.multiply(magnitudeMix,np.exp(1j * phaseMix))))        
        elif mode == Modes.realAndImaginary:
            realMix = 0
            imaginaryMix = 0
            realWeights, imaginaryWeights = self.generateModesWeights(selectedOutputComponents)
            for i, (real_weight, imag_weight) in enumerate(zip(realWeights, imaginaryWeights)):
                if real_weight != 0:
                    realMix += real_weight * imagesModels[i].getEditedReal()
                if imag_weight != 0:
                    imaginaryMix += imag_weight * imagesModels[i].getEditedImaginary()       
            return abs(np.fft.ifft2(realMix+ 1j*imaginaryMix)) 



