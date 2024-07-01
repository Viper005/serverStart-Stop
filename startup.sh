#!/bin/bash

# Log file path
LOG_FILE="/home/ssm-user/startuplogs.txt"

# Date and time stamp
DATE_TIME="$(date +'%Y-%m-%d %H:%M:%S')"

# Script path and user
SCRIPT_PATH="/home/ubuntu/start.sh"
SCRIPT_USER="ubuntu"

# Run commands or script as devadm user, logging both stdout and stderr to LOG_FILE
sudo su - "$SCRIPT_USER" -c "$SCRIPT_PATH" > >(tee -a "$LOG_FILE") 2> >(tee -a "$LOG_FILE" >&2)

# Log date and time stamp
echo "Script executed at: $DATE_TIME" >> "$LOG_FILE"
    