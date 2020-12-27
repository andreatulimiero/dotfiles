#!/bin/bash
DPI=36
for l in down up mute off ; do 
    wget https://material.io/tools/icons/static/icons/baseline-volume_${l}-white-${DPI}.zip

    unzip baseline-volume_${l}-white-${DPI}.zip
    mv 2x/baseline_volume_${l}_white_${DPI}dp.png volume_${l}.png
    rm -rf 1x 2x baseline-volume_${l}-white-${DPI}.zip
done
