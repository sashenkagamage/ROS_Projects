#!/usr/bin/env python
import rospy 
from ros_test.msg import Sensor
import random

#create a new publisher. we specify the topic name, then type of message then the queue size
sensor_pub = rospy.Publisher('iot_sensor_topic', Sensor, queue_size=10)


#we need to initialize the node
rospy.init_node('iot_node_pub', anonymous=True)

#set the loop rate
rate = rospy.Rate(1) # 1hz
#keep publishing until a Ctrl-C is pressed
i = 0
while not rospy.is_shutdown():
    iot_sensor = Sensor()
    iot_sensor.id = 1
    iot_sensor.name = "go_park"
    iot_sensor.temperature = 24.33 + (random.random()*2)
    iot_sensor.humidity = 33.41+ (random.random()*2)
    rospy.loginfo("I measured:")
    rospy.loginfo(iot_sensor)
    sensor_pub.publish(iot_sensor)
    rate.sleep()
    i=i+1
