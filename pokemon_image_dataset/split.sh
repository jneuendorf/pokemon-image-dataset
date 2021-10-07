#!/usr/bin/env bash


# 31x21 - black-white.png
# 20x13 - crystal.png
# 28x18 - diamond-pearl-frame2.png
# x - diamond-pearl.png
# x - emerald-frame2.png
# x - generation-3.png
# x - heartgold-soulsilver-frame2.png
# x - heartgold-soulsilver.png
# x - platinum-frame2.png
# x - platinum.png
# x - silver.png
# x - sugimori.png


for filename in raw/*.png; do
    width_height=$(identify -format '%wx%h' $filename)
    echo $filename
    echo $width_height
    convert -crop $width_height $filename res/$(basename $filename)
    break
done