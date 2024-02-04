#!/bin/bash
# Filename: utils.sh
# Author: meizhaohui
# Function: Useful utilities for shell script.

#######################################
# Check if the folder exists, create it if it does not exist
# Arguments:
#   folder to create
# Returns:
#   0 if folder was created, non-zero on error.
#######################################
make_dir() {
    if [[ ! -d "$1" ]]; then
        mkdir -p "$1"
    fi
}

#######################################
# Basic log function
# Arguments:
#   log message
# Outputs:
#   Writes message to stdout
#######################################
echo_log() {
    now=$(date +"[%Y/%m/%d %H:%M:%S]")
    echo -e "\033[1;$1m${now}$2\033[0m"
}

#######################################
# debug log message
# Arguments:
#   log message
# Outputs:
#   Writes message to stdout
#######################################
msg_debug() {
    echo_log 30 "[Debug] ====> $*"
}

#######################################
# error log message
# Arguments:
#   log message
# Outputs:
#   Writes message to stdout
#######################################
msg_error() {
    echo_log 31 "[Error] ====> $*"
}

#######################################
# success log message
# Arguments:
#   log message
# Outputs:
#   Writes message to stdout
#######################################
msg_success() {
    echo_log 32 "[Success] ====> $*"
}

#######################################
# warning log message
# Arguments:
#   log message
# Outputs:
#   Writes message to stdout
#######################################
msg_warn() {
    echo_log 33 "[Warning] ====> $*"
}

#######################################
# information log message
# Arguments:
#   log message
# Outputs:
#   Writes message to stdout
#######################################
msg_info() {
    echo_log 34 "[Info] ====> $*"
}

#######################################
# return warning log message
# Arguments:
#   log message
# Outputs:
#   Writes message to stderr then user can get it
#######################################
return_error() {
    echo -e "===============>> $1" 1>&2
}
