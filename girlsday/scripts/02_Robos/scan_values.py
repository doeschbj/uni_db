import rospy
import turtle
import math
import threading
import numpy as np
from sensor_msgs.msg import LaserScan

lock = threading.Lock()
pos = np.empty(360 , dtype=float)
maxi = 10
mini = 0

def callback(msg):
	global pos
	global lock
	global mini
	global maxi
	while not lock.acquire():
		pass
	try:
		pos = np.empty(360 , dtype=float)
		pos = msg.ranges
		maxi = msg.range_max
		mini = msg.range_min
	finally:
		lock.release()

def main():
	global pos
	global lock
	global mini
	global maxi
	t = turtle.Pen()
	t.ht()
	t.speed(0)
	t.tracer(8, 0)
	t.circle(10)
	t.up()
	rospy.init_node('scan_values')
	sub = rospy.Subscriber('/robot3/scan',LaserScan,callback)
	while not rospy.is_shutdown():
		while not lock.acquire():
			pass
		try:		
			for i in range(360):
				if pos[i] > mini and pos[i] < maxi:
						x = int(-(math.sin(i * math.pi/180) * pos[i]) * 120)
						y = int((math.cos(i*math.pi/180) * pos[i]) * 120)
						t.goto(x, y)
						t.down()
						t.circle(2)
						t.up()	
		finally:
			lock.release()
			t.clear()
			t.goto(0,0)
			t.down()
			t.circle(10)
			t.up()	
		

if __name__ == '__main__':
	main()
