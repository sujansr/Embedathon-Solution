#!/usr/bin/env python

import rospyanonymous=True
from geometry_msgs.msg import Twist

def move_circle(): 
    rospy.init_node('node_turtle_revolve',)
    # Create a publisher which can "talk" to Turtlesim and tell it to move
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

    # Create a Twist message and add linear x and angular z values
    move_cmd = Twist()
    move_cmd.linear.x = 0.40
    move_cmd.angular.z = -0.40/3.5

    # Save current time and set publish rate at 10 Hz
    now = rospy.Time.now()
    rate = rospy.Rate(10)
    
    # For the next 6 seconds publish cmd_vel move commands to Turtlesim
    while not rospy.is_shutdown():
        pub.publish(move_cmd)
        rate.sleep()


if __name__ == '__main__':
    try:
        move_circle()
    except rospy.ROSInterruptException:
        pass
