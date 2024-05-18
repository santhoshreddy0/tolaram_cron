#!/bin/bash
currDir="$( cd "$(dirname "$0")" ; pwd -P )"
    if ! pgrep -f "$currDir/roundBets.py";
    then
        python3 "$currDir/roundBets.py" &
    fi
#done