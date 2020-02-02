#!/bin/bash

#two arguments: client IP, client port
gst-launch-1.0 --gst-debug-level=2  -v -e v4l2src device=/dev/video1 -v !\
	     'video/x-raw, format=(string)YUV, width=(int)640, height=(int)480' !\
	               omxh264enc bitrate=600000  ! 'video/x-h264, stream-format=(string)byte-stream' !\
		              h264parse ! rtph264pay ! udpsink host=$1 port=$2
#gst-launch-1.0 --gst-debug-level=2  device=/dev/video1 !\
#'video/x-raw(memory:NVMM),width=3820, height=2464, framerate=21/1, format=YUV' !\
#          nvvidconv flip-method=2 ! omxh264enc bitrate=600000  ! 'video/x-h264, stream-format=(string)byte-stream' !\
#       h264parse ! rtph264pay ! udpsink host=$1 port=$2
