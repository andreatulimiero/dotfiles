#!/bin/bash
DPI=36
for m in '' _charging; do 
    for l in 20 30 50 60 80 90 full; do 
        wget https://material.io/tools/icons/static/icons/baseline-battery${m}_${l}-white-${DPI}.zip

        unzip baseline-battery${m}_${l}-white-${DPI}.zip
        mv 2x/baseline_battery${m}_${l}_white_${DPI}dp.png battery${m}_${l}.png
        rm -rf 1x 2x baseline-battery${m}_${l}-white-${DPI}.zip
    done
done
