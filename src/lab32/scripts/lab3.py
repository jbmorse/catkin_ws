﻿Michelle Gagnon and Josh Morse
RBE 3002 Lab 4 Write-Up

	The goal of this lab was to incorporate the material from labs 2 and 3 in order to have a turtlebot navigate in the real world. In order for this to work, the turtlebot would have to be able to map it's environment and then find a path based on the map. It would then have to successful drive along the path while avoiding obstacles. 
	Our occupancy grid size for this lab was 0.1. We chose this size because our A* code ran extremely fast at 0.05. Therefore, it was determined that 0.1 would allow the program to run quickly enough while still being at a low resolution.
	Our heuristic function was very simple. Every cell was either completely occupied or not at all. This was determined by checking if any part of the cell was occupied. If it was, the algorithm determined that the entire cell was 100% impassible. Each cell could only be passed through if there was nothing in it at all. In this case, the algorithm was given a value of zero rather than 100. The final option was for unknown cells. If the map had not yet been generated for an area, the algorithm would pass a value of -1. 
