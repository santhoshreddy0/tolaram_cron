#!/bin/bash

# Get the current directory of the script
currDir="$( cd "$(dirname "$0")" ; pwd -P )"

# Check if the process dream11Bets.py is running
if ! pgrep -f "$currDir/dream11Bets.py" > /dev/null 2>&1; then
    # Start dream11Bets.py in the background
    nohup python3 "$currDir/dream11Bets.py" > "$currDir/dream11Bets.log" 2>&1 &
fi