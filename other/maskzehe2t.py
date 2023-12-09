from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt5.QtCore import Qt, QRectF, pyqtSignal

class ImageView(QGraphicsView):
    doubleClick = pyqtSignal()

    def __init__(self):
        super().__init__()

    def mouseDoubleClickEvent(self, event):
        self.doubleClick.emit()  # Emit the signal on double click
        super().mouseDoubleClickEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.view = ImageView()
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)

        # Add a rectangle item for demonstration
        rect_item = QGraphicsRectItem(QRectF(50, 50, 100, 100))
        self.scene.addItem(rect_item)

        self.view.doubleClick.connect(self.on_doubleclick)

        self.setCentralWidget(self.view)

    def on_doubleclick(self):
        print("Double-clicked on ImageView")

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
