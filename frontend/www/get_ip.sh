#!/bin/bash

# host_ip=$(echo $IP_ADDRESS)
host_ip=$(echo $IP_ADDRESS)

echo '{"ip": "'"$host_ip"'"}'  > host_ip.json