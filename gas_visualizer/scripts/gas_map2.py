#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import rospy
from geometry_msgs.msg import Point32, Point, PoseWithCovarianceStamped, Pose, Vector3, Quaternion,Twist
from nav_msgs.msg import Odometry
import statistics



global posx, posy, posz, s1tvoc,s1co2,s2tvoc,s2co2,s3tvoc,s3co2,tvoc,co2

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
max_co2=1000
max_tvoc=2500

rosRate=5

size_map=1000
size_square=20
const=100

#Matriz para graficar co2
z1=np.zeros(shape=(size_map,size_map))
#Matriz para almacenar datos co2
z1_end=np.zeros(shape=(size_map,size_map))
#Matriz para graficar tvoc
z2=np.zeros(shape=(size_map,size_map))
#Matriz para almacenar datos tvoc
z2_end=np.zeros(shape=(size_map,size_map))
		
class gasmap(object):
	global posx, posy, posz, tvoc,co2,h2,ethanol
	
	def __init__ (self):
		x = np.linspace(0, 2, 10)
		y = np.linspace(0, 2, 10)
	#Matriz para graficar co2
		z1=np.zeros(shape=(size_map,size_map))
	#Matriz para almacenar datos co2
		z1_end=np.zeros(shape=(size_map,size_map))
	#Matriz para graficar tvoc
		z2=np.zeros(shape=(size_map,size_map))
	#Matriz para almacenar datos tvoc
		z2_end=np.zeros(shape=(size_map,size_map))
		
		rate=rospy.Rate(rosRate)
		
		
	def listener(self):
		rospy.Subscriber("/odom",Odometry,self.callback)
		#rospy.Subscriber("/robot_a/amcl_pose",PoseWithCovarianceStamped,self.callback)
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
	
	def event2(self, msg):
		global s2tvoc,s2co2
		s2tvoc=msg.linear.x
		s2co2=msg.linear.y
		
	def event3(self, msg):
		global s3tvoc,s3co2
		s3tvoc=msg.linear.x
		s3co2=msg.linear.y 
 
	def f1(self, x, y):
		global s1co2, posx, posy
		z1[1,1]=max_co2	
		for i in range((int(posx*const)+(size_map/2))-size_square/2,(int(posx*const)+(size_map/2))+size_square/2):
			for j in range((int(posy*const)+(size_map/2))-size_square/2,(int(posy*const)+(size_map/2))+size_square/2):		
				z1[i,j] =s1co2
				z1_end[i,j] =s1co2
		return z1
    	
	def f2(self, x, y):
		global s1tvoc, posx, posy
		z2[1,1]=max_tvoc
		for i in range((int(posx*const)+(size_map/2))-size_square/2,(int(posx*const)+(size_map/2))+size_square/2):
			for j in range((int(posy*const)+(size_map/2))-size_square/2,(int(posy*const)+(size_map/2))+size_square/2):	
				z2[i,j] =s1tvoc
				z2_end[i,j] =s1tvoc
		return z2

	def updatefig1(self,*args):
		global x, y, s1tvoc,s1co2, posx, posy
		x= posx
		y= posy
		im1.set_array(self.f1(x,y))
		im2.set_array(self.f2(x,y))
		return im1, im2,
    	
	def start(self):
		while not rospy.is_shutdown():
			global posx, posy, posz
			self.listener()
			ani1 = animation.FuncAnimation(fig1, self.updatefig1, interval=50, blit=True)
			ani2 = animation.FuncAnimation(fig2, self.updatefig1, interval=50, blit=True)
			plt.show()
			rate.sleep()
    	
def mapFromTo(x,a,b,c,d):
	y=(x-a)/(b-a)*(d-c)+c
	return y

if __name__ == '__main__':
	global posx, posy, posz
	rospy.init_node('graphic_node',anonymous=True)
	gasmap1=gasmap()
	
	x=0
	y=0
	fig1 = plt.figure()
	im1 = plt.imshow(gasmap1.f1(x,y), animated=True)
	fig1.suptitle('Grafica de CO2 (400-60000 ppm)', fontsize=16)
	fig1.colorbar(im1)
	
	fig2 = plt.figure()
	im2 = plt.imshow(gasmap1.f2(x,y), animated=True)
	fig2.suptitle('Grafica de TVOC (0 - 60000 ppb)', fontsize=16)
	fig2.colorbar(im2)
	
	try:
		gasmap1.start()	
	except rospy.ROSInterruptException:
        	pass

 


