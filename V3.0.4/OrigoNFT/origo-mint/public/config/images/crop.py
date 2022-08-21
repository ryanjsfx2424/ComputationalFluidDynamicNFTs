import cv2

im = cv2.imread("connect_box.png", cv2.IMREAD_UNCHANGED)
x,y, w,h = cv2.boundingRect(im[..., 3])
im2 = im[y:y+h, x:x+w, :]
cv2.imwrite("result.png", im2)

