#/usr/bin/python3

## Simple Variables

### Integers

i = 4
n = 7

### Strings

m = "Hello "
l = "World"

### Boolean

this = True




## Complex Variables lists or dictionaries

### Lists
planets = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Neptune', 'Uranus']


# for planet in planets:
#     print(planet)

### Dictionary

captains = {'1701': 'Kirk', 
            '1701-D': 'Picard', 
            '1864': 'Terryl', 
            '74656': 'Janeway'}

for ship, captain in captains.items():
    print("The captain of the NCC-"+ship, "is captain", captain)