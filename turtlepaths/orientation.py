#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose 
import math 
import time
from rotate import rotate 

def setDesiredOrientation(publisher, speed_in_deg, desired_angle_deg):
    relative_angle_radians = math.radians(desired_angle_deg) - yaw
    clockwise = 0
    if relative_angle_radians < 0:
        clockwise =1
    else:
        clockwise = 0;
    print("relative angle radians:",math.degrees(relative_angle_radians))
    print("desired angle degree:",desired_angle_deg)
    rotate(publisher, speed_in_deg, math.degrees(abs(relative_angle_radians)), clockwise)
def poseCallback(pose_message):
    global x
    global y, yaw  #yaw is used to store the current desired location 
    x = pose_message.x
    y = pose_message.y
    yaw = pose_message.theta

if __name__ == '__main__':
    rospy.init_node('turtlesim_rotate', anonymous=True)

    cmd_vel_topic = '/turtle1/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size= 10)

    position_topic = '/turtle1/pose'
    pose_subscriber = rospy.Subscriber(position_topic, Pose, poseCallback)
    time.sleep(2)
    setDesiredOrientation(velocity_publisher, 30, 45)

    # !IMPORTANT
    ''' the difference between rotate and desired orientation is, in desired orientation the robot is fixed to rotate to a desired angle'''