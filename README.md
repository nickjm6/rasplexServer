# Retropie Server

This is a Web Server Running on my Raspberry Pi on the Rasplex operating System.

The Raspberry Pi also runs RetroPie, Kodi(OSMC), and Raspbian. 
Each of these Operating Systems has their own web server very simalar to this.
This is the only one of the web servers that hosts a socket using python.
The other web servers use Node.js

The point of these web servers is create an interface that allows me to interact with the Pi

If you want to use this multi-boot set up for the raspberry pi, here is where I found it:

	http://www.multibootpi.com/builds/quad-boot-raspbian-pixel-retropie-rasplex-kodi/

All of these web servers, along with the web site that interacts with these web servers are on my GitHub account:
	
	https://github.com/nickjm6

The Server for this operating system was very difficult to work with due to the fact that it is a read only file system.

To host the server, you can simply run:
	python rasplexServer.py

However, this will not make the server start on boot. There are a few ways to do this.
The ways that I know of are to make a Service or to edit the crontab file. 

The way I did it was to edit the crontab file. For more information on how to make something run on boot, Look up crontab on google.

