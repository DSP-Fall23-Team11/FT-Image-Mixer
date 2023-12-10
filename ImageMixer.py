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

    def setWeights(self, weights):
        self.weights = weights
        self.weights = [ weight/sum(self.weights) for weight in self.weights]
    
    def mixImageModels(self,imagesModels,mode):
        if mode == Modes.magnitudeAndPhase:
            magnitudeMix= 0
            phaseMix =0
            for i,weight in  enumerate(self.weights):
                if weight!= 0:
                    magnitudeMix += weight*imagesModels[i].magnitude
                    phaseMix +=  weight*imagesModels[i].phase
            return abs(np.real(np.fft.ifft2(np.multiply(magnitudeMix,np.exp(1j * phaseMix)))))        
        elif mode == Modes.realAndImaginary:
            realMix= 0
            imaginaryMix =0
            for i,weight in  enumerate(self.weights):
                if weight!= 0:
                    realMix += weight*imagesModels[i].real
                    imaginaryMix +=  weight*imagesModels[i].imaginary
            return abs(np.real(np.fft.ifft2(realMix+ 1j*imaginaryMix))) 



