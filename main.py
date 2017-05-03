import numpy as np
import random as rand
from PIL import Image


def world_genBlank(w_size, world, value):
    for x in xrange(0, w_size):
        for y in xrange(0, w_size):
            world[x][y] = value

def world_genOcean(w_size, world):
    lip = 2
    for x in xrange(0, w_size):
        for y in xrange(0, w_size):
            if x <= lip - 1:
                world[x][y] = 'w'
            if y <= lip - 1:
                world[x][y] = 'w'
            if x >= w_size - lip:
                world[x][y] = 'w'
            if y >= w_size - lip:
                world[x][y] = 'w'

def world_genSand(w_size, world):
    for x in xrange(0, w_size):
        for y in xrange(0, w_size):
            if checkNeighbors(x,y,world,'w',w_size) and world[x][y] == 'x':
                # We have found a piece of land that neighbors the water
                world[x][y] = 's'

def world_genErodedShore(w_size, world, erosions):
    for x in xrange(0,erosions):
        world_genSand(w_size,world)
        world_randomReplace(w_size,world,'s','w',40)
    world_genSand(w_size, world)

def world_genIslands(w_size, world, num, value):
    for x in xrange(0,num):

        islandX = rand.randint(0,w_size)
        islandY = rand.randint(0,w_size)
        height = rand.randint(0,w_size/5) + w_size/10
        width = rand.randint(0,w_size/5) + w_size/10

        genEllipse(w_size,world,islandX,islandY,height,width, 'x')

def world_randomReplace(w_size, world, targetValue, replaceValue, percent):
    for x in xrange(0, w_size):
        for y in xrange(0, w_size):
            if world[x][y] == targetValue:
                randomValue = rand.randint(0,100)
                if (randomValue < percent):
                    world[x][y] = replaceValue

def world_print(w_size, world):
    for x in xrange(0, w_size):
        for y in xrange(0, w_size):
            print world[x][y],
        print ''

def genEllipse(w_size, world, x, y, height, width, value):

    for xv in xrange(x-width,x+width):
        for yv in xrange(y-height,y+height):
            ## Now we do lots of math
            left_top = (xv - x) + 0.0
            left_top = (left_top) * (left_top) + 0.0
            left_bot = width * width + 0.0

            left_final = left_top / left_bot + 0.0

            right_top = (yv - y) + 0.0
            right_top = (right_top) * (right_top) + 0.0
            right_bot = height * height + 0.0

            right_final = right_top / right_bot + 0.0

            if left_final + right_final <= 1:
                ## We have solved our conic
                ## Finally, ensure we are within range...
                if xv >= 0 and xv < w_size and yv >= 0 and yv < w_size:
                    world[xv][yv] = value

def genTargetEllipse(w_size, world, x, y, height, width, value, targetVal):

    for xv in xrange(x-width,x+width):
        for yv in xrange(y-height,y+height):
            ## Now we do lots of math
            left_top = (xv - x) + 0.0
            left_top = (left_top) * (left_top) + 0.0
            left_bot = width * width + 0.0

            left_final = left_top / left_bot + 0.0

            right_top = (yv - y) + 0.0
            right_top = (right_top) * (right_top) + 0.0
            right_bot = height * height + 0.0

            right_final = right_top / right_bot + 0.0

            if left_final + right_final <= 1:
                ## We have solved our conic
                ## Finally, ensure we are within range...
                if xv >= 0 and xv < w_size and yv >= 0 and yv < w_size:
                    ## Finally, check if it contains the correct values
                    value = world[xv][yv]
                    if (value == targetVal):
                        world[xv][yv] = value

def checkNeighbors(x,y,world,value,w_size):
    for xv in xrange(x-1,x+2):
        for yv in xrange(y-1,y+2):
            if xv < w_size and yv < w_size and xv >= 0 and yv >= 0:
                curVal = world[xv][yv]
                if curVal == value:
                    return 1
    return 0

def exportWorld(w_size, world):
    print ("Exporting to output.jpg")
    im = Image.new("RGB", (w_size, w_size), "black")


    for x in xrange(0,w_size):
        for y in xrange(0,w_size):
            if world[x][y] == 'w':
                im.putpixel((x,y), (75,75,175))
            if world[x][y] == 's':
                im.putpixel((x,y),(255,200,20))
            if world[x][y] == 'x':
                im.putpixel((x,y),(50,180,50))
            if world[x][y] == 'f':
                im.putpixel((x,y),(85,140,50))

    im.save("output.jpg")

def main():
    size = 100
    world = np.chararray(shape=(size, size))
    world_genBlank(size, world, 'w')
    world_genIslands(size,world,10,'x')
    world_genErodedShore(size, world, 3)
    exportWorld(size, world)

main()