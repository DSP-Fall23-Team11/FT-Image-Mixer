import sys
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QVBoxLayout, QWidget, QLabel, QSlider
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import Qt

class ImageProcessor(QWidget):
    def __init__(self):
        super().__init__()

        self.image_path = 'ashf2.jfif'
        self.original_pixmap = QPixmap(self.image_path)
        self.current_pixmap = self.original_pixmap.copy()

        self.init_ui()

    def init_ui(self):
        # Create QGraphicsScene and QGraphicsView
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        
        # Create QGraphicsPixmapItem and set the original pixmap
        self.pixmap_item = QGraphicsPixmapItem(self.original_pixmap)
        self.scene.addItem(self.pixmap_item)

        # Create brightness and contrast sliders
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setMinimum(-100)
        self.brightness_slider.setMaximum(100)
        self.brightness_slider.setValue(0)
        self.brightness_slider.sliderReleased.connect(self.update_image)

        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setMinimum(-100)
        self.contrast_slider.setMaximum(100)
        self.contrast_slider.setValue(0)
        self.contrast_slider.sliderReleased.connect(self.update_image)

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.view)
        layout.addWidget(QLabel("Brightness"))
        layout.addWidget(self.brightness_slider)
        layout.addWidget(QLabel("Contrast"))
        layout.addWidget(self.contrast_slider)

        self.setWindowTitle('Image Processor')
        self.setGeometry(100, 100, 800, 600)
        self.show()

    def update_image(self):
 # Get the current values of brightness and contrast
        brightness = self.brightness_slider.value()
        contrast = self.contrast_slider.value()

        # Apply brightness and contrast adjustments
        image = self.original_pixmap.toImage()
        for y in range(0,image.height(),2):
            for x in range(0,image.width(),2):
                color = QColor(image.pixel(x, y))

                # Apply brightness adjustment
                new_brightness = QColor(
                    max(0, min(255, color.red() + brightness)),
                    max(0, min(255, color.green() + brightness)),
                    max(0, min(255, color.blue() + brightness)),
                    color.alpha()
                )

                # Apply contrast adjustment
                contrast_factor = (100.0 + contrast) / 100.0
                new_contrast = QColor(
                    max(0, min(255, int((new_brightness.red() - 128) * contrast_factor + 128))),
                    max(0, min(255, int((new_brightness.green() - 128) * contrast_factor + 128))),
                    max(0, min(255, int((new_brightness.blue() - 128) * contrast_factor + 128))),
                    new_brightness.alpha()
                )

                image.setPixel(x, y, new_contrast.rgb())

        # Update the pixmap in QGraphicsPixmapItem
        self.current_pixmap = QPixmap.fromImage(image)
        self.pixmap_item.setPixmap(self.current_pixmap)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageProcessor()
    sys.exit(app.exec_())