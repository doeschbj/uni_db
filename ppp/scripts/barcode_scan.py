#! /usr/bin/env python

import cv2
import rospy
from pyzbar import pyzbar
import imutils
from imutils.video import VideoStream
import time
from ppp.srv import barcode, barcodeResponse

vs = VideoStream( usePiCamera = True ).start()
time.sleep(2.0)

def f_handle_barcode(req):
    code = readCam()
    return barcodeResponse(int(code))


def readCam():
    old = 0
    i = 0
    while i < 2:
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        barcodes = pyzbar.decode(frame)

        if len(barcodes) > 0:
            code = barcodes[0].data.decode("utf-8")
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
    rospy.init_node('barcode_pi', anonymous=True)
    rate = rospy.Rate(60) # 20hzgle_lamp()
    f_init()
    s = rospy.Service('barcode_read_pi', barcode, f_handle_barcode)
    rospy.spin()

def f_init():
	print("Initialized QR SCAN")

if __name__ == '__main__':
	try:
		f_main()
	except rospy.ROSInterruptException:
		pass