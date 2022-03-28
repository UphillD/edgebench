#!/bin/bash
# Edgebench Framework
# sysmon Module
# 
# Launches a system monitor instance

sar -ur -P ALL 1 -o syslog.bin >/dev/null 2>&1 &

