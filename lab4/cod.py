#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

def linear_vel(constant=1.5):

	return constant * pose.ranges[1] #distance_tolerance)

def move():
        while pose.ranges[1] > distance_tolerance:    

		vel_msg.linear.x = linear_vel()
		vel_msg.linear.y = 0
		vel_msg.linear.z = 0
		vel_msg.angular.x = 0
		vel_msg.angular.y = 0
		vel_msg.angular.z = 0


		velocity_publisher.publish(vel_msg)
		rate.sleep()

	return

def scan_data(data):
	pose=data
	right=min(pose.ranges[0:6])
	forward=min(pose.ranges[6:12])
	left=min(pose.ranges[12:18])
	pose.ranges=[right, forward, left]
	print (right, forward, left)
	return


# Starts a new node
rospy.init_node('bot', anonymous=True)
velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
pose_subscriber = rospy.Subscriber('/base_scan', LaserScan, scan_data)
vel_msg = Twist()

rate = rospy.Rate(10)

distance_tolerance = 1

pose = LaserScan()	
for i in range(18):
	pose.ranges.append(0.001)

  
if __name__ == '__main__':
	try:
		while not rospy.is_shutdown():
			move()
	except rospy.ROSInterruptException: pass
