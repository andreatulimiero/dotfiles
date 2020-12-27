#!/bin/bash
MAX_TITLE_LEN=20
players="$(playerctl -l 2>/dev/null)"
if [ ${#players} -eq 0 ]; then
    echo ""
    exit 0;
fi;
title="$(playerctl metadata title)"
if [ ${#title} -gt $MAX_TITLE_LEN ]; then
    title="${title:0:$MAX_TITLE_LEN}..."
fi
artist="$(playerctl metadata artist)"

echo "$artist - $title"
