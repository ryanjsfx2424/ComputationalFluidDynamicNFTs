from fontTools.ttLib import TTFont

fload = "Helvetica-Bold.ttf"
fsave = "Helvetica-Bold.woff"

fid = TTFont(fload)
fid.flavor = "woff"
fid.save(fsave)
## end ttf_to_woff.py
