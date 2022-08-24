fload = "origo-mint/src/styles/discord1.png"
fsave = "origo-mint/src/styles/discord1-crop.png"
#'''
from PIL import Image
im = Image.open("origo-mint/src/styles/discord1.png")
im.getbbox()
im2 = im.crop(im.getbbox())
im2.save("origo-mint/src/styles/discord1-crop.png")
#'''

'''
import cv2

im = cv2.imread(fload, cv2.IMREAD_UNCHANGED)
x, y, w, h = cv2.boundingRect(im[..., 3])
im2 = im[y:y+h, x:x+w, :]
cv2.imwrite(fsave, im2)
'''
