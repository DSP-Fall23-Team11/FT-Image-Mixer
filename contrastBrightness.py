import numpy as np

from PIL import Image, ImageEnhance
import cv2


import matplotlib.pyplot as plt





# Open the image
image_path = 'download.jfif'
image = Image.open(image_path)

# Adjust brightness
brightness = 10
enhancer = ImageEnhance.Contrast(image)
adjusted_image = enhancer.enhance(2)

# Display the images
plt.figure(figsize=(8, 4))

# Original image
plt.subplot(1, 2, 1)
plt.title("Original Image")
plt.imshow(image)
plt.axis("off")

# Adjusted image
plt.subplot(1, 2, 2)
plt.title("Adjusted Image")
plt.imshow(adjusted_image)
plt.axis("off")

plt.show()



# image = cv2.imread("ashf2.jfif")

# new_image = np.zeros(image.shape, image.dtype)

# contrast = 2
# bright = 1

# for y in range(image.shape[0]):
#   for x in range(image.shape[1]):
#     for c in range(image.shape[2]):
#       new_image[y, x, c] = np.clip(contrast * image[y, x, c] + bright, 0, 255)


# plt.figure(figsize=(10, 5))

# # Original image
# plt.subplot(1, 2, 1)
# plt.title("Original Image")
# plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
# plt.axis("off")

# # Adjusted image
# plt.subplot(1, 2, 2)
# plt.title("Adjusted Image")
# plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))
# plt.axis("off")

# plt.show()