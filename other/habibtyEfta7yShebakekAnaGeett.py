import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QColor,QMouseEvent, QBrush
from PyQt5.QtCore import QRect, QPoint, Qt

class DrawnElement:
    def __init__(self, rect, color):
        self.rect = rect
        self.color = color

class QExampleLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.drawnRectangles = []
        self.isTriangleDrawn = False         
        self.origin = QtCore.QPoint()     
        self.isInside = True    
        self.currentRubberBandGeometry = None

       
    def initUI(self):
        self.setPixmap(QtGui.QPixmap('assets\images\sad_cat.jpg'))
        self.selected_rect = None
 
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_O:
            self.isInside = False
             
        elif event.key() == QtCore.Qt.Key_I:
            self.isInside = True
        self.update()    

    def mousePressEvent(self, event):    
        self.origin = event.pos()    
        self.currentRubberBand = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self)
        self.currentRubberBand.setGeometry(QtCore.QRect(self.origin, QtCore.QSize()))
        self.currentRubberBand.show()
        self.currentRubberBandGeometry = self.currentRubberBand.geometry()

    # def mousePressEvent(self, event):        
    #     self.origin = event.pos()  
    #     self.currentRubberBand = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self)

    #     if event.button() == Qt.MouseButton.LeftButton:
    #         pos = event.pos()
    #         found = False
            
    #         for drawnRect in self.drawnRectangles:
    #             if drawnRect.rect.contains(pos):
    #                 print("Clicked inside a drawn rectangle")
    #                 found = True
    #                 break

    #         if not found:
    #             print("Clicked outside all drawn rectangles")
        
    #     else:
    #         self.currentRubberBand.setGeometry(QtCore.QRect(self.origin, QtCore.QSize()))
    #         self.currentRubberBand.show()
    
    def mouseMoveEvent(self, event):
        self.currentRubberBand.setGeometry(QtCore.QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        if self.isTriangleDrawn:
            self.clearDrawnRectangles()

        self.rubberBand = self.currentRubberBand
        self.selectedRect = self.currentRubberBand.geometry()
        
        rubberBandGeometry = self.currentRubberBand.geometry()
        selected_rect = QRect(rubberBandGeometry.topLeft(), rubberBandGeometry.size())

        translucent_red = QtGui.QColor(255, 0, 0, 100)  # Red with alpha value (100)

        new_rectangle = DrawnElement(selected_rect, translucent_red)
        self.drawnRectangles.append(new_rectangle)
        self.isTriangleDrawn = True

        self.currentRubberBand.hide()
        self.currentRubberBand.deleteLater()
        # pos = self.mapFromGlobal(event.globalPos())  
        
        # image_rect = self.pixmap().rect()
        # if self.selectedRect.contains(pos):
        #     print("ana gowa")
        # else:
        #     print("ana barra")
        
        # self.selectedOutsideRubberBand(myRect, event)
        self.exportSelectedArea(self.selectedRect)
    # def clearPartOfRectangle(self, clearGeometry):

    #     painter = QtGui.QPainter(self.pixmap())
    #     painter.setCompositionMode(QtGui.QPainter.CompositionMode_Clear)
    #     painter.fillRect(clearGeometry, QtCore.Qt.transparent)
    #     painter.end()

    #     self.setPixmap(self.pixmap())
  
    def clearDrawnRectangles(self):
        self.drawnRectangles = []  # Clear stored rectangles
        self.update()  # Trigger repaint
        self.isTriangleDrawn = False

    def subtractRubberBandFromPixmap(self, pixmap_rect, rubber_band_rect):
        
        # Define a polygon covering the entire pixmap
        full_pixmap_polygon = QtGui.QPolygon([
            pixmap_rect.topLeft(),
            pixmap_rect.topRight(),
            pixmap_rect.bottomRight(),
            pixmap_rect.bottomLeft()
        ])

        # Define a polygon for the area covered by the QRubberBand
        rubber_band_polygon = QtGui.QPolygon([
            rubber_band_rect.topLeft(),
            rubber_band_rect.topRight(),
            rubber_band_rect.bottomRight(),
            rubber_band_rect.bottomLeft()
        ])

        subtracted_polygon = full_pixmap_polygon.subtracted(rubber_band_polygon)

        return subtracted_polygon
        
    def paintEvent(self, event):        
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)  # Enable antialiasing for smoother shapes

        if self.isInside: 
            for drawnRect in self.drawnRectangles:
                painter.setPen(QtCore.Qt.NoPen)  # No outline
                painter.setBrush(QtGui.QBrush(drawnRect.color))  # Use a brush with color
                painter.drawRect(drawnRect.rect)  # Fill rectangle with translucent color   
        else:
            painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))
            pixmap_rect = QRect(0, 0, self.pixmap().width(), self.pixmap().height())  # Adjust these dimensions as per your pixmap
            rubber_band_rect = self.currentRubberBandGeometry

            polygon = self.subtractRubberBandFromPixmap(pixmap_rect, rubber_band_rect)
            painter.drawPolygon(polygon)

            painter.setBrush(QtGui.QBrush(QtGui.QColor(200, 100, 0, 100)))  # Specify the color here
            painter.setPen(QtCore.Qt.NoPen)  # No outline
            painter.drawPolygon(polygon)
            
            # rect = self.rect()
            # painter.drawRect(rect)
            # translucent_color = QtGui.QColor(255, 0, 0, 100)
            # # painter.fillRect(rect, QtGui.QBrush(translucent_color))
            # for drawnRect in self.drawnRectangles:
            #     painter.setPen(QtGui.QPen(drawnRect.color, 2))  # Set pen color and thickness
            #     painter.setBrush(QtCore.Qt.NoBrush)  # No fill for the rectangles
            #     painter.drawRect(drawnRect.rect)  # Draw rectangles


    # def selectedOutsideRubberBand(self, Rectangle: QRect, event: QMouseEvent):
    #     pos = self.mapFromGlobal(event.globalPos())  
    
    #     # image_rect = self.pixmap().rect()
    #     if Rectangle.contains(pos):
    #         print("Mouse is within the intersection.")
    #     else:
                # rectSameSize = QRect(rect.topLeft(), rect.size())
        # if rectSameSize.contains(pos):
        #     print("ana gowa yala")
        
        
    def exportSelectedArea(self, selected_rect):
        # Get the selected area from the image and export it as a separate image
        pixmap = self.pixmap()
        selected_pixmap = pixmap.copy(selected_rect)
        selected_pixmap.save("selected_area.png")  # Change the file format if needed

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    exampleLabel = QExampleLabel()
    exampleLabel.show()
    sys.exit(app.exec_())
