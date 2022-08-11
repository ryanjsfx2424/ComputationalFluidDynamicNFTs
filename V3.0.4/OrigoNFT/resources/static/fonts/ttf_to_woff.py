from fontTools.ttLib import TTFont

name = "Quicksand-Bold"
fload = name + ".ttf"
fsave = name + ".woff"

fid = TTFont(fload)
fid.flavor = "woff"
fid.save(fsave)
## end ttf_to_woff.py
