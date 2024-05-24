#!/bin/bash

# Get the current directory of the script
currDir="$( cd "$(dirname "$0")" ; pwd -P )"

# Check if the process matchBets.py is running
if ! pgrep -f "$currDir/roundBets.py" > /dev/null 2>&1; then
    # Start roundBets.py in the background
    nohup python3 "$currDir/roundBets.py" > "$currDir/roundBets.log" 2>&1 &
fi