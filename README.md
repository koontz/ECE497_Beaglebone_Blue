class project for ECE497 at rose-hulman
project wiki: http://elinux.org/ECE497_Project_Beaglebone_Blue_Robotics

At rose we have to use our own privte DNS server for internet connections.
If you get the error, cannot resolve host, change the nameserver to 8.8.8.8 in usbConfig and wificonfig

If the web server has issues using the roboticscape libary please update the path in webServer/server.py to reflect the libary .so location on your machine
