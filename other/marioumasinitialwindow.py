import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class QExampleLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setPixmap(QtGui.QPixmap('assets\images\sad_cat.jpg'))

    def mousePressEvent(self, event):
        self.origin = event.pos()
        self.currentRubberBand = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self)
        self.currentRubberBand.setGeometry(QtCore.QRect(self.origin, QtCore.QSize()))
        self.currentRubberBand.show()

    def mouseMoveEvent(self, event):
        self.currentRubberBand.setGeometry(QtCore.QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        # self.currentRubberBand.hide()
        currentRect = self.currentRubberBand.geometry()
        # self.currentRubberBand.deleteLater()
        cropPixmap = self.pixmap().copy(currentRect)
        cropPixmap.save('output.png')

        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    exampleLabel = QExampleLabel()
    exampleLabel.show()
    sys.exit(app.exec_())
