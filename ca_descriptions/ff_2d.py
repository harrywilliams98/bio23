# Name: Conway's game of life
# Dimensions: 2

# --- Set up executable path, do not edit ---
import sys
import inspect
import random
this_file_loc = (inspect.stack()[0][1])
main_dir_loc = this_file_loc[:this_file_loc.index('ca_descriptions')]
sys.path.append(main_dir_loc)
sys.path.append(main_dir_loc + 'capyle')
sys.path.append(main_dir_loc + 'capyle/ca')
sys.path.append(main_dir_loc + 'capyle/guicomponents')
# ---

from capyle.ca import Grid2D, Neighbourhood, CAConfig, randomise2d
import capyle.utils as utils
import numpy as np

counter = 0
reachedTown = False 
dropped = False
drop = 100000

def transition_func(grid, neighbourstates, neighbourcounts, fuelCount, windBias, moisture, initGrid, terrainBias, windSpeed):

    global counter, drop, reachedTown, dropped
    randoms = np.random.rand(100,100)*100
    
    dead_neighbours, live_neighbours, dense_neighbours, fast_neighbours, water_neighbours, burnt_neighbours, town = neighbourcounts
    NW, N, NE, W, E, SW, S, SE = neighbourstates 
    
    # Flamability of each terrain
    terrainBias[((grid == 0) | (grid == 6))] = 0.8
    terrainBias[grid == 2] = 0.2
    terrainBias[grid == 3] = 2
    
    biasedNeighbours = neighbourstates
    # 1/8 for each neighbour that is on fire
    biasedNeighbours[biasedNeighbours != 1] = 0
    biasedNeighbours *= (1/8)
   
    
  
    surroundingBias = ((live_neighbours*(1/8)))


    wNW, wN, wNE, wW, wE, wSW, wS, wSE = [a*b for a,b in zip(biasedNeighbours,windBias)]
    totalWindBias = (wNW + wN + wNE + wW + wE + wSW + wS + wSE)*windSpeed
    
    
    
    overallProbability = (100*( ((surroundingBias * totalWindBias * terrainBias)) ))
    
    birth = (((randoms - overallProbability) <= 0) & (moisture <= 1))
    death = (fuelCount == 0)
    
    fuelCount[birth & ( (grid == 0) | (grid == 6) ) ] = 7200
    fuelCount[birth & (grid == 2)] = 40000
    fuelCount[birth & (grid == 3)] = 300

    
    grid[birth] = 1
    moisture[birth] = 0
    grid[death] = 5

    # yCenter = 50
    # xCenter = 10
    # rad = 7.12

    # yWater,xWater = np.ogrid[-yCenter:200-yCenter, -xCenter:200-xCenter]
    # mask = xWater*xWater + yWater*yWater <= rad*rad
    
    r=1
    
    yCenter = 580000
    xCenter = 26
    if(r==0):
        yLimUpper = 1
        yLimLower = -1
        xLimUpper = 10
        xLimLower = -10
    elif(r==1):
        yLimUpper = 10
        yLimLower = -10
        xLimUpper = 1
        xLimLower = -1
    
    yWater,xWater = np.ogrid[-yCenter:100-yCenter, -xCenter:100-xCenter]
    mask =  (((yLimLower <= yWater) & (yWater <= yLimUpper)) & ((xLimLower <= xWater) & (xWater <= xLimUpper)))
    
    
    
    if ((grid[mask]==1).any() and not dropped):
        moisture[mask] = 120
        grid[mask] = 4
        drop = counter
        dropped = True
        
    
    if (counter == (drop+10)):
        grid[(mask & (grid != 5) & (initGrid != 1) )] = initGrid[(mask & (grid != 5) & (initGrid != 1) )]
        
        

    moisture[moisture >= 2 ] -= (1+live_neighbours[moisture >= 2 ])
    fuelCount[((fuelCount >= 1) &  (moisture < 1))] -= 1 
    
    if(checkForReachTown(grid, counter) != "NOT REACHED" and not reachedTown):
        reachedTown = True
        timeToReachTown = checkForReachTown(grid, counter)
        print("Number of Hours: " + str(timeToReachTown/60))
        print ("Number of iterations: " + str(timeToReachTown))

    counter += 1
    
    return grid

def checkForReachTown(g, time):
    
    town = g[98:100, 0:5]
    reached = (town == 1)
    if(town[reached].any()):
        return time
    else:
        return "NOT REACHED"
        
       
    
    
    

