import cv2
import json
import numpy as np
import sys, getopt
import matplotlib
import math
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def computeVolume(heightMap, cellSize):
    #measure in cm
    cx = cellSize[0] 
    cy = cellSize[1] 

    vol = 0

    for row in heightMap:
        for y in row:
            vol += cx * cy * y
    
    return vol

def loadAndBuildHeightMap(inputpath, rescale, multiplier):
    print('Input path is ', inputpath)
    
    try:
        # Opening JSON file
        f = open(inputpath +'/reconstruction.json' )
    
        # returns JSON object as 
        # a dictionary
        data = json.load(f)
    except:
        print('File could not be loaded. EXIT')
        return

    procHeightmap = np.array(data["estimation"]["processed_heightMap"])

    roomWidth = data["estimation"]["room_width"]
    roomHeight = data["estimation"]["room_height"]
    roomDepth = data["estimation"]["room_depth"]

    procHeightmap = np.resize(procHeightmap, (data['estimation']['heightMap_depth'],
                        data['estimation']['heightMap_width']))

    cellProp = data['estimation']['cell_size_Depth'] / data['estimation']['cell_size_Width']
    cellSize = [data['estimation']['cell_size_Depth'], data['estimation']['cell_size_Depth']]
        
    # Resize the image
    rescale = (int(procHeightmap.shape[1]), int(procHeightmap.shape[0] * cellProp))
    procHeightmap = cv2.resize(procHeightmap, rescale, interpolation=cv2.INTER_AREA)

    bmpHeightMap = np.array(procHeightmap * multiplier, dtype=np.uint8)

    return bmpHeightMap,procHeightmap, cellSize, (roomWidth,roomHeight,roomDepth )



default_path = 'C://Users//User/Documents/out_reconstruct/13-11-2023-14-15/'

inputPath1 = "C:/Users/User/Documents/out_reconstruct/Lucas/E1/mesa vacia"
inputPath2 = "C:/Users/User/Documents/out_reconstruct/Lucas/E1/mesa con caja 2"

inputPath1 = "C:/Users/User/Documents/out_reconstruct/Lucas/E2/"
inputPath2 = "C:/Users/User/Documents/out_reconstruct/Lucas/"

############## Main
def main(argv):
   # parse input files
    inputpath = default_path
    opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    for opt, arg in opts:
        if opt in ("-d", "--dir"):
            inputpath = arg
    
    ###Load first map
    bmpHeightMap, procHeightmap1, cellSize, roomSize = loadAndBuildHeightMap(inputPath1, (), 10)

    vol1 = computeVolume(procHeightmap1, cellSize)
    print("Volume in M3 . 1st :", vol1)

    procHeightmap2 = None
    diference = None
    
    ###Load second map
    if inputPath2 != "":
        bmpHeightMap2, procHeightmap2, cellSize2, roomSize2 = loadAndBuildHeightMap(inputPath2, (), 10)
        procHeightmap2 = np.resize(procHeightmap2, procHeightmap1.shape)

        vol2 = computeVolume(procHeightmap2, cellSize)

        print("Volume in M3 . 2nd :", vol2)
    
    if procHeightmap2 is not None:
        diference = (procHeightmap2 - procHeightmap1) * 1
    
    # render as heightmap
    maxSz = max(roomSize[0],roomSize[2])
    lin_x = np.linspace(0,maxSz,procHeightmap1.shape[1],endpoint=False)
    lin_y = np.linspace(0,maxSz,procHeightmap1.shape[0],endpoint=False)
    x,y = np.meshgrid(lin_x,lin_y)
    
    
    fig, axs = plt.subplots(2, 2)

    # 1st subplot
    # ============ 
    # set up subplot grid
 
    axF = axs[0][0]

    #axF = axs[0,0] #  fig.add_subplot(311)
    axF.imshow(procHeightmap1, cmap='terrain')

    # 2nd subplot
    # ============ 
    axT = axs[1][0]
    if procHeightmap2 is not None:
        axT.imshow(procHeightmap2, cmap='terrain')

     # 3rd subplot
    # ============ 
    axM =axs[1][1]
    #axT = axs[0,1] # fig.add_subplot(312)
    axM.set_facecolor((1, 1, 1, 0))
    if procHeightmap2 is not None:
        axM.imshow(diference, cmap='terrain')
        
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(x, y, procHeightmap1, cmap='terrain')
    plt.show()
    
    ###Load second map
    cv2.waitKey(-1)
  

if __name__ == "__main__":
   main(sys.argv[1:])


