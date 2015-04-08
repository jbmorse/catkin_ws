import rospy, tf

from nav_msgs.msg import GridCells
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Point
from geometry_msgs.msg import Quaternion

import time

import Queue

#This is a library that can be called to perform specific AStar functions

#This implementation is based on the A* implementation found at http://www.redblobgames.com/pathfinding/a-star/implementation.html#sec-1-4

#This library will only work if the following values are held by certain variables

#point A
#X coordinate = A.x
#Y coordinate = A.y

#PriorityQueue  frontier

#OccupancyGrid gridMap
#data[0] = gridMap.data[0]
#mapmetadata = gridMap.info
#width = gridMap.info.width
#height = gridMap.info.height

def GetData (x, y, gridMap):
	width = gridMap.info.width
	height = gridMap.info.height
	if (x < 0 or x > width or y < 0 or y > height):
		return 1
	dataLocation = (height * y) + x
	return gridMap.data[dataLocation]

def GetHeuristic (a, b):
	return (abs(a.x - b.x) + abs(a.y - b.y))

def IsSame (a, b):
	return (a.x == b.x and a.y == b.y)

def GetNeighbors (a, gridMap):
	neighbors = []
	#north
	if (GetData(a.x, a.y + 1, gridMap) == 0):
		neighbors.append(Point(a.x, a.y + 1, 0))
	#east
	if (GetData(a.x + 1, a.y, gridMap) == 0):
		neighbors.append(Point(a.x + 1, a.y, 0))
	#south
	if (GetData(a.x, a.y - 1, gridMap) == 0):
		neighbors.append(Point(a.x, a.y - 1, 0))
	#west
	if (GetData(a.x - 1, a.y, gridMap) == 0):
		neighbors.append(Point(a.x - 1, a.y, 0))
	return neighbors


def GetPath (gridMap, start, goal):
	parents, costs = SearchForGoal(gridMap, start, goal)
	path = Path()
	path.poses = [PoseStamped()]
	currentIndex = 0
	
	currentNode = goal

	while not IsSame(currentNode, start):
		path.poses[currentIndex].pose.position = currentNode
		currentNode = parents[currentNode]
		currentIndex += 1
	
	path.poses[currentIndex].pose.position = start
	return path

def MakeGridCellsFromList (cellList):
	gridCells = GridCells()
	gridCells.cell_width = .2
	gridCells.cell_height = .2
	gridCells.cells = cellList
	gridCells.header.frame_id = 'map'
	return gridCells
	

def SearchForGoal (gridMap, start, goal):
	print "starting a thing"
	parents = {}
	parents[start] = None
	costs = {}
	costs[start] = 0
	frontier = Queue.PriorityQueue()
	frontierList = [start]
	visited = []
	found = []
	frontier.put(start, 0)

	frontierPublisher = rospy.Publisher('frontier', GridCells) 
	visitedPublisher = rospy.Publisher('visited', GridCells) 

	print "I'm so ready"

	while not frontier.empty():
		time.sleep(.1)
		publishableFrontier = MakeGridCellsFromList(frontierList)
		frontierPublisher.publish(publishableFrontier)
		publishableVisited = MakeGridCellsFromList(visited)
		visitedPublisher.publish(publishableVisited)
		
		currentNode = frontier.get()
		frontierList.remove(currentNode)
		visited.append(currentNode)

		if (IsSame(currentNode, goal)):
			break

		for neighbor in GetNeighbors(currentNode, gridMap):
			costToNeighbor = costs[currentNode] + 1
		
			if neighbor not in found:
				costs[neighbor] = costToNeighbor
				found.append(neighbor)
				priority = costToNeighbor + GetHeuristic(neighbor, goal)
				frontier.put(neighbor, priority)
				if neighbor not in frontierList:
					frontierList.append(neighbor)
				parents[neighbor] = currentNode
	
	return parents, costs