def setup(args):
    config_path = args[0]
    
    config = utils.load(config_path)
    # ---THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED---
    config.title = "Forest Fire Simulation"
    config.dimensions = 2
    config.states = (0, 1, 2, 3, 4, 5, 6)
    # ------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----

    config.state_colors = [(0,1,0),(1,0,0),(0.133,0.55,0.133),(0.7, 0.4, 0), (0,0,1), (0,0,0), (0.66,0.66,0.66)]
    config.num_generations = 1500
    if config.grid_dims is None:
            if config.dimensions == 2:
                config.grid_dims = (100, 100)
        
    
    if config.initial_grid is None:
            fillstate = config.states[0] if config.states is not None else 0
            newGrid = np.zeros(config.grid_dims, dtype=type(fillstate))
            for row in range(config.grid_dims[0]):
                for col in range(config.grid_dims[1]):
                    if ((row >= (config.grid_dims[0]/5) and row <= ((3*config.grid_dims[0])/10)) and (col >= (config.grid_dims[1]/10) and col <= ((3*config.grid_dims[1])/10))):
                        newGrid[row][col] = 4
                        continue
                    if (  (row >= config.grid_dims[0]/10 and row <= (7*config.grid_dims[0])/10 ) and (col >= ((13*config.grid_dims[1])/20) and col <= (7*config.grid_dims[1])/10)  ):
                        newGrid[row][col] = 3
                        continue
                    if ( (row >= (3*config.grid_dims[0])/5  and row <=  (4*config.grid_dims[0])/5  ) and (col >= (3*config.grid_dims[1])/10 and col <= (config.grid_dims[1]/2) ) ):
                        newGrid[row][col] = 2
                        continue
                    if (  (row > (195*config.grid_dims[0])/200 and row <= config.grid_dims[0] ) and (col >= ((0*config.grid_dims[1])) and col < (config.grid_dims[1])/20)  ):
                        newGrid[row][col] = 6
                        continue
                    newGrid[row][col] = 0
                    
                    
            config.initial_grid = newGrid
    
    config.wrap = False
    
    

    # ----------------------------------------------------------------------

    if len(args) == 2:
        config.save()
        sys.exit()

    return config


def main():
    # Open the config object
    config = setup(sys.argv[1:])
    fuelCount = np.zeros(config.grid_dims)
    fuelCount.fill(-1)
    fuelCount[(config.initial_grid == 1)] = 45000
    #windBias = np.zeros(config.grid_dims) 
    
    #print(config.grid_dims)
    # low and high wind speed
    windSpeed = 2
    
    moisture = np.zeros(config.grid_dims)
    
    terrainBias = np.zeros(config.grid_dims)
    
    #NW, N, NE, W, E, SW, S, SE = neighbourstates 
    
    w1 = 2 # next closest to wind direction
    w2 = 3 # in the direction of wind
    w3 = 0.9 # next closes to opposite
    w4 = 0.4 # parralel with wind
    w5 = 0.7 # the opposite from the direction

    # North
    #windBias = [w1, w2, w1, w4, w4, w3, w5, w3] 
    # South
    windBias = [w3, w5, w3, w4, w4, w1, w2, w1] 
    # West
    #windBias = [w1, w4, w3, w2, w5, w1, w4, w3]
    #East
    #windBias = [w3, w4, w1, w5, w2, w3, w4, w1]
    
    # NW
    #windBias = [w2, w1, w4, w1, w3, w4, w3, w5]
    # NE
    #windBias = [w4, w1, w2, w3, w1, w5, w3, w4]
    # SW
    #windBias = [w4, w3, w5, w1, w3, w2, w1, w4]
    # SE
    #windBias = [w5, w3, w4, w3, w1, w4, w1, w2]   
    
    #windBias = [1,1,1,1,1,1,1,1]
    

    
    #if(wind == 'NE'):
        #windBias = windBias[-1:] + windBias[:-1]
    #elif('W'):
        #windBias = windBias[-2:] + windBias[:-2]
    #elif('E'):
        #windBias = windBias[-3:] + windBias[:-3]
    #elif('SW'):
        #windBias = windBias[-4:] + windBias[:-4]
    #elif('S'):
        #windBias = windBias[-5:] + windBias[:-5]
    #elif('SE'):
        #windBias = windBias[-6:] + windBias[:-6]
    #elif('NW'):
        #windBias = windBias[-7:] + windBias[:-7]     
        
    #print(windBias)
    
    # Create grid object
    grid = Grid2D(config, (transition_func, fuelCount, windBias, moisture, config.initial_grid, terrainBias, windSpeed))
    #fuelCount = np.zeros(grid.shape[0], grid.shape[1])
    
    #print("GRID", type(grid))
    # Run the CA, save grid state every generation to timeline
    timeline = grid.run()
    #print("TIMELINE", timeline)
    # save updated config to file
    config.save()
    # save timeline to file
    utils.save(timeline, config.timeline_path)


if __name__ == "__main__":
    main()
