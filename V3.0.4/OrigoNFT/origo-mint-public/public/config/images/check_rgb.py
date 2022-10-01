from PIL import Image

#im = Image.open("big_box.png")
#im = Image.open("progress_bar_screenshot.png")
im = Image.open("bot_box_ss.png")
pix = im.load()
print(im.size)
print(pix[int(im.size[0]/2), int(im.size[1]/2)])
