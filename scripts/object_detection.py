#!/usr/bin/env python

import time
import rospy
from std_msgs.msg import String
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import cv2
import numpy as np
import os
import csv
from classifier.yolo import YOLO
import rospkg
import yaml
from cv_bridge import CvBridge


class ObjectDetection:
	yolo = None
	config = None
        bridge = None

	def __init__(self):

		rospy.init_node('object_detection_node')

		rospack = rospkg.RosPack()
		path = rospack.get_path('object_detection')

		#Load config	
		object_detection_config = rospy.get_param("/object_detection_config")
		self.config = yaml.load(object_detection_config)

		self.yolo = YOLO(path+self.config['classification']['model'], path+self.config['classification']['anchors'], path+self.config['classification']['classes'])
		self.bridge = CvBridge()
        	
		#change the camera topic if it is different
		rospy.Subscriber('/camera/color/image_raw', Image, self.classify)
        	rospy.spin()


	
	def classify(self, image):
		img = self.bridge.imgmsg_to_cv2(image, "bgr8")
		img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) 
		scores, classes, img_ret = self.yolo.detect_image(img)
		print(classes)
		


if __name__ == '__main__':
    try:
        ObjectDetection()
    except rospy.ROSInterruptException:
	rospy.logerr('Could not start object detection node.')

