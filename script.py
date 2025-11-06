import sys

import cv2  # Opencv ver 3.1.0 used
import numpy as np

# Set recursion limit
sys.setrecursionlimit(10 ** 9)

import selectinwindow

# Initialize the drag object
wName = "select region"

# Read an actual image (replace with your image path)
image_path = "test.jpg"
image = cv2.imread(image_path)

if image is None:
    print(f"Error: Could not read image at {image_path}")
    # Create a white background if image not found
    imageWidth = 320
    imageHeight = 240
    image = np.ones([imageHeight, imageWidth, 3], dtype=np.uint8) * 255
else:
    imageHeight, imageWidth = image.shape[:2]

# Define the drag object
rectI = selectinwindow.DragRectangle(image, wName, imageWidth, imageHeight)

cv2.namedWindow(rectI.wname)
cv2.setMouseCallback(rectI.wname, selectinwindow.dragrect, rectI)

# keep looping until rectangle finalized
while True:
    # display the image
    cv2.imshow(wName, rectI.image)
    key = cv2.waitKey(1) & 0xFF

    # if returnflag is True, break from the loop
    if rectI.returnflag:
        break

print("Dragged rectangle coordinates")
print(str(rectI.outRect.x) + ',' + str(rectI.outRect.y) + ',' + \
      str(rectI.outRect.w) + ',' + str(rectI.outRect.h))

# close all open windows
cv2.destroyAllWindows()
