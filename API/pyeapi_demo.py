#!/usr/bin/python3

import pyeapi

switches = ['leaf1-DC1', 'leaf2-DC1', 'leaf3-DC1', 'leaf4-DC1']

for item in switches:
    connect = pyeapi.connect_to(item)
    for vlan_ID in range(100,201):
        result = connect.api("vlans").create(vlan_ID)
        
        if result == True:
            print("It worked! VLAN", vlan_ID, "created for switch", item)

        if result == False:
            print("There was a problem")