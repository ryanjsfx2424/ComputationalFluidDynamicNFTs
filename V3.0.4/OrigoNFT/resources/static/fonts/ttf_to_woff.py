from fontTools.ttLib import TTFont

fload = "Adlinnaka-BoldDemo.ttf"
fsave = "Adlinnaka-BoldDemo.woff"

fid = TTFont(fload)
fid.flavor = "woff"
fid.save(fsave)
## end ttf_to_woff.py
