#!/bin/bash
port=${1:-5805}
gst-launch-1.0 -vvv -e udpsrc port=${port} !\
	"application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" !\
	 rtph264depay ! avdec_h264 ! autovideosink
