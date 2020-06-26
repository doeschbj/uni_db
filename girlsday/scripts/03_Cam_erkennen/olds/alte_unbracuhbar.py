#Master und Slave beides auf dem turtlebot während der entwicklung umgelagert auf zwei verteilte systeme
import sys, os, time
import pixy_api/pixy 
import rospy
import math
from ctypes import *
from pixy import *
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32

vel_pub = rospy.Publisher('/dataSensor',Int32,queue_size = 10)
msg = Twist()
rospy.init_node('talker', anonymous=True)
rate = rospy.Rate(40) # 10hz
pi = math.pi

yspeed = 0
zspeed = 0
xturnspeed = 0
yturnspeed = 0
max = 0.06

def f_main():
	f_achtfahren()

def f_achtfahren():
	speed = 0.2
	f_publish(speed,0)
	rospy.sleep(3)
	turnspeed = 1
	f_publish(speed,turnspeed)
	rospy.sleep(6)
	f_publish(speed,0)
	rospy.sleep(3)
	f_publish(speed,turnspeed)
	rospy.sleep(6)
	f_publish(0,0)


def f_fahren(): 
	#f_turnRight(angle) rechtsdrehung
	#f_turnLeft(angle) linksdrehung 
	#angle legt winkel der drehung fest 
	#f_drive_cm(way_cm,drive_speed) faehrt cm nach vorne
	#way_cm anzahl cm die gefahren werden sollen
	#drive_speed Geschwindigkeit wobei: -0.5 < drive_speed < 0.5 ausser 0
	f_drive_cm(3,0.3)
	f_turnLeft(90)
	f_drive_cm(3,0.3)
	f_turnLeft(90)
	f_drive_cm(3,0.3)
	f_turnLeft(90)
	f_drive_cm(3,0.3)
	f_turnLeft(90)

def getBlocks():
	print ("Pixy2 Drive")
	speed = 0.005
	turnspeed = 0
	pixy.init ()
	pixy.change_prog ("color_connected_components");

	class Blocks (Structure):
	  _fields_ = [ ("m_signature", c_uint),
		("m_x", c_uint),
		("m_y", c_uint),
		("m_width", c_uint),
		("m_height", c_uint),
		("m_angle", c_uint),
		("m_index", c_uint),
		("m_age", c_uint) ]

	blocks = BlockArray(100)
	errordis = 0
	errorturn = 0
	factor = 0.00018
	factorturn = 0.007
	counter = 3
	while not rospy.is_shutdown():
	  	count = pixy.ccc_get_blocks (100, blocks)
		if count > 0:
			sig = blocks[0].m_signature # Farbe die erkannt wurde sig ist eins wenn erste farbe 			erkannte wurde usw
			if sig == 1:# gelb
				width = blocks[0].m_width
				height = blocks[0].m_height
				x = blocks[0].m_x
				counter = 0;
				if width > 60 :#and height > 55:
					errordis = 60 - width
					speed = speed + (errordis * factor)

				if width < 60 :#and height < 55:
					errordis = 60 - width
					speed = speed + (errordis * factor)

				if x > 190:
					errorturn = 160 - x
					turnspeed = turnspeed + (errorturn * factorturn)

				if x < 120 :
					errorturn = 155 - x
					turnspeed = turnspeed + (errorturn * factorturn)
			elif sig == 2: # andere Farbe
				sig = 99
			
		else:
			if counter == 3:
				turnspeed = 0
				speed = 0
			else: 
				counter = counter + 1
		
		if speed < -max: speed = -max
		if turnspeed < -max: turnspeed = -max
		if speed > max: speed = max;
		if turnspeed > max: turnspeed = max

		f_publish(speed,turnspeed)
		rate.sleep()

def f_publish(xspeed, zturnspeed):
	msg.linear.x = xspeed
	msg.linear.y = yspeed
	msg.linear.z = zspeed
	msg.angular.z = zturnspeed
	msg.angular.y = yturnspeed
	msg.angular.x = xturnspeed
	vel_pub.publish(msg)

def f_turnRight(angle):
	turnspeed = -0.5
	way = (angle * pi * 19)/ 360
	turntime = way/abs(turnspeed * 10) 
	f_publish(0,turnspeed)
	rospy.sleep(turntime)
	f_publish(0,0)

def f_turnLeft(angle):
	turnspeed = 0.5
	way = (angle * pi * 19)/ 360
	turntime = way/abs(turnspeed * 10) 
	f_publish(0,turnspeed)
	rospy.sleep(turntime)
	f_publish(0,0)

def f_drive_cm(way_cm, drive_speed):
	if drive_speed > 0.5:
		drive_speed = 0.5
	if drive_speed < -0.5:
		drive_speed = -0.5
	drive_time = way_cm/abs(drive_speed * 10) 
	f_publish(drive_speed,0)
	rospy.sleep(drive_time)
	f_publish(0,0)
	
f_main()
	
  
