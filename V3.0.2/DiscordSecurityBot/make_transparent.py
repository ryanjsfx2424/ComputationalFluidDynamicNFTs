import cv2
import numpy as np

fname = "gradient_lock.png"
fsave = "gradient_lock_transparent.png"

# load image as greyscale
grey = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)

# make 4-channel RGBA black background w/ same height + width.
im = np.zeros((*grey.shape, 4), dtype=np.uint8)

# put your alpha channel in, inverted
im[:,:,3] = ~grey

# Save
cv2.imwrite(fsave, im)
