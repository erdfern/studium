#!/usr/bin/env bash

# Check for correct number of arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 [PID] [INTERVAL]"
    exit 1
fi

pid="$1"
interval="$2"

while true; do
    if ! kill -0 "$pid" >/dev/null 2>&1; then # kill -0 just checks if the process exists, it doesn't send any signal
        echo "Process with PID $pid is no longer with us :("
        break  # Exit the loop since the process is dead
    fi

    echo "Process with PID $pid is still going."
    sleep "$interval" 
done
