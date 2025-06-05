#!/usr/bin/env python3

#  navigate autonomously to a specific point using move_base action


import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PoseStamped , Twist

class NavToPoint:

    def __init__(self, points):
        rospy.on_shutdown(self.cleanup)
        # Subscribe to the move_base action server
        self.move_base = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        rospy.loginfo("Waiting for move_base action server...")
        self.move_base.wait_for_server(rospy.Duration(120))
        rospy.loginfo("Connected to move base server")
        
        self.points = points
        self.goal = MoveBaseGoal()
        self.goal.target_pose.header.frame_id = 'map'
        self.goal.target_pose.pose.orientation.x = 0.0
        self.goal.target_pose.pose.orientation.y = 0.0
        self.goal.target_pose.pose.orientation.z = 0.0
        self.goal.target_pose.pose.orientation.w = 1.0  # quaternion orientation
        #sekf.mutex = 0
        rospy.loginfo("Ready to go")
        rospy.sleep(1)

    def goto(self):
        rospy.loginfo("Starting navigation test")

        for point in self.points:
            
            self.goal.target_pose.header.stamp = rospy.Time.now()
            self.goal.target_pose.pose.position.x = point[0]  # x position in meters
            self.goal.target_pose.pose.position.y = point[1]  # y position in meters

            self.move_base.send_goal(self.goal)

            # Wait for the robot to reach the goal
            wait = self.move_base.wait_for_result()

            if not wait:
                rospy.logerr("Action server not available!")
                rospy.signal_shutdown("Action server not available!")
            else:
                rospy.loginfo("Navigation result: %s" % self.move_base.get_result())

            # Perform an action here
            if point[0]!=0.008 and point[1]!=-0.014 :
                print("sleeping")
                print(point)
                rospy.sleep(2)
                self.perform_action()
            

    def perform_action(self):
        rospy.loginfo("Performing action")
        # Create a Twist message to set the linear velocity
        twist = Twist()
        twist.linear.x = 0.0854  # 0.0254 meters = 1 inch
        # Set the duration to move forward (adjust as needed)
        duration = rospy.Duration.from_sec(10.0)  # move for 5 seconds
        # Publish the twist message to move the robot
        self.cmd_vel_pub.publish(twist)
        rospy.sleep(duration.to_sec())
        # Stop the robot by publishing a zero Twist message
        twist.linear.x = 0.0
        self.cmd_vel_pub.publish(twist)
        rospy.loginfo("Action completed")
        rospy.sleep(5)

    def cleanup(self):
        rospy.loginfo("Shutting down navigation node...")
        self.move_base.cancel_goal()


if __name__ == '__main__':
    try:
        # Initialize the ROS node
        rospy.init_node('nav_to_point', anonymous=True)

        # Set the points to navigate to
        points = [[-0.181, 0.896],[0.138,-0.082],[-0.286,-0.819],[0.008,-0.014]]
        #x: -0.18146048398493622
        #y: 0.8964385286604148
        #x: 0.13804446290205538
        #y: -0.08295120717393693
        #x: -0.28622433701843203
        #y: -0.819892217401756
        #x: 0.008051020915027336
        #y:-0.014508889016552461


        ntp = NavToPoint(points)
        ntp.goto()
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test interrupted")

