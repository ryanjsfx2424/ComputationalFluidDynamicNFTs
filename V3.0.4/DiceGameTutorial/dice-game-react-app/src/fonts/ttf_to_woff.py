from fontTools.ttLib import TTFont

fload = "Lobster-Regular.ttf"
fsave = "Lobster.woff"

fid = TTFont(fload)
fid.flavor = "woff"
fid.save(fsave)
## end ttf_to_woff.py
