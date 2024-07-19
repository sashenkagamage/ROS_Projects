#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose 
import math 
import time

def move(velocity_publisher, speed, distance, is_forward):
    velocity_message = Twist()   #declare a message in Twist type

    global x, y   #declare global variables for the current location
    x0 = x
    y0 = y

    if (is_forward): #is_forward is a boolean expression and will move forward when it is True 
        velocity_message.linear.x = abs(speed)
    else:
        velocity_message.linear.x = -abs(speed) # - sign means move backwards 

    distance_moved = 0.0
    loop_rate = rospy.Rate(10) #publish the velocity at 10Hz

    while not rospy.is_shutdown():
        rospy.loginfo("Turtlesim moves forward")
        velocity_publisher.publish(velocity_message)
        loop_rate.sleep()
        distance_moved = abs(math.sqrt(((x-x0)**2) +((y-y0)**2)))
        print(distance_moved)
        if (distance_moved>distance):
            rospy.loginfo("Reached")
            break
    velocity_message.linear.x = 0  #DON'T FORGET THIS STEP
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


    move(velocity_publisher, 10.0, 4.0, True)


