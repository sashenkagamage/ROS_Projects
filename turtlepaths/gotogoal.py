#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose 
import math 
import time

def go_to_goal(velocity_publisher, x_goal, y_goal):
    global x
    global y, yaw

    velocity_message = Twist()

    while not rospy.is_shutdown():
         K_linear = 0.5 #constant; if the gain is very high the controller starts oscilating and it's not appropriate 
         distance = abs(math.sqrt(((x_goal - x)**2) +((y_goal-y)**2)))  #euclidian distance 
         linear_speed = distance * K_linear #the linear_speed is propotional to the distance; this is a P-Controller #P of the PID Controller
        
         K_angular = 4.0 #another constant
         desired_angle_goal = math.atan2(y_goal-y, x_goal-x) #mathematically atan2 give angle between two vectors 
         #creating a  propotional controller for the angle to rotate 
         angular_speed = (desired_angle_goal-yaw)*K_angular

         velocity_message.linear.x = linear_speed
         velocity_message.angular.z = angular_speed

         velocity_publisher.publish(velocity_message)
         print('x =', x, 'y =', y, 'distance to goal:', distance)

         if distance < 0.01:
              break 
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


    go_to_goal(velocity_publisher, 7, 3)
