#!/bin/bash

host_ip=$(ifconfig | grep inet | awk 'NR==5 {print $2}')

echo '{"ip": "'"$host_ip"'"}'  > host_ip.json