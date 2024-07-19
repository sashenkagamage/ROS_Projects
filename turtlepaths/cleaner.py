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

def gridClean(velocity_publisher):
    global x
    global y, yaw
    desired_pose = Pose()
    desired_pose.x = 1
    desired_pose.y = 1
    desired_pose.theta = 0

    go_to_goal(velocity_publisher, 1, 1)

    setDesiredOrientation(velocity_publisher, 30, math.radians(desired_pose.theta))

    for i in range(5):
        move(velocity_publisher, 2.0, 1.0, True)
        rotate(velocity_publisher, 20, 90, False)
        move(velocity_publisher, 2.0, 9.0, True)
        rotate(velocity_publisher, 10, 90, True)
        move(velocity_publisher, 2.0, 1.0, True)
        rotate(velocity_publisher, 20, 90, True)
        move(velocity_publisher, 2.0, 9.0, True)
        rotate(velocity_publisher, 20, 90, False)
    pass
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


    gridClean(velocity_publisher)

