#!/bin/bash

# Get the current directory of the script
currDir="$( cd "$(dirname "$0")" ; pwd -P )"

# Check if the process matchBets.py is running
if ! pgrep -f "$currDir/playerBets.py" > /dev/null 2>&1; then
    # Start playerBets.py in the background
    nohup python3 "$currDir/playerBets.py" > "$currDir/playerBets.log" 2>&1 &
fi