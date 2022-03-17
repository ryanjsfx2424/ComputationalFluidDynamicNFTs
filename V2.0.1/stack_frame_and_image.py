## stack_frame_and_image.py
from PIL import Image
import os
import glob

HOME = "/Users/redx/Documents/Desktop/NFTs/FutureFrames/"

foreground = Image.open("certificate.png")
imf_width, imf_height = foreground.size

#background = Image.open("french_flag11_Slice_z_temperature_copy.png")
background = Image.open("cfd-nft-v2-minting-utility3.png")
background = background.resize((imf_width, imf_height), Image.LANCZOS)

background.paste(foreground, (0,0), foreground)
background.save("fancy-cfd-nft-v2-minting-utility4.png")
## stack_frame_and_image.py
