#!/usr/bin/env python
"""ROS node that performs Visualization of Gas Information in RViz of ARTUR nose"""

import rospy
from geometry_msgs.msg import Point32, Point, PoseWithCovarianceStamped, Pose, Vector3, Quaternion,Twist
from visualization_msgs.msg import Marker
from std_msgs.msg import Header, ColorRGBA, String
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import statistics

global posx, posy, posz, tvoc,co2,h2,ethanol
posx=0
posy=0
posz=0
s1tvoc=0
s2tvoc=0
s3tvoc=0
tvoc=0

co2=0
s1co2=0
s2co2=0
s3co2=0

h2=0
ethanol=0

size_anchor=0.2



class MarkerBasics(object):
	global posx, posy, posz, tvoc,co2,h2,ethanol
	
	def __init__ (self):
		self.count=0
		self.count2=0
		
		self.marker_publisher1=rospy.Publisher('marker_s1co2', Marker, queue_size=5)
		self.marker_publisher2=rospy.Publisher('marker_s1tvoc', Marker, queue_size=5)
		self.marker_publisher3=rospy.Publisher('marker_s2co2', Marker, queue_size=5)
		self.marker_publisher4=rospy.Publisher('marker_s2tvoc', Marker, queue_size=5)
		self.marker_publisher5=rospy.Publisher('marker_s3co2', Marker, queue_size=5)
		self.marker_publisher6=rospy.Publisher('marker_s3tvoc', Marker, queue_size=5)
		#Publisher de las medias
		self.marker_publisher7=rospy.Publisher('marker_co2', Marker, queue_size=5)
		self.marker_publisher8=rospy.Publisher('marker_tvoc', Marker, queue_size=5)
		
		self.rate=rospy.Rate(1)
		
		#configuracion de grafico de matplotlib
		#coord=np.arange(-5,5,0.01)
		#x,y=np.meshgrid(coord,coord, indexing= "ij")
		z=np.zeros(shape=(1000,1000))
		for i in range(400,600):
			for j in range(400,600):
				z[i,j] = 50
				
		for i in range(100,200):
			for j in range(100,200):
				z[i,j] = 150
				
		for i in range(500,700):
			for j in range(500,700):
				if z[i,j]!=0:
					z[i,j] = statistics.mean([z[i,j],90])
				else:
					z[i,j]=90
		
		plt.figure(figsize=(8,6))
		plt.imshow(z,cmap="summer")
		plt.colorbar()
		plt.show()
		
		#figura con update
		
	def rviz_vis(self):
		global posx, posy, posz, s1tvoc,s1co2, s2tvoc,s2co2, s3tvoc,s3co2 
		
		#Meshgrid para mostrar grafico
		
		s1tvoc_range=(1-mapFromTo(s1tvoc,40,500,0,1))
		s1co2_range=(1-mapFromTo(s1co2,400,3000,0,1))
		
		s2tvoc_range=(1-mapFromTo(s2tvoc,40,500,0,1))
		s2co2_range=(1-mapFromTo(s2co2,400,3000,0,1))
		
		s3tvoc_range=(1-mapFromTo(s3tvoc,40,500,0,1))
		s3co2_range=(1-mapFromTo(s3co2,400,3000,0,1))
		
		lifetime_marker=2400
		
		#Marker de s1co2
		self.markers1co2=Marker()
		self.markers1co2=Marker(
			type=Marker.SPHERE,
			id=0,
			lifetime=rospy.Duration(lifetime_marker),
			pose=Pose(Point(posx,posy,posz),Quaternion(0, 0, 0, 1)),
			scale=Vector3(size_anchor,size_anchor,size_anchor),
			#header=Header(frame_id='base_link'),
			header=Header(frame_id='robot_a_map'),
			color=ColorRGBA(1.0,s1co2_range,1.0, 1))
		
		self.count=self.count+1
		self.markers1co2.id=self.count
		self.marker_publisher1.publish(self.markers1co2)
		
		
		#Marker de s2co2
		self.markers2co2=Marker()
		self.markers2co2=Marker(
			type=Marker.SPHERE,
			id=0,
			lifetime=rospy.Duration(lifetime_marker),
			pose=Pose(Point(posx,posy,posz),Quaternion(0, 0, 0, 1)),
			scale=Vector3(size_anchor,size_anchor,size_anchor),
			#header=Header(frame_id='base_link'),
			header=Header(frame_id='robot_a_map'),
			color=ColorRGBA(1.0,s2co2_range,1.0, 1))
		self.markers2co2.id=self.count
		self.marker_publisher3.publish(self.markers2co2)
		
		#Marker de s3co2
		self.markers3co2=Marker()
		self.markers3co2=Marker(
			type=Marker.SPHERE,
			id=0,
			lifetime=rospy.Duration(lifetime_marker),
			pose=Pose(Point(posx,posy,posz),Quaternion(0, 0, 0, 1)),
			scale=Vector3(size_anchor,size_anchor,size_anchor),
			#header=Header(frame_id='base_link'),
			header=Header(frame_id='robot_a_map'),
			color=ColorRGBA(1.0,s3co2_range,1.0, 1))
		self.markers2co2.id=self.count
		self.marker_publisher5.publish(self.markers3co2)
				
		#Marker de s1tvoc
		self.markers1tvoc=Marker()
		self.markers1tvoc=Marker(
			type=Marker.SPHERE,
			id=0,
			lifetime=rospy.Duration(lifetime_marker),
			pose=Pose(Point(posx,posy,posz),Quaternion(0, 0, 0, 1)),
			scale=Vector3(size_anchor,size_anchor,size_anchor),
			#header=Header(frame_id='base_link'),
			header=Header(frame_id='robot_a_map'),
			color=ColorRGBA(1.0,1.0,s1tvoc_range, 1))
		self.markers1tvoc.id=self.count
		self.marker_publisher2.publish(self.markers1tvoc)
		
		#Marker de s2tvoc
		self.markers2tvoc=Marker()
		self.markers2tvoc=Marker(
			type=Marker.SPHERE,
			id=0,
			lifetime=rospy.Duration(lifetime_marker),
			pose=Pose(Point(posx,posy,posz),Quaternion(0, 0, 0, 1)),
			scale=Vector3(size_anchor,size_anchor,size_anchor),
			#header=Header(frame_id='base_link'),
			header=Header(frame_id='robot_a_map'),
			color=ColorRGBA(1.0,1.0,s1tvoc_range, 1))
		self.markers2tvoc.id=self.count
		self.marker_publisher4.publish(self.markers2tvoc)
		
		#Marker de s3tvoc
		self.markers3tvoc=Marker()
		self.markers3tvoc=Marker(
			type=Marker.SPHERE,
			id=0,
			lifetime=rospy.Duration(lifetime_marker),
			pose=Pose(Point(posx,posy,posz),Quaternion(0, 0, 0, 1)),
			scale=Vector3(size_anchor,size_anchor,size_anchor),
			#header=Header(frame_id='base_link'),
			header=Header(frame_id='robot_a_map'),
			color=ColorRGBA(1.0,1.0,s1tvoc_range, 1))
		self.markers3tvoc.id=self.count
		self.marker_publisher6.publish(self.markers3tvoc)
	
	
		co2=(s1co2+s2co2+s2co2)/3
		co2_range=(1-mapFromTo(co2,400,3000,0,1))
		
		
		#Marker de media co2
		self.markerco2=Marker()
		self.markerco2=Marker(
			type=Marker.SPHERE,
			id=0,
			lifetime=rospy.Duration(lifetime_marker),
			pose=Pose(Point(posx,posy,posz),Quaternion(0, 0, 0, 1)),
			scale=Vector3(size_anchor,size_anchor,size_anchor),
			#header=Header(frame_id='base_link'),
			header=Header(frame_id='robot_a_map'),
			color=ColorRGBA(1.0,co2_range,1.0, 1))
		self.markerco2.id=self.count
		self.marker_publisher7.publish(self.markerco2)
		
		
		tvoc=(s1tvoc+s2tvoc+s2tvoc)/3
		tvoc_range=(1-mapFromTo(tvoc,40,500,0,1))
		
		#Marker de media tvoc
		self.markertvoc=Marker()
		self.markertvoc=Marker(
			type=Marker.SPHERE,
			id=0,
			lifetime=rospy.Duration(lifetime_marker),
			pose=Pose(Point(posx,posy,posz),Quaternion(0, 0, 0, 1)),
			scale=Vector3(size_anchor,size_anchor,size_anchor),
			#header=Header(frame_id='base_link'),
			header=Header(frame_id='robot_a_map'),
			color=ColorRGBA(1.0,1.0,s1tvoc_range, 1))
		self.markertvoc.id=self.count
		self.marker_publisher8.publish(self.markertvoc)
		
	
	def start(self):
		while not rospy.is_shutdown():
			global posx, posy, posz, tvoc,co2,h2,ethanol
			co2_last=co2
			posx_last=posx
			posy_last=posy
			self.listener()
			if (abs(co2-co2_last)<10):
				self.count2=self.count2+1
			if (abs(posx-posx_last)>0.1):
				self.count2=0
			if (self.count2>10):
				self.rviz_vis()
				self.count2=0
			self.rate.sleep()
	
	def listener(self):
		global posx, posy, posz, tvoc,co2,h2,ethanol
		#Subscriber para usar con unitree		
		#rospy.Subscriber("/odom",PoseWithCovarianceStamped,self.callback)
		#Subscriber para usar con simulador
		rospy.Subscriber("/robot_a/amcl_pose",PoseWithCovarianceStamped,self.callback)
		rospy.Subscriber("/gas_1",Twist,self.event1)
		rospy.Subscriber("/gas_2",Twist,self.event2)
		rospy.Subscriber("/gas_3",Twist,self.event3)
    
	def callback(self,msg):	
		global posx, posy, posz
		posx=msg.pose.pose.position.x
		posy=msg.pose.pose.position.y
		posz=msg.pose.pose.position.z
		
	def event1(self,msg):
		global s1tvoc,s1co2
		s1tvoc=msg.linear.x
		s1co2=msg.linear.y
	
	def event2(self,msg):
		global s2tvoc,s2co2
		s2tvoc=msg.linear.x
		s2co2=msg.linear.y
		
	def event3(self,msg):
		global s3tvoc,s3co2
		s3tvoc=msg.linear.x
		s3co2=msg.linear.y
		
#funciones para graficar	

			
		
def mapFromTo(x,a,b,c,d):
   y=(x-a)/(b-a)*(d-c)+c
   return y
   
if __name__ == '__main__':
    global posx, posy, posz
    rospy.init_node('marker_basic_node',anonymous=True)
    markerbasics_object=MarkerBasics()
    
    try:
		markerbasics_object.start()
		
    except rospy.ROSInterruptException:
        pass
