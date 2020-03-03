import sys, os, time
sys.path.insert(0, "~/catkin_ws/src/uni_db/02_Robos/pixy_api/")
import rospy
import math
from ctypes import *
from std_msgs.msg import Float64
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32MultiArray
from threading import Thread
from pixy_api import pixy
from pixy_api.pixy import *

data_pub = rospy.Publisher('/dataSensor',Int32MultiArray,queue_size = 10)
speed_pub = rospy.Publisher('/robot3/cmd_vel',Twist,queue_size = 10)

rospy.init_node('robot1talker', anonymous=True)
msg = Twist()
rate = rospy.Rate(60) # 20hzgle_lamp()
yspeed = 0
zspeed = 0
xturnspeed = 0
yturnspeed = 0
run = 0
def f_callback(data):
	global run
	print data.data
	thread = Thread(target=f_getBlocks)	
	thread.daemon = True
	if data.data =="go":
		run = 1
		thread.start()
	elif data.data =="stop":
		f_stop()
		run = 0
	elif data.data == "lamp":
		toggle_lampon()
	elif data.data =="ende":
		f_stop()
		run = 0

rospy.Subscriber('/info',String,f_callback)		


def f_main():
	f_init()
	rospy.spin()

def f_init():
	print("Blocks started")
	pixy.init ()
	pixy.change_prog ("color_connected_components")
	
	print("Initialized")
	
def f_getBlocks():
	global run
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
	while run == 1:	
		count = pixy.ccc_get_blocks (100, blocks)
		if count > 0:
			arr = []
			arr.append(blocks[0].m_signature)
			arr.append(blocks[0].m_width)
			arr.append(blocks[0].m_height)
			arr.append(blocks[0].m_x)
			arr.append(blocks[0].m_y)
			arr_pub = Int32MultiArray(data=arr)
			print(str(arr[0]) + " erkannt")
			f_publish(arr_pub)
			rate.sleep()
		else:	
			arr = []
			arr.append(0)
			arr_pub = Int32MultiArray(data=arr)
			f_publish(arr_pub)
			rate.sleep()	
			print("Nichts erkannt")
	print("ende")


def f_stop():
	f_publishSpeed(0,0)
	rate.sleep()
def toggle_lampon():
	#pixy.toggle_lamp()  nachschauen wie es heißt
	pass

def f_publish(data):
	data_pub.publish(data)

def f_publishSpeed(xspeed, zturnspeed):
	msg.linear.x = xspeed
	msg.linear.y = yspeed
	msg.linear.z = zspeed
	msg.angular.z = zturnspeed
	msg.angular.y = yturnspeed
	msg.angular.x = xturnspeed
	speed_pub.publish(msg)

if __name__ == '__main__':
	try:
		f_main()
	except rospy.ROSInterruptException:
		pass

