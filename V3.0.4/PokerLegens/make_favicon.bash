FNAME=pokerlegens1.jpg

convert pokerlegens1.jpg -scale  16  16.jpg
convert pokerlegens1.jpg -scale  32  32.jpg
convert pokerlegens1.jpg -scale  48  48.jpg
convert pokerlegens1.jpg -scale  96  96.jpg
convert pokerlegens1.jpg -scale 128 128.jpg
convert pokerlegens1.jpg -scale 192 192.jpg
convert pokerlegens1.jpg -scale 256 256.jpg
convert pokerlegens1.jpg -scale 512 512.jpg

convert 16.jpg 32.jpg 48.jpg 96.jpg 128.jpg 192.jpg 256.jpg 512.jpg favicon.ico
