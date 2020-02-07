#!/usr/bin/env python
import rospy
import sys, os, time
import math
from ctypes import *
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import String

vel_pub = rospy.Publisher('/robot3/cmd_vel',Twist,queue_size = 10)
info_pub = rospy.Publisher('/info',String,queue_size = 2)
msg = Twist()
rospy.init_node('mastertalker', anonymous=True)

rate = rospy.Rate(80)
count = 0
pi = math.pi
counter = 100
cmd = ""

def f_callback(data):
	global cmd
	if cmd == "start":
		getBlocks(data)
	elif cmd == "startkugel":
		f_kugel_find(data)

rospy.Subscriber('/dataSensor',Int32MultiArray,f_callback)

def f_main():
	global counter
	while True:
		global cmd
		if counter == 100:
			print("")
			x = str(input("Kommando eingeben: (start/stop/ende/acht/fahren/steuern/tasten/kugelfind):"))
			if x == "start":
				cmd = "start"
				counter = 0
				f_publishData("go")
				rate.sleep()
			elif x == "stop":
				f_publishData("stop")
				rate.sleep()
			elif x == "acht":
				f_achtfahren()
			elif x == "fahren":
				f_fahren()
			elif x == "ende":
				f_publishData("ende")
				rate.sleep()
				break
			elif x == "steuern":
				f_steuern()
			elif x == "kugelfind":
				f_kugel()
			elif x == "tasten":
				os.system("roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch")
			else:
				print("Bitte nur oben genannte Woerter eingeben!")

def f_steuern():
	while True:
		x = str(input("Bewegung eingeben: (gerade/drehen/ende):"))
		if x == "gerade":
			x = int(input("Wieviel cm soll gefahren werden? (-200 bis 200):"))
			if x < 201 and x > -201:
				f_drive_cm(x,0.2)
			else:
				print("Bitte nur oben genannte Woerter eingeben!")
		elif x == "drehen":
			x = int(input("Winkel angeben. (-360 bis 360 Grad):"))
			if x < 361 and x > -361:
				if x > -1:
					f_turnLeft(x)
				elif x < 0:
					f_turnRight(x * -1)
			else:
				print("Bitte nur oben genannte Woerter eingeben!")
		elif x == "ende":
			break
		else:
			print("Bitte nur oben genannte Woerter eingeben!")

def f_kugel():
	global cmd
	cmd = "startkugel"
	f_publishData("go")
	rate.sleep()

yspeed = 0
zspeed = 0
xturnspeed = 0
yturnspeed = 0

speed = 0.0005
turnspeed = 0
mission1 = 0
mission2 = 0
mission3 = 0
maxi = 0.09
maxturn = 0.3
#########################################################
def f_kugel_find(data):
	global mission1
	global mission2 
	global mission3
	arr = data.data
	sig = arr[0] 
	if mission1 == 0:#rote kugel finden und hinfahren
		if sig != 2:
			f_publish(0,0.5)
			rate.sleep()
		else:
			f_drive_ball(data,2)

	elif mission2 == 0:#blaue kugel finden
		if sig != 3:
			f_publish(0,0.5)
			rate.sleep()
		else:
			f_drive_ball(data,3)
	elif mission3 == 0:# gruene kugel
		if sig != 4:
			f_publish(0,0.5)
			rate.sleep()
		else:
			f_drive_ball(data,4)

def f_drive_ball(data,sign):
	global mission1
	global mission2 
	global mission3
	global speed
	global maxi
	global maxturn
	global turnspeed
	
	arr = data.data
	errordis = 0
	errorturn = 0
	factor = 0.0000018
	#0.00018
	factorturn = 0.03
	sig = arr[0] # farbe
	width = arr[1]			
	height = arr[2]
	acam = width * height #flaeche die erkannt wird
	x = arr[3]
	if acam > 4500 :
		errordis = 4500 - acam
		speed = speed + (errordis * factor)

	elif acam < 3200 :
		errordis = 3200 - acam
		speed = speed + (errordis * factor)
	else:
		speed = 0
	if x > 180:
		errorturn = 180 - x
		turnspeed = turnspeed + (errorturn * factorturn)

	elif x < 120 :
		errorturn = 120 - x
		turnspeed = turnspeed + (errorturn * factorturn)
	else: 
		turnspeed = 0

	if acam < 4000 and acam > 2700 and x < 170 and x > 130: 
		if sign == 2:
			mission1 = 1
			print("")
			print("Mission 1 Complete")
		elif sign == 3:
			mission2 = 1
			print("Mission 2 Complete")
		elif sign == 4:
			mission3 = 1
			print("Mission 3 Complete")
			print("Kommando eingeben: (start/stop/ende/acht/fahren/steuern/tasten/kugelfind):")
		return	
	if speed < -maxi: speed = -maxi
	if turnspeed < -maxturn: turnspeed = -maxturn
	if speed > maxi: speed = maxi
	if turnspeed > maxturn: turnspeed = maxturn
	f_publish(speed,turnspeed)
	rate.sleep()
