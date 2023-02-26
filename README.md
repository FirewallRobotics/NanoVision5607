# NanoVision5607

## General Jetson Setup
* When using Headless setup to update code and background services power needs to be provided by the barrel connection. Jumper needs to be on power pins. Micro Usb is used to connect laptop up by terminal program like Putty. See Nano developer startup guide for details.
 https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#setup

* use "systcl enable <application.service>" command to enable background services for robot
* use "sysctl disable <application.service>" command to disable background services
* use "sysctl list-units | grep team5607" to find background services for robot


## Hardware Issues

No longer an issue with updates
WIFI
* That WIFI dongle is flaky...
  * echo "blacklist rtl8192cu" | sudo tee -a /etc/modprobe.d/blacklist.conf
* Join network
  * nmcli d wifi connect "SSID" password "password"

FAN
* https://devtalk.nvidia.com/default/topic/1055225/jetson-nano/automagic-fan-control-for-the-jetson-nano-is-here-/
* https://github.com/Pyrestone/jetson-fan-ctl

## Requirements

* https://docs.nvidia.com/deeplearning/frameworks/install-tf-jetson-platform/index.html


sudo usermod -aG docker $USER

