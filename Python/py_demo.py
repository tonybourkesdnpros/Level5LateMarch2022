#!/usr/bin/python3

import yaml
import json

# Variables

## Simple Variables (integers, strings, booleans)

### Integer

i = 5
n = 7
m = i + n

# print(m)

### Strings

x = 'Hello'
y = "world"

### Booleans

f = True
k = False

# if f == True:
#     print("F is true")

## More complex variables (lists, dictionaries)

### Lists

planets = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

# print(planets[0])

### Dictionaries

facts = {'water': 'wet',
         'fire': 'hot',
         'sky': 'blue',
         'primes': [2, 3, 5, 7, 11, 13]}

# print(facts['primes'][1])

# Loops

# for thing in planets:
#    print(thing)

# Convert YAML/JSON into a dictionary

file = open('underlay.yml', 'r')
underlay = yaml.safe_load(file)
file.close()

# print(underlay['leaf4-DC2']['interfaces']['loopback0']['ipv4'])

file = open('response.json', 'r')

response = json.load(file)

# print(response['jsonrpc'])


def generate_iface(switch):
    for interface in underlay[switch]['interfaces']:
        print("interface", interface)
        ip = str(underlay[switch]['interfaces'][interface]['ipv4'])
        mask = str(underlay[switch]['interfaces'][interface]['mask'])
        print("  ip address", ip+"/"+mask)
        if 'Ethernet' in interface:
            print("  no switchsport")
            print("  mtu 9214")


generate_iface("spine1-DC3")
