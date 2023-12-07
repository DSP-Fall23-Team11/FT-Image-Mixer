import logging
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QSlider, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt


class ImageProcessor:
    def __init__(self, image_path):
        self.image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    def convert_to_grayscale(self):
        # Convert the image to grayscale if it's colored
        if len(self.image.shape) == 3:
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def resize(self, target_size):
        # Resize the image to the target size
        self.image = cv2.resize(self.image, target_size)

    def apply_fourier_transform(self):
        # Apply Fourier Transform to the image
        f_transform = np.fft.fft2(self.image)
        return f_transform


class ImageDisplay(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene(self)
        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)
        self.setScene(self.scene)

        self.image_processor = None
        self.component_combo = None
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.contrast_slider = QSlider(Qt.Horizontal)

        self.init_ui()

    def init_ui(self):
        self.brightness_slider.setRange(-255, 255)
        self.contrast_slider.setRange(-127, 127)

        layout = QVBoxLayout()
        layout.addWidget(self.component_combo)
        layout.addWidget(self.brightness_slider)
        layout.addWidget(self.contrast_slider)
        self.setLayout(layout)

        self.brightness_slider.valueChanged.connect(self.update_display)
        self.contrast_slider.valueChanged.connect(self.update_display)

    def set_image_processor(self, image_processor):
        self.image_processor = image_processor
        self.update_display()

    def update_display(self):
        if self.image_processor:
            component = self.get_current_component()
            image_data = self.get_image_data(component)
            adjusted_image = self.adjust_brightness_contrast(image_data)
            pixmap = self.create_pixmap(adjusted_image)
            self.pixmap_item.setPixmap(pixmap)

    def get_current_component(self):
        return self.component_combo.currentText()

    def get_image_data(self, component):
        if component == "FT Magnitude":
            return np.abs(self.image_processor.apply_fourier_transform())
        elif component == "FT Phase":
            return np.angle(self.image_processor.apply_fourier_transform())
        elif component == "FT Real":
            return np.real(self.image_processor.apply_fourier_transform())
        elif component == "FT Imaginary":
            return np.imag(self.image_processor.apply_fourier_transform())

    def create_pixmap(self, image_data):
        image_data = np.log(1 + np.abs(image_data))
        image_data = (image_data / np.max(image_data) * 255).astype(np.uint8)
        height, width = image_data.shape
        q_image = QImage(image_data.data, width, height, width, QImage.Format_Grayscale8)
        return QPixmap.fromImage(q_image)

    def adjust_brightness_contrast(self, image_data):
        brightness = self.brightness_slider.value()
        contrast = self.contrast_slider.value()

        adjusted_image = np.clip(image_data + brightness, 0, 255)
        adjusted_image = ((adjusted_image - 127) * (1 + contrast / 127) + 127).astype(np.uint8)

        return adjusted_image


class MixerWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.image_displays = [ImageDisplay() for _ in range(4)]
        self.mixer_display = ImageDisplay()
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        for image_display in self.image_displays:
            layout.addWidget(image_display)

        mixer_layout = QVBoxLayout()
        mixer_layout.addWidget(self.mixer_display)
        layout.addLayout(mixer_layout)

        self.setCentralWidget(central_widget)


if __name__ == '__main__':
    app = QApplication([])
    window = MixerWindow()
    window.show()
    app.exec_()
