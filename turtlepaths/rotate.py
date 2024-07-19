#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose 
import math 
import time

def rotate (velocity_publisher, angular_speed_deg, relative_angle, clockwise):   #in degrees
    velocity_message = Twist()                        #creating the message in Twist type
    angular_speed = math.radians(abs(angular_speed_deg))  #converting the angle to radians

    if (clockwise):             #clockwise is boolean function 
        velocity_message.angular.z = -abs(angular_speed)
    else:
        velocity_message.angular.z = abs(angular_speed)
    loop_rate = rospy.Rate(10) #message frq 10Hz
    t0 = rospy.Time.now().to_sec()  #instance before starting the motion

    while not rospy.is_shutdown():
        rospy.loginfo("I am rotating")
        velocity_publisher.publish(velocity_message)

        t1 = rospy.Time.now().to_sec()                 #in the move function we calculated the distance, in the rotation we can calculate the angle 
        current_angle = (t1 - t0)*angular_speed_deg  
        loop_rate.sleep()

        if (current_angle>relative_angle):
            print("I am done")
            break
    velocity_message.angular.z = 0
    velocity_publisher.publish(velocity_message)


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

    rotate(velocity_publisher, 30, 90, True)