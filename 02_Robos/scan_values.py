import rospy
import turtle
import math
from sensor_msgs.msg import LaserScan
t = turtle.Pen()

def callback(msg):
	global t
	for i in range(360):
		x = (math.sin(i) * msg.ranges[i]) * 120.0
		y = (math.cos(i) * msg.ranges[i]) * 120.0
		t.goto(x,y)
		t.down()
		t.circle(2)
		t.up()
		
def main():
	global t
	t.ht()
	t.speed(0)
	t.tracer(8, 0)
	t.up()
	rospy.init_node('scan_values')
	sub = rospy.Subscriber('/robot3/scan',LaserScan,callback)
	rospy.spin()

if __name__ == '__main__':
	main()
