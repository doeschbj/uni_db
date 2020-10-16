# import packages
import cv2
from pyzbar import pyzbar
import imutils
from imutils.video import VideoStream
import time
 
# initialize video stream and wait
vs = VideoStream( usePiCamera = True ).start()
time.sleep(2.0)
 
# loop over frames
while True:
    frame = vs.read()
    # for better performance, resize the image
    frame = imutils.resize(frame, width=400)
    # find and decode all barcodes in this frame
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        # do anything with that data
        print( barcode.data.decode("utf-8") )