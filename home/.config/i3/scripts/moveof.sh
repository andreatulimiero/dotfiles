#!/bin/bash
MIN_WS=1
MAX_WS=10
wsNext=$(( $( i3-msg -t get_workspaces | jq '.[] | select(.focused).num' ) + $1))
if [ $wsNext -lt $MIN_WS ] || [ $wsNext -gt $MAX_WS ]; then
    exit 0;
fi;
i3-msg workspace $wsNext
