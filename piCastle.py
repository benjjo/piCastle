#!/usr/bin/python3.4
#-----------------------------------------------------------------------------------------------
# Name:        piCastle
# Purpose:     you want a castle? You got it.
#              Designed for building a castle on the location that the player is standing.
#              This is written very simply for debugging/learning purposes.
#              This is a project stemmed from Learn Python The Hard Way, ex40/41/42.
#              Eventually this will be integrated into a user interface with QT and pyQT.
#              Inspired by Matt's castle building program:
#              http://www.raspberrypi-spy.co.uk/2014/06/building-a-castle-in-minecraft-with-python/
#              I wanted to create castles without destroying the entire Minecraft environment.
# Version:     Development
# Author:      benjo charlie
# Created:     2016
#
#-----------------------------------------------------------------------------------------------

# Imports
from mcpi.minecraft import Minecraft

mc = Minecraft.create()
x, y, z = mc.player.getPos()

class castle(object):

    def __init__(self):
        self.start = 'start'

    def walls(self, x, y, z, width, height, material, data):
        width /= 2
        # Build a block
        mc.setBlocks(x-width, y, z-width, x+width, y+height, z+width, material, data)
        # Hollow it out
        width -= 1
        mc.setBlocks(x-width, y, z-width, x+width, y+height, z+width, 0)

    def floors(self, x, y, z, width, height, material, data):
        width /= 2
        mc.setBlocks(x-width, y+height-1, z-width, x+width, y+height-1, z+width, material, data)
        print("Floor level =", y+height-1)        

    def windows(self, x, y, z, width, height, material, direction):
        print("The enrty value of y is:", y)
        # Cut the two windows, then apply a ledge to top/bottom
        
        # Cut the E/W Windows
        width /= 2
        height -= 2
        if direction == 'longitudinal':
            # move on the z axis
            z -= 4
            for i in range(0, 3):
                z += 2
                mc.setBlocks(x-width, y+height-3, z, x+width, y+height, z, 0)
                # West top
                mc.setBlock(x-width, y+height, z, material, 4)
                # East top
                mc.setBlock(x+width, y+height, z, material, 5)
                # West lower
                mc.setBlock(x-width, y+height-3, z, material, 0)
                # East lower
                mc.setBlock(x+width, y+height-3, z, material, 1)
        # Cut the N/S windows
        elif direction == 'latitudinal':
            # move on the x axis
            x -= 4
            for i in range(0, 3):
                x += 2				
                mc.setBlocks(x, y+height-3, z-width, x, y+height, z+width, 0)
                # North top
                mc.setBlock(x, y+height, z-width, material, 6)
                # South top
                mc.setBlock(x, y+height, z+width, material, 7)
                # North lower
                mc.setBlock(x, y+height-3, z-width, material, 2)
                # South lower
                mc.setBlock(x, y+height-3, z+width, material, 3)

    def merlon(self, x, y, z, width, height):
        ref = width / 2
        for i in range(0, width):
            if i % 2 != 0:
                # This is confusing AF
                mc.setBlock(x-ref+i, y+height, z+ref, 0)
                mc.setBlock(x-ref+i, y+height, z-ref, 0)
                mc.setBlock(x+ref, y+height, z-ref+i, 0)
                mc.setBlock(x-ref, y+height, z-ref+i, 0)

    def stairs():
        pass
        

builder = castle()
# Build the perimeter fence, 6 blocks high, 50 wide out of black wool
builder.walls(x, y, z, 50, 6, 35, 15)
builder.merlon(x, y, z, 50, 6)
# Build the perimeter fence, 6 blocks high, 30 wide out of black wool
builder.walls(x, y, z, 30, 6, 35, 15)
builder.merlon(x, y, z, 30, 6)
# Build the bottom layer floor
builder.floors(x, y, z, 60, 0, 155, 0)
# Build the main tower walls
builder.walls(x, y, z, 10, 26, 155, 0)
builder.merlon(x, y, z, 10, 26)

# Cut out the windows in a N/S, W/E pattern
for i in range(1, 6):
    builder.floors(x, y, z, 10, (5 * i), 155, 0)
    if i % 2 == 0:
        facing = 'latitudinal'
    elif i % 2 != 0:
        facing = 'longitudinal'
    builder.windows(x, y, z, 10, (5 * i), 156, facing)
