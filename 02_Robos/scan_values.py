import rospy
from sensor_msgs.msg import LaserScan

def callback(msg):
	print ("Values at 0 Grad")
	print msg.ranges[0]
	print ("Values at 90 Grad")
	print msg.ranges[89]
	print ("Values at 180 Grad")
	print msg.ranges[179]
	print ("Values at 360 Grad")
	print msg.ranges[359]
	print("--------------------")

rospy.init_node('scan_values')
sub = rospy.Subscriber('/robot1/scan',LaserScan,callback)
rospy.spin() 
