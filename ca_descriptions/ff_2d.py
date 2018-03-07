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

#DO THE SURROUNDING CELLS FEATURE

def transition_func(grid, neighbourstates, neighbourcounts, fuelCount, windBias, moisture, initGrid, terrainBias):

    
    randoms = np.random.rand(200,200)*100
    
    dead_neighbours, live_neighbours, dense_neighbours, fast_neighbours, water_neighbours, burnt_neighbours, town = neighbourcounts
    NW, N, NE, W, E, SW, S, SE = neighbourstates 
    
    terrainBias[grid == 0] = 1
    terrainBias[grid == 2] = 2
    terrainBias[grid == 3] = 3
    
    biasedNeighbours = neighbourstates
    
    biasedNeighbours[biasedNeighbours != 1] = 0
    biasedNeighbours *= (1/8)
   
    
    
    surroundingBias = live_neighbours*(1/8)


    wNW, wN, wNE, wW, wE, wSW, wS, wSE = [a*b for a,b in zip(biasedNeighbours,windBias)]
    totalWindBias = (wNW + wN + wNE + wW + wE + wSW + wS + wSE)*4
    
    
    birth =  ( ((randoms - surroundingBias -  totalWindBias < 25) & ( (grid == 0) | (grid == 6) ) ) | ((randoms - surroundingBias -  totalWindBias < 2) & (grid == 2) ) | ((randoms - surroundingBias -  totalWindBias < 50) & (grid == 3) )  ) & (live_neighbours >= 1) & (moisture <= 1) 
    #birth =  (((randoms - windBias - surroundingBias < 25) & (grid == 0) ) | ((randoms - windBias - surroundingBias < 2) & (grid == 2) ) | ((randoms - windBias - surroundingBias < 50) & (grid == 3) )) & (live_neighbours >= 1) & (moisture <= 1) 
    #birth =  (randoms - windBias - surroundingBias < 25) & (live_neighbours >= 1) & (grid == 0) & (moisture <= 1)     
    #harderBirth = (randoms - windBias - surroundingBias < 2) & (live_neighbours >= 1) & (grid == 2) & (moisture <= 1) 
    #easyBirth = (randoms - windBias - surroundingBias < 50) & (live_neighbours >= 1) & (grid == 3) & (moisture <= 1)  
    death = (fuelCount == 0)
    
    fuelCount[birth & ( (grid == 0) | (grid == 6) ) ] = 35
    fuelCount[birth & (grid == 2)] = 60
    fuelCount[birth & (grid == 3)] = 20

    
    grid[birth] = 1
    moisture[birth] = 0
    grid[death] = 5
     

    yCenter = 50
    xCenter = 10
    rad = 22.56

    yWater,xWater = np.ogrid[-yCenter:200-yCenter, -xCenter:200-xCenter]
    mask = xWater*xWater + yWater*yWater <= rad*rad
    
    if (counter == 65):
        moisture[mask] = 100
        grid[mask] = 4
    
    if (counter == 75):
        grid[(mask & (grid != 5) & (initGrid != 1) )] = initGrid[(mask & (grid != 5) & (initGrid != 1) )]
        
        

    moisture[moisture >= 2 ] -= (1+surroundingBias[moisture >= 2 ])
    fuelCount[((fuelCount >= 1) &  (moisture < 1))] -= 1 
    
    if(checkForReachTown(grid, counter) != "NOT REACHED"):
    	print(checkForReachTown(grid, counter))
    
    global counter
    counter += 1
    
    return grid

def checkForReachTown(g, time):
	
	town = g[195:200, 0:10]
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
    config.num_generations = 450
    if config.grid_dims is None:
            if config.dimensions == 2:
                config.grid_dims = (200, 200)
        
    
    if config.initial_grid is None:
            fillstate = config.states[0] if config.states is not None else 0
            newGrid = np.zeros(config.grid_dims, dtype=type(fillstate))
            for row in range(config.grid_dims[0]):
                for col in range(config.grid_dims[1]):
                    if ((row >= (config.grid_dims[0]/5) and row <= ((3*config.grid_dims[0])/10)) and (col >= (config.grid_dims[1]/10) and col <= ((3*config.grid_dims[1])/10))):
                        newGrid[row][col] = 4
                        continue
                    if ( (row >= (3*config.grid_dims[0])/5  and row <=  (4*config.grid_dims[0])/5  ) and (col >= (3*config.grid_dims[1])/10 and col <= (config.grid_dims[1]/2) ) ):
                        newGrid[row][col] = 2
                        continue
                    if (  (row >= config.grid_dims[0]/10 and row <= (7*config.grid_dims[0])/10 ) and (col >= ((13*config.grid_dims[1])/20) and col <= (7*config.grid_dims[1])/10)  ):
                        newGrid[row][col] = 3
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
    fuelCount[(config.initial_grid == 1)] = 35
    #windBias = np.zeros(config.grid_dims) 
    
    moisture = np.zeros(config.grid_dims)
    
    terrainBias = np.zeros(config.grid_dims)
    
    windBias = [2, 8, 2, 0, 0, -1, -4, -1]
    
    
    # Create grid object
    grid = Grid2D(config, (transition_func, fuelCount, windBias, moisture, config.initial_grid, terrainBias))
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
