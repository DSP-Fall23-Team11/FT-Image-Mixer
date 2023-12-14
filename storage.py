## A Gallery having instances of ImageModel to make sure all the time all images have a unified dims 
import numpy as np
import cv2

class Storage():
    def __init__(self,ImageModels):
        self.ImagesModels = ImageModels
        self.minWidth = 100000
        self.minHeight = 100000
    def setImageModels(self,ImageModels):
       self.ImagesModels = ImageModels
    def getMinDims(self):
        for img in self.ImagesModels:
          if type(img)!=type(...):
            self.minWidth = min(img.imgShape[0],self.minWidth)
            self.minHeight = min(img.imgShape[1],self.minHeight)

    def unifyImagesSize(self):
        if type(self.ImagesModels[1])!=type(...):
           self.getMinDims()
           resized_images = [... ,... ,..., ... ]
           for i,img in enumerate(self.ImagesModels):
              if(type(img)!=type(...)):
                resized_images[i] = cv2.resize(img.imgByte, (self.minWidth, self.minHeight))
                 
           for index , img in enumerate(self.ImagesModels):
               if(type(resized_images[index])!=type(...)):
                   img.SetImageParams(resized_images[index])
                   

                
            
             
                

