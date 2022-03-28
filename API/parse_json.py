#!/usr/bin/python3

import json

file = open('response.json', 'r')

response = json.load(file)



for interface in response['result'][0]['interfaces']:
    ip = response['result'][0]['interfaces'][interface]['interfaceAddress']['ipAddr']['address']
    print(interface, 'has an IP address of', ip)



