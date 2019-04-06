from PIL import Image, ImageDraw
import math
import random

debug = False
status = True
flows = 32
radius = 16
sweep = 8
steps = 512

im = Image.open("Heightmap.png")
im = im.convert("RGB")
width, height = im.size

# we need to generate a list of U,V tuples to pass to the drawing board
draw = ImageDraw.Draw(im)

for q in range(0,flows):
    startUV = (int(random.random()*width),int(random.random()*height))
    listUV = [startUV]
    validUV = True
    
    if status:
        print("Path: " + str(q+1) + "/" + str(flows))
        
    valTemp = 255
    
    for j in range(0,steps):
        for i in range(0,sweep):
            angle = i * ((2 * math.pi)/sweep)

            uCoord = int(startUV[0] + radius * math.cos(angle))
            vCoord = int(startUV[1] + radius * math.sin(angle))
            
            # DEBUG
            if debug:
                print("U: " + str(uCoord))
                print("V: " + str(vCoord))
            
            # make sure to only use the coordinates if they're in the image's dimensions
            if (0 < uCoord < width) and (0 < vCoord < height):

                hVal = im.getpixel((uCoord,vCoord))[0]

                # if hval < valTemp, write hval to valTemp and assign coords to locUV
                if (hVal < valTemp):
                    valTemp = hVal
                    startUV = (uCoord,vCoord)
                    
                # confirm UV as valid
                validUV = True
            else:
                validUV = False
                radius += radius

        # export the chosen coordinate to the list ONLY if UV is valid
        if validUV:
            listUV.append(startUV)

    #draw.line(listUV, fill=(0,0,255), width = 1)
    #draw.point(listUV, fill=(255,255,255))
    
    # draw the gradient line
    for index, span in enumerate(listUV):
        if (index < len(listUV)) and (index != 0):
            draw.line((listUV[index],listUV[index-1]), fill=(0,index,255), width = 4)

del draw

# write to stdout
im.save("output", "PNG")
im.show()