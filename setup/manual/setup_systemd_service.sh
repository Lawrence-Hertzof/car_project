#!/bin/bash

# Service name
$SERVICE_NAME='rasp_video_server.service'

# Function to log with colors
log() {
    local COLOR=$1
    local MESSAGE=$2
    local NC="\033[0m" # No Color
    echo -e "${COLOR}${MESSAGE}${NC}"
}

# Define colors
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
BLUE="\033[0;34m"

# Step 1: Move service to systemd directory
log "${BLUE}" "Copying service file to /etc/systemd/system/${SERVICE_NAME}..."
cp systemd_service.service /etc/systemd/system/${SERVICE_NAME}
if [ $? -eq 0 ]; then
    log "$GREEN" "Service file copied successfully."
else
    log "$RED" "Failed to copy service file."
    exit 1
fi

# Step 2: Enable service
log "$BLUE" "Enabling service ${SERVICE_NAME}..."
sudo systemctl enable ${SERVICE_NAME}
if [ $? -eq 0 ]; then
    log "$GREEN" "Service enabled successfully."
else
    log "$RED" "Failed to enable service."
    exit 1
fi

# Step 3: Start service
log "$BLUE" "Starting service ${SERVICE_NAME}..."
sudo systemctl start ${SERVICE_NAME}
if [ $? -eq 0 ]; then
    log "$GREEN" "Service started successfully."
else
    log "$RED" "Failed to start service."
    exit 1
fi


log "$YELLOW" "
##################################################
#    Service Status Check:                       #
#    To check the service status, run:           #
#        sudo journalctl -u your_service_name    #
##################################################
"
