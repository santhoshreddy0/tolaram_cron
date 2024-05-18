#!/bin/bash
currDir="$( cd "$(dirname "$0")" ; pwd -P )"
    if ! pgrep -f "$currDir/playerBets.py";
    then
        python3 "$currDir/playerBets.py" &
    fi
#done