#!/bin/bash
# Edgebench Framework
# sysmon Module
# 
# Generates a system report for the last 10 seconds


current_time=$(date +"%0k:%0M:%0S")
start_time=$(date +"%0k:%0M:%0S" -d "-11sec")

sadf -dht -s "${start_time}" -e "${current_time}" -- -urp -P ALL syslog.bin

