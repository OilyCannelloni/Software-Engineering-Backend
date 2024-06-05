#!/bin/bash

# Function to check if nmcli is installed
check_nmcli() {
    if ! command -v nmcli &> /dev/null
    then
        echo "nmcli could not be found. Please install NetworkManager to use this script."
        exit 1
    fi
}

# Function to retrieve IP address information for a specific device
get_ip_info() {
    local device=$1
    ip_info=$(nmcli device show "$device" | grep -E 'IP4.ADDRESS' | awk '{print $2}')
    echo "$ip_info"
}

# Function to check for an active connection and retrieve IP addresses
check_connection() {
    local device_type=$1
    device=$(nmcli device status | grep -e "$device_type\s" | grep connected | awk '{print $1}')

    if [ "$device_type" == "wifi" ]; then
        echo "Wi-Fi"
    elif [ "$device_type" == "ethernet" ]; then
        echo "Ethernet"
    fi
    if [ -n "$device" ]; then
        ip_info=$(get_ip_info "$device")
        if [ -z "$ip_info" ]; then
            echo "No IP address"
        else
            echo "$ip_info"
        fi
    else
        echo "No IP address"
    fi
}

# Main script execution
check_nmcli

check_connection "wifi"
check_connection "ethernet"

