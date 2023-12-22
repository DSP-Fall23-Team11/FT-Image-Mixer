import logging
import numpy as np
import cv2
from ImageModel import ImageModel
from Modes import Modes

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(lineno)s - %(levelname)s - %(message)s')

FileHandler = logging.FileHandler('imageMixer.log')
FileHandler.setLevel(logging.DEBUG)
FileHandler.setFormatter(formatter)
logger.addHandler(FileHandler)

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
        return magWeight,phaseWeight                 


    
    def mixImageModels(self,imagesModels,mode,selectedOutputComponents,viewports,roiMode):
        if roiMode == 0:
                mask = np.zeros(imagesModels[0].imgByte.shape)
                mask[int(viewports[0].y1):int(viewports[0].y2)+1,int(viewports[0].x1):int(viewports[0].x2)+1] = 1
        else:    
                mask = np.ones(imagesModels[0].imgByte.shape)
                mask[int(viewports[0].y1):int(viewports[0].y2)+1,int(viewports[0].x1):int(viewports[0].x2)+1] = 0
        if mode == Modes.magnitudeAndPhase:
            magnitudeMix= 0
            phaseMix =0
            magnitudeWeights, phaseWeights = self.generateModesWeights(selectedOutputComponents)
            for i, (mag_weight, phase_weight) in enumerate(zip(magnitudeWeights, phaseWeights)):
                if mag_weight != 0:
                    magnitudeMix += mag_weight * np.abs(imagesModels[i].getFshift())
                if phase_weight != 0:
                    phaseMix += phase_weight * np.angle(imagesModels[i].getFshift())
            return np.clip(np.abs(np.fft.ifft2(((magnitudeMix*mask)*np.exp(1j * (phaseMix*mask))))),0,255)        
        elif mode == Modes.realAndImaginary:
            realMix = 0
            imaginaryMix = 0
            realWeights, imaginaryWeights = self.generateModesWeights(selectedOutputComponents)
            for i, (real_weight, imag_weight) in enumerate(zip(realWeights, imaginaryWeights)):
                if real_weight != 0:
                    realMix += real_weight * np.real(imagesModels[i].getFshift())
                if imag_weight != 0:
                    imaginaryMix += imag_weight * np.imag(imagesModels[i].getFshift())       
            return np.clip(np.abs(np.fft.ifft2((realMix*mask)+(imaginaryMix*mask)*1j)),0,255) 
            


