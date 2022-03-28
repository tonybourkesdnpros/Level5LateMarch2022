#!/usr/bin/python3

import yaml

file = open('example.yml', 'r')

example = yaml.safe_load(file)

print("Here are the switches listed in the YAML file")

for item in example['switches']:
    print(item)
    for interface in example['switches'][item]['interfaces']:
        print(item, "has an interface:", interface)


