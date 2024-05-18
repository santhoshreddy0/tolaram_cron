#!/bin/bash
currDir="$( cd "$(dirname "$0")" ; pwd -P )"
    if ! pgrep -f "$currDir/matchBets.py";
    then
        python3 "$currDir/matchBets.py" &
    fi
#done