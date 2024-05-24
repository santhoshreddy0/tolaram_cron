#!/bin/bash

# Get the current directory of the script
currDir="$( cd "$(dirname "$0")" ; pwd -P )"

# Check if the process matchBets.py is running
if ! pgrep -f "$currDir/matchBets.py" > /dev/null 2>&1; then
    # Start matchBets.py in the background
    nohup python3 "$currDir/matchBets.py" > "$currDir/matchBets.log" 2>&1 &
fi