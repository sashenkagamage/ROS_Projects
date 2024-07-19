#!/usr/bin/env python
import rospy 
from ros_test.msg import Sensor

def sensor_callback(sensor):
    rospy.loginfo("new IoT data received: (%d, %s, %.2f ,%.2f)", 
        sensor.id,sensor.name,
        sensor.temperature,sensor.humidity)
  

rospy.init_node('iot_sesnor_sub', anonymous=True)
rospy.Subscriber('iot_sensor_topic', Sensor, sensor_callback)

rospy.spin()