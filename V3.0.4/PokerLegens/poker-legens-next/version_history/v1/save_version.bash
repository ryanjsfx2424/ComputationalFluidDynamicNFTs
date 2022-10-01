VN=v1
VPATH=version_history/$VN

mkdir $VPATH
cp * $VPATH
cp -r public     $VPATH
cp -r src        $VPATH
cp -r pages      $VPATH
cp -r components $VPATH
cp -r styles     $VPATH

