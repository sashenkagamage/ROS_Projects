#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose 
import math 
import time


def spiral(velocity_publisher, rk, wk): #
    global x
    global y, yaw
    velocity_message = Twist()
    loop_rate = rospy.Rate(1)

    while not rospy.is_shutdown():

        rk = rk+1  #linear velocity is a function of time; rk will be incremented everytime 
        #but the angular velocity will be constant
        velocity_message.linear.x= rk
        velocity_message.linear.y = 0
        velocity_message.linear.z = 0
        velocity_message.angular.x = 0
        velocity_message.angular.y = 0
        velocity_message.angular.z = wk
        velocity_publisher.publish(velocity_message)
        loop_rate.sleep()
    velocity_message.linear.x = 0
    velocity_message.angular.z = 0
    velocity_publisher.publish(velocity_message)

def poseCallback(pose_message):
    global x
    global y, yaw
    x = pose_message.x
    y = pose_message.y
    yaw = pose_message.theta

if __name__ == '__main__':
    rospy.init_node('turtlesim_motion_pose', anonymous=True)

    cmd_vel_topic = '/turtle1/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size= 10)

    position_topic = '/turtle1/pose'
    pose_subscriber = rospy.Subscriber(position_topic, Pose, poseCallback)
    time.sleep(2)


    spiral(velocity_publisher, 0, 4)