# NanoVision5607

## Hardware Issues

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
