#! /usr/bin/env python
import sys, os, time
sys.path.insert(0, "~/catkin_ws/src/uni_db/ppp/scripts/pixy_api/")
import rospy
import math
from ctypes import *
from pixy_api import pixy
from pixy_api.pixy import *

while 1:
    line_get_main_features()
    b_count = line_get_barcodes(100, barcodes)
    if b_count > 0:
        for index in range (0, b_count):
            print(Barcode)
            print(barcodes[index].m_code)

def f_handle_barcode(req):
    code = readCam()
    return barcodeResponse(int(code))


def readCam():
    old = 0
    i = 0
    while i < 4:
        barcodes = BarcodeArray(100)
        frame = 0
        line_get_main_features()
        b_count = line_get_barcodes(100, barcodes)
        if b_count > 0:
            code = barcodes[0].m_code
            if code == old:
                i = i + 1
            else:
                old = code
                i = 0
        else:
            code = -1
            if code == old:
                i = i + 1
            else:
                old = code
                i = 0

    return code

def f_main():
    rospy.init_node('barcode_pixy', anonymous=True)
    rate = rospy.Rate(60)
    f_init()
    s = rospy.Service('barcode_read_pixy', ReadBarcodePixy, f_handle_barcode)
    rospy.spin()

def f_init():
    pixy.init()
    pixy.change_prog("line")
    print("Initialized")

if __name__ == '__main__':
	try:
		f_main()
	except rospy.ROSInterruptException:
		pass