#! /usr/bin/env python
import os
import pprint
import pygame
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Point
from train import Trainer

class ModeManager(object):
	""" ** Mode Manager Node **
	"""
	def __init__(self):
		# Initialize joystick receiver using pygame
		pygame.init()
		pygame.joystick.init()
		self.controller = None
		while self.controller is None:
			try:
				self.controller = pygame.joystick.Joystick(0)
			except:
				pass
		self.controller.init()

		# Initialize ROS Publisher
		self.mode = None
		self.mode_pub = rospy.Publisher('mode', String, queue_size=10)
		self.cmd_pub  = rospy.Publisher('cmd', Point, queue_size=1)
		rospy.init_node('controller', anonymous=True)

		# Initialize Keras model Trainer
		self.trainer = Trainer()

	# Listen for PS4 Controller inputs
	def listen(self):
		# Mode management
		while not rospy.is_shutdown():
			for event in pygame.event.get():
				if event.type == pygame.JOYBUTTONDOWN:
					if(event.button==1 and self.mode!='manual'):
						self.cmd_pub.publish(Point(0.0,0.0, 0.0))
						rospy.loginfo("Switching to manual...")
						self.mode_pub.publish("manual")
						self.mode = 'manual'
					elif(event.button==3 and self.mode!='auto'):
						# Stop the cars motors
						self.cmd_pub.publish(Point(0.0,0.0, 0.0))
						rospy.loginfo("Switching to auto...")
						self.mode_pub.publish("auto")
						self.mode = 'auto'
					elif(event.button==4): # L1
						# Stop the cars motors and reset s
						self.cmd_pub.publish(Point(0.0,0.0, 0.0))
						rospy.loginfo("Training model...")
						self.mode_pub.publish("none")
						self.trainer.train()

if __name__ == "__main__":
    mm = ModeManager()
    mm.listen()
