#!/usr/bin/env bash

arp-scan -l | grep 38:a4:ed:be:70:7c && systemctl stop picam-stream || systemctl start picam-stream
systemctl status picam-stream
