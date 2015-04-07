#!/usr/bin/env python

import rospy, tf

import AStar

from tf.transformations import euler_from_quaternion

from kobuki_msgs.msg import BumperEvent
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point
from nav_msgs.msg import Odometry
from nav_msgs.msg import OccupancyGrid

import time
import math

def MapCallback(occupancy):
	global mapReady, occupancyGrid
	
	mapReady = 1
	occupancyGrid = occupancy

if __name__ == '__main__':

	global mapReady, occupancyGrid

	mapReady = 0
	occupancyGrid = None

	rospy.init_node('jbmorse_Lab_3_node')

	rospy.Subscriber('map', OccupancyGrid, MapCallback)
	#rospy.Subscriber('map_metadata', MapMetaData, MapMetaCallback)
	#rospy.Subscriber('move_base_simple/goal', PoseStamped, GoalCallback)
	#rospy.Subscriber('initialpose', PoseWithCovarianceStamped, InitialPoseCallback)

	odom_list = tf.TransformListener()

	rospy.sleep(rospy.Duration(1, 0))

	print "Starting Lab 3"

	i = 0
	while not mapReady:
		sleep(.1)
	
	start = Point()
	goal = Point()
	start.x = 4
	start.y = 14
	goal.x = 34
	goal.y = 34

	AStar.SearchForGoal(occupancyGrid, start, goal)

	print "Lab 3 complete!"
