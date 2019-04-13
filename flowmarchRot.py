from PIL import Image, ImageDraw
import math

# linear interpolation function
def lerp(x, y, blend):
    return x + blend * (y - x)

# normalize for color ranges
def normalize01(input):
    return input/255
def normalize255(input):
    normalizedOutput = int(input*255)
    if (normalizedOutput > 255):
        normalizedOutput = 255
    return int(normalizedOutput)

im = Image.open("Heightmap.png")
im = im.convert("L")

uSteps = im.size[0]
vSteps = im.size[1]
status = False
flowColor = (0,0,255)
stepLossRate = 1
materialDensity = .5
rSteps = 150

# START TIMING
import time
startTime = time.time()

# we need to generate a list of U,V tuples to pass to the drawing board
draw = ImageDraw.Draw(im)

for column in range(0,uSteps):
    startUV = (int(uSteps/2),1)

    # init prevHeight
    prevHeight = 0

    # init density
    flowDensity = 1

    # init coordinate positions
    uPos = column
    vPos = 0

    if status:
        print("Step: " + str(column+1) + "/" + str(uSteps))

    # draw flowColor over the current pixel
    # if heightColor is less than prevHeight, flowDensity is unchanged - if it's MORE than prevHeight, deltaHeight is subtracted from flowDensity

    # loop through every vertical pixel in this U column
    for row in range(0,vSteps):
        # reduce flowDensity by loss rate
        flowDensity = flowDensity * stepLossRate

        # only do if valid UV in range
        if (vPos <= vSteps):
            # get height at current pixel
            height = im.getpixel((uPos,vPos))

            # get deltaHeight
            deltaHeight = normalize01(height - prevHeight) * materialDensity

            # if deltaHeight is positive, lower density
            if (deltaHeight > 0):
                newDensity = flowDensity - deltaHeight

                # prevent negative flowDensity
                if (newDensity > 0):
                    flowDensity = newDensity
                else:
                    flowDensity = 0

            #print(flowDensity)

            # calculate newColor
            # interpolate between flowColor and height according to flowDensity
            newR = int(lerp(height, flowColor[0],normalize255(flowDensity)))

            newColor = (newR,newR,newR)

            # draw newColor onto current pixel
            im.putpixel((uPos,vPos),normalize255(flowDensity))
            #print(newColor)

            prevHeight = height

        # increment the v position if in range
        newVPos = vPos + 1
        if (newVPos <= vSteps):
            vPos = newVPos

del draw

print("Flowmarch Completed!")
endTime = time.time()

print("Time elapsed: {} seconds".format('%.2f'%(endTime - startTime)))

# write to stdout
im.save("Flow_Loss_" + str(stepLossRate) + "_matDensity_" + str(materialDensity) + ".png", "PNG")
im.show()