####################################################################################################
def getBlocks(data):
	global counter
	global count
	global speed
	global maxi
	global maxturn
	global turnspeed
	
	arr = data.data
	errordis = 0
	errorturn = 0
	factor = 0.0000018
	factorturn = 0.03
	sig = arr[0] # farbe

	if counter < 100 and arr[0] > 0:
		print("Farbe: " + str(arr[0])+"")
		print("Position:  x: "+ str(arr[3]) + "  y: "+ str(arr[4]))
		print("Breite: "+str(arr[1])+" Hoehe: "+str(arr[2]))		
		counter = counter + 1

########### Teilblock falls rot erkannt wird
	if sig == 2:# rot
		if count == 10:
			width = arr[1]			
			height = arr[2]
			acam = width * height #flaeche die erkannt wird
			x = arr[3]
			if acam > 5000 :
				errordis = 5000 - acam
				speed = speed + (errordis * factor)

			elif acam < 3700 :
				errordis = 3700 - acam
				speed = speed + (errordis * factor)
			else:
				speed = 0
			if x > 160:
				errorturn = 160 - x
				turnspeed = turnspeed + (errorturn * factorturn)

			elif x < 100 :
				errorturn = 100 - x
				turnspeed = turnspeed + (errorturn * factorturn)
			else: 
				turnspeed = 0
			if speed < -maxi: speed = -maxi
			if turnspeed < -maxturn: turnspeed = -maxturn
			if speed > maxi: speed = maxi
			if turnspeed > maxturn: turnspeed = maxturn
			f_publish(speed,turnspeed)
			rate.sleep()
		elif count < 10:
			count = count +1
		elif count > 10:
			count = 0
########### Teilblock falls gelb erkannt wird
	elif sig == 1: # gelb
		f_publish(0,0)
		#f_achtfahren()
		rate.sleep()

########### Teilblock falls gruen erkannt wird
	elif sig == 4:#gruen
		f_publish(2,2)
		rate.sleep()
########### Teilblock falls blau erkannt wird
	elif sig == 3: #blau
		rate.sleep()
###########
	elif sig == 0:
		f_publish(0,0)
		rate.sleep()

def f_fahren(): 
	#f_turnRight(angle) rechtsdrehung
	#f_turnLeft(angle) linksdrehung 
	#angle legt winkel der drehung fest 
	#f_drive_cm(way_cm,drive_speed) faehrt cm nach vorne
	#way_cm anzahl cm die gefahren werden sollen
	#drive_speed Geschwindigkeit wobei: -0.5 < drive_speed < 0.5 ausser 0
	f_drive_cm(30,0.3)
	f_turnLeft(90)
	f_drive_cm(30,0.3)
	f_turnLeft(90)
	f_drive_cm(30,0.3)
	f_turnLeft(90)
	f_drive_cm(30,0.3)
	f_turnLeft(90)
######################################################################################################
def f_achtfahren():
	speed = 0.2
	f_publish(speed,0)
	rospy.sleep(1.5)
	turnspeed = 1.4
	f_publish(speed,turnspeed)
	rospy.sleep(5.5)
	f_publish(speed,0)
	rospy.sleep(3)
	f_publish(speed,-turnspeed)
	rospy.sleep(5.5)
	f_publish(speed,0)
	rospy.sleep(1.5)
	f_publish(0,0)

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
	drive_time = way_cm/abs(drive_speed * 100) 
	f_publish(drive_speed,0)
	rospy.sleep(drive_time)
	f_publish(0,0)

def f_publish(xspeed, zturnspeed):
	msg.linear.x = xspeed
	msg.linear.y = yspeed
	msg.linear.z = zspeed
	msg.angular.z = zturnspeed
	msg.angular.y = yturnspeed
	msg.angular.x = xturnspeed
	vel_pub.publish(msg)

def f_publishData(data):
	info_pub.publish(data)




f_main()

