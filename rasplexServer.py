#import the necessary dependancies
from socket import *
import subprocess

#set server port to 80, initialize the socket and bind it to the proper port
serverPort = 80
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

#set volume level to 100. This will not actually change the volume on the OS because I haven't figured that out yey
#This is just a placeholder so the RESTful API calls will work
vol = 100

#function that changes the volume
#Once again, this doesn't actually set the volume, it just changes a variable named 'vol'
def updateVol(upordown):
	global vol
	if upordown == "+":
		vol += 5
	elif upordown == "-":
		vol -= 5
	if vol > 100:
		vol = 100
	elif vol < 0:
		vol = 0
	return vol

#This function will take a url from an HTTP GET request and sort out the variables
def getVars(varString):
	varArr = varString.split("&")
	variables = {}
	for v in varArr:
		try:
			splitted = v.split("=")
			variable = splitted[0]
			value = splitted[1]
			variables[variable] = value
		except:
			continue
	return variables

print 'The server is ready to receive'

#loop forever, awaiting HTTP requests
while 1:
	try:
		#Recieve a request
		connectionSocket, addr = serverSocket.accept()
		request = connectionSocket.recv(1024)
		#Split all of the headers into an array
		HTTPHeaders = request.split("\n")
		#find out if the request is GET or POST. Also get the path from the request header
		requestHeader = HTTPHeaders[0].split(" ")
		method = requestHeader[0]
		path = requestHeader[1]
		#Set up header to be sent as a request
		headers = "HTTP/1.1 200 OK\nContent-Type: text/plain\n\n"
		message = "INVALID REQUEST"
		#Manage GET Requests
		if method == "GET":
			pathStr = path
			#Retrieve variables from request
			if "?" in pathStr:
				pathArr = pathStr.split("?")
				path = pathArr[0]
				variableStr = pathArr[1]
				variables = getVars(variableStr)
			#Now actually manage the calls
			if path == "/":
				#This call acts as a ping to see if raspberry pi is on
				message = "TRUE\n" 
			elif path == "/currentOS":
				#This call returns the current operating system, which will always be rasplex
				message = "rasplex\n"
			elif path == "/getVol":
				#This call return the volume level
				message = "%d\n" % vol
		#Manage POSTS requests
		elif method == "POST":
			#get the variables from HTTP request in the last header
			variableArr = HTTPHeaders[-1]
			if path == "/switchOS":
				#This call will switch the operating system if the request is valid
				variables = getVars(variableArr)
				if "osName" in variables.keys():
					newOS = variables["osName"].lower()
					if newOS == "raspbian" or newOS == "retropie" or newOS == "kodi":
						try:
							message = "attempting to switch OS"
							connectionSocket.send(headers + message)
							subprocess.check_output("./%s" % newOS, shell=True).decode()
						except Exception as e:
							message = "Switch was not sucessfully excecuted: %s" % str(e)
					else:
						message = "Invalid OS"
				else:
					message = "Please enter an OS to switch to"
			elif path == "/reboot":
				#This call will reboot the raspberry pi
				try:
					message = "attempting reboot"
					connectionSocket.send(headers + message)
					subprocess.check_output("reboot", shell=True).decode()
				except:
					message = "reboot failed:"
			elif path == "/rca":
				#this call sets display mode to RCA, displaying on my LCD touchscreen
				try:
					message = "attempting reboot"
					connectionSocket.send(headers + message)
					subprocess.check_output("./rca", shell=True).decode()
				except:
					message = "reboot failed"
			elif path == "/hdmi":
				#This call will set display mode to HDMI
				try:
					message = "attempting reboot"
					connectionSocket.send(headers + message)
					subprocess.check_output("./hdmi", shell=True).decode()
				except:
					message = "reboot failed"
			elif path == "/volumeup":
				#This call turns the volume up
				try:
					newVol = updateVol("+")
					message = "%d\n" % newVol
					# subprocess.check_output("./vol +", shell=True).decode()
					# message = "volume increased"
				except:
					message = "%d\n" % vol
			elif path == "/volumedown":
				#This call turns the volume down
				try:
					newVol = updateVol("-")
					message = "%d\n" % newVol
					# subprocess.check_output("./vol -", shell=True).decode()
					# message = "volume decreased"
				except:
					message = "%d\n" % vol
		#send the header and close the socket
		connectionSocket.send(headers + message)
		connectionSocket.close()
	except:
		connectionSocket.send(headers + message)
		connectionSocket.close()
		continue
	finally:
		#make sure to close the socket no matter what
		connectionSocket.close()
