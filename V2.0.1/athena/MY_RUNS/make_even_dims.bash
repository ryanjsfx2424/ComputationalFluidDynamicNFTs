#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd $DIR
PLOTDIR=$1
#cd $PLOTDIR

for f in *.png
do
  f1=$(file ${f} | cut -d" " -f5)
  f2=$(file ${f} | cut -d" " -f7)
  f2=${f2::${#f2}-1}
  if [ $((f1%2)) -eq 1 ]
  then
    f1=$((f1-1))
    convert $f -resize ${f1}x${f2}\! $f
  fi
  if [ $((f2%2)) -eq 1 ]
  then
    f2=$((f2-1))
    convert $f -resize ${f1}x${f2}\! $f
  fi
done
wait
