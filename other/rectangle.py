import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt5.QtGui import QColor


class RectangleObject(QGraphicsRectItem):
    def __init__(self, x, y, width, height, parent=None):
        super().__init__(x, y, width, height, parent)
        self.setBrush(QColor(0, 255, 0))  # Set the brush color (green in this case)


def main():
    app = QApplication(sys.argv)
    scene = QGraphicsScene()

    # Creating a rectangle object
    rectangle = RectangleObject(50, 50, 200, 100)
    scene.addItem(rectangle)

    view = QGraphicsView(scene)
    view.setWindowTitle('Rectangle Object')
    view.setGeometry(100, 100, 400, 300)
    view.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
