import rospy
from sensor_msgs.msg import LaserScan

def callback(msg):
	i = 0
	while i < 360:
		
		print("Values at ")
		print(i)	
		print msg.ranges[i]
		print("--------------------")
		i = i + 10

rospy.init_node('scan_values')
sub = rospy.Subscriber('/robot3/scan',LaserScan,callback)
rospy.spin() 
