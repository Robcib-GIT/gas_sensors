#!/usr/bin/env python
"""ROS node that performs Visualization of Gas Information in RViz of ARTUR nose"""

import rospy
from geometry_msgs.msg import Point32, Point, PoseWithCovarianceStamped, Pose, Vector3, Quaternion,Twist, PoseStamped
from visualization_msgs.msg import Marker
from nav_msgs.msg import Odometry
from std_msgs.msg import Header, ColorRGBA, String, Bool
import statistics

global posx, posy, tvoc,co2,h2,ethanol
posx=0
posy=0
posz=0

size_anchor=0.4

rosRate=5
z=Bool()

class MarkerVictim(object):
	global posx, posy, posz, tvoc,co2,h2,ethanol
	
	def __init__ (self):
		self.count=0
		
		self.marker_publisher1=rospy.Publisher('marker_victima', Marker, queue_size=5)
		self.p1=rospy.Publisher('/start',Bool,queue_size=1)
		
		self.rate=rospy.Rate(rosRate)
	
	def rviz_vis(self):
		global posx, posy, posz
		
		lifetime_marker=50000
			
		self.markervictim=Marker()
		self.markervictim=Marker(
			type=Marker.CUBE,
			id=0,
			lifetime=rospy.Duration(lifetime_marker),
			pose=Pose(Point(0,0,posz),Quaternion(0, 0, 0, 1)),
			scale=Vector3(size_anchor,size_anchor,size_anchor),
			header=Header(frame_id='base_link'),
			color=ColorRGBA(0.0,0.0,1.0, 1))
		
		self.count=self.count+1
		self.markervictim.id=self.count
		self.marker_publisher1.publish(self.markervictim)
		
	def start(self):
		while not rospy.is_shutdown():
			global posx, posy, posz
			self.listener()
			self.rate.sleep()
			rospy.spin()
	
	def listener(self):
		global posx, posy, posz
		rospy.Subscriber("/ventilador",PoseStamped,self.callback_venti)
		rospy.Subscriber("/victima",PoseStamped,self.callback_victima)
		rospy.Subscriber("/odom",Odometry,self.callback_pose)
    
	def callback_venti(self,msg):	
		venti=msg.pose.position.x
		if (venti==1):
			z.data=True
			self.p1.publish(z)
			rospy.loginfo("Ventilador ON")
		if (venti==0):
			z.data=False
			self.p1.publish(z)
			rospy.loginfo("Ventilador OFF")
				
	def callback_victima(self,msg):
		victim=msg.pose.position.x
		#rospy.loginfo(victim)
		if (victim==1):
				self.rviz_vis()
				rospy.loginfo("Victima found")
				
	def callback_pose(self,msg):
		global posx, posy, posz
		posx=msg.pose.pose.position.x
		posy=msg.pose.pose.position.y
		posz=msg.pose.pose.position.z		
	
if __name__ == '__main__':
    rospy.init_node('marker_victim_node',anonymous=True)
    marker_victim=MarkerVictim()
    
    try:
		marker_victim.start()
		
    except rospy.ROSInterruptException:
        pass
