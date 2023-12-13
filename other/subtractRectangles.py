import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene
from PyQt5.QtCore import QRect, QPoint, Qt


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        scene = QGraphicsScene(self)
        view = QGraphicsView(scene)
        self.setCentralWidget(view)

        # Creating two rectangles
        rect1 = scene.addRect(50, 50, 200, 100, QPen(QColor("blue")), QColor("blue"))
        rect2 = scene.addRect(100, 75, 150, 50, QPen(QColor("red")), QColor("red"))

        # Creating QPainterPaths from the rectangles
        path1 = QPainterPath()
        path2 = QPainterPath()
        path1.addRect(rect1.rect())
        path2.addRect(rect2.rect())

        # Subtracting path2 from path1
        path1 -= path2

        # Adjusting view to show only the resulting subtracted rectangle
        result_rect = scene.addPath(path1, QPen(QColor("green")), QColor("green"))
        view.fitInView(result_rect, aspectRatioMode=1)  # Fit view to show only the resulting subtracted rectangle

        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Subtract Rectangles')
        self.show()


def main():
    app = QApplication(sys.argv)
    ex = MyWidget()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
