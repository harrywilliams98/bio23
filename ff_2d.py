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

def transition_func(grid, neighbourstates, neighbourcounts, fuelCount, windBias, windSpeed, moisture):
	
    randoms = np.random.rand(200,200)*100
    
    
    dead_neighbours, live_neighbours, shrub_neighbours, fast_neighbours, water_neighbours, burnout_neighbours = neighbourcounts
    NW, N, NE, W, E, SW, S, SE = neighbourstates
    
    
    
    global counter
    counter += 1
    
    
    surroundingBias = live_neighbours*2 
    
    
    
    windBias[NW==1] += 1*windSpeed
    windBias[N==1] += 4*windSpeed
    windBias[NE==1] += 1*windSpeed
    windBias[SW==1] -= 1*windSpeed
    windBias[S==1] -= 4*windSpeed
    windBias[SE==1] -= 1*windSpeed
    
    birth =  (randoms - windBias - surroundingBias < 25) & (live_neighbours >= 1) & (grid == 0) & (moisture < 1) 
    harderBirth = (randoms - windBias - surroundingBias < 2) & (live_neighbours >= 1) & (grid == 2) & (moisture < 1) 
    easyBirth = (randoms - windBias - surroundingBias < 50) & (live_neighbours >= 1) & (grid == 3) & (moisture < 1)  
    death = (fuelCount == 0)
    
    grid[birth | harderBirth | easyBirth] = 1
    grid[death] = 5
    fuelCount[birth] = 35
    fuelCount[easyBirth] = 20
    fuelCount[harderBirth] = 60 

    
    if (counter == 20):
    	moisture[100:140 , 0:50] = 15
    	#grid[100:140 , 0:50] = config.initial_grid[100:140 , 0:50] NEEDS FIXING


    
    moisture[moisture >= 1 ] -= 1
    fuelCount[fuelCount >= 1 ] -= 1 
    
    windBias[:, :] = 0 #resetting all windBiases 
    
    return grid


def randomNum(limit):
    return random.randint(0,limit)

def setup(args):
    config_path = args[0]
    
    config = utils.load(config_path)
    # ---THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED---
    config.title = "Forest Fire Simulation"
    config.dimensions = 2
    config.states = (0, 1, 2, 3, 4, 5)
    # ------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----

    config.state_colors = [(0,1,0),(1,0,0),(0.133,0.55,0.133),(0.7, 0.4, 0), (0,0,1), (0,0,0)]
    # config.num_generations = 150
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
    windSpeed = 2 # initial arbitrary value 
    config = setup(sys.argv[1:])
    fuelCount = np.zeros(config.grid_dims)
    fuelCount.fill(-1)
    windBias = np.zeros(config.grid_dims) 
    
    moisture = np.zeros(config.grid_dims) 
    
    
    # Create grid object
    grid = Grid2D(config, (transition_func, fuelCount, windBias, windSpeed, moisture))
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
