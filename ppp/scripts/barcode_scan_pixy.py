#! /usr/bin/env python
sys.path.insert(0, "~/catkin_ws/src/uni_db/girlsday/scripts/pixy_api/")
import rospy
import math
from ctypes import *
from pixy_api import pixy
from pixy_api.pixy import *

pixy.init()
pixy.change_porg("line")

barcodes = BarcodeArray(100)
frame = 0

while 1:
    line_get_main_features(4,false)
    b_count = line_get_barcodes(100, barcodes)
    if b_count > 0:
        for index in range (0, b_count):
            print(Barcode)
            print(barcodes[index].m_code)