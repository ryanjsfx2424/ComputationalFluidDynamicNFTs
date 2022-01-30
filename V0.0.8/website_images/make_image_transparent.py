## make_logo_transparent.py
"""
This should make white transparent, from stackoverflow.

Note: execute with python3 !!
"""
import cv2
import numpy as np

img_in  = "logo_screenshot.png"
img_out = "logo_transparent.png"

#img_in  = "background_screenshot.png"
#img_out = "background_transparent.png"

# load image as greyscale
grey = cv2.imread(img_in, cv2.IMREAD_GRAYSCALE)

# make 4-channel RGBA black background w/ same height + width.
im = np.zeros((*grey.shape, 4), dtype=np.uint8)

# put your alpha channel in, inverted
im[:,:,3] = ~grey

# Save
cv2.imwrite(img_out, im)
## end make_image_transparent.py
