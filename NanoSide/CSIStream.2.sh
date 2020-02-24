#!/bin/bash
host=roborio-5607-frc.local
port=5805

while getopts ":h:p:" opt; do
	case ${opt} in
		h ) # process option h
			host=$OPTARG
			shift;
		;;
		p ) # process option p
			port=$OPTARG
			shift;
		;;
		\? ) echo "Usage: $0 [-h] [-p]"
		;;
		esac
done

#two arguments: client IP, client port
#1280 x 720
gst-launch-1.0 nvarguscamerasrc !\
'video/x-raw(memory:NVMM),width=640, height=360, framerate=30/1, format=NV12' !\
          nvvidconv flip-method=2 ! omxh264enc bitrate=3000000 control-rate=4 ! 'video/x-h264, stream-format=(string)byte-stream' !\
       h264parse !  mpegtsmux ! rtpmp2tpay ! udpsink async=false host=$host port=$port
exit
#!  mpegtsmux ! rtpmp2tpay ! udpsink async=false host=$host port=$port
# rtph264pay
gst-launch-1.0 nvarguscamerasrc ! \
	  'video/x-raw(memory:NVMM), width=(int)1920, height=(int)1080, \
	    format=(string)NV12, framerate=(fraction)15/1' ! nvv4l2h264enc ! \
	      h264parse !mpegtsmux ! rtpmp2tpay ! udpsink async=false host=$host port=$port
