#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2
import numpy as np
import math

x = 0.0
y = 0.0 
theta = 0.0

def newOdom(msg):
    global x
    global y
    global theta

    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

    rot_q = msg.pose.pose.orientation
    (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])
    print("theta",theta)


def move_circle(): 
    rospy.init_node("speed_controller",anonymous=True)


    sub = rospy.Subscriber("/odom", Odometry, newOdom)
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)

    speed = Twist()

    r = rospy.Rate(4)

    goal = Point()

    for i in np.arange(0,(3*math.pi)+0.4,0.1):
        goal.x = -i
        goal.y = math.sin(2*-i)*math.sin(-i/2)*math.exp(-0.01)

        while ((x-goal.x) > 0.1):
            inc_x = goal.x -x
            inc_y = goal.y -y

            angle_to_goal = atan2(inc_y, inc_x)
            print("angel",angle_to_goal)

            if (angle_to_goal - theta) > 0.1:
                speed.linear.x = 0.0
                speed.angular.z = 0.3
            elif(theta - angle_to_goal) > 0.1:
                speed.linear.x = 0.0
                speed.angular.z = -0.3
            else:
                speed.linear.x = 0.3
                speed.angular.z = 0.0

            pub.publish(speed)
            r.sleep()

        speed.linear.x = 0.0
        speed.angular.z = 0.0
        pub.publish(speed)

if __name__ == '__main__':
    try:
        move_circle()
    except rospy.ROSInterruptException:
        pass