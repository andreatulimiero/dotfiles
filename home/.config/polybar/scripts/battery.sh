#!/bin/bash
BATTERY_LEVEL=$(cat /sys/class/power_supply/BAT1/capacity)
BATTERY_STATUS=$(cat /sys/class/power_supply/BAT1/status | cut -d' ' -f1)

ICONS=("\uf0e7" "\uf244" "\uf243" "\uf242" "\uf241" "\uf240")
ICON_NO=''
if [ $BATTERY_STATUS == "Charging" ]; then
    ICON_NO=0
else
    if [ $BATTERY_LEVEL -ge 95 ]; then
        ICON_NO=5
    elif [ $BATTERY_LEVEL -ge 60 ]; then
        ICON_NO=4
    elif [ $BATTERY_LEVEL -ge 35 ]; then
        ICON_NO=3
    elif [ $BATTERY_LEVEL -ge 15 ]; then
        ICON_NO=2
    else
        ICON_NO=1
    fi
fi

echo -e "${ICONS[$ICON_NO]} $BATTERY_LEVEL%"
