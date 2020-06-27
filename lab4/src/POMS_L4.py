#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class Robot:

	distance_tolerance = 1
	dist_ang=0.0

	def __init__(self):
		rospy.init_node('Robot', anonymous= True)
		self.velocity_publisher =  rospy.Publisher('/cmd_vel', Twist, queue_size= 10)
		self.pose_subscriber =  rospy.Subscriber('/base_scan', LaserScan, self.scan_data)
		self.pose =  LaserScan()

		for i in range(18):
        		self.pose.ranges.append(0.001)
        	self.rate =  rospy.Rate(10)

	def scan_data( self, data):
		self.pose =  data
		right=min(self.pose.ranges[0:6])
		forward=min(self.pose.ranges[6:12])
		left=min(self.pose.ranges[12:18])
		self.pose.ranges = [right, forward, left]
		print(right, forward, left)

	
	def linear_vel(self, constant= 1.5):
		return constant *  self.pose.ranges[1]

	def angular_vel(self, dist_ang, constant=5):
		return dist_ang * constant


	def move_forward(self):	
		vel_msg = Twist()
		vel_msg.linear.x = 0
		vel_msg.linear.y = 0
		vel_msg.linear.z = 0
		vel_msg.angular.x = 0
		vel_msg.angular.y = 0
		vel_msg.angular.z = 0
			

		if self.pose.ranges[1] > self.distance_tolerance:
			vel_msg.linear.x = self.linear_vel()
			vel_msg.angular.z = 0
			self.velocity_publisher.publish(vel_msg)
		else:
			if self.pose.ranges[0] < self.pose.ranges[2]:
				dist_ang=self.pose.ranges[2]/self.pose.ranges[0]
				print("rotating right")
			else: 
				dist_ang=-self.pose.ranges[0]/self.pose.ranges[2]
				print("rotating left")

			vel_msg.linear.x = 0
			vel_msg.angular.z = self.angular_vel(dist_ang)
			

		self.velocity_publisher.publish(vel_msg)
		self.rate.sleep()
		return


 	def move(self):

		while not rospy.is_shutdown():
			self.move_forward()



if __name__ == '__main__':
    try:
	x = Robot()
	x.move()
    except rospy.ROSInterruptException:
        pass
