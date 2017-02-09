from socket import *
import subprocess

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

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
while 1:
	try:
		connectionSocket, addr = serverSocket.accept()
		request = connectionSocket.recv(1024)
		HTTPHeaders = request.split("\n")
		requestHeader = HTTPHeaders[0].split(" ")
		method = requestHeader[0]
		path = requestHeader[1]
		headers = "HTTP/1.1 200 OK\nContent-Type: text/plain\n\n"
		message = "INVALID REQUEST"
		if method == "GET":
			pathStr = path
			if "?" in pathStr:
				pathArr = pathStr.split("?")
				path = pathArr[0]
				variableStr = pathArr[1]
				variables = getVars(variableStr)
			if path == "/":
				message = "TRUE\n"
			elif path == "/currentOS":
				message = "rasplex\n"
		elif method == "POST":
			variableArr = HTTPHeaders[-1]
			if path == "/switchOS":
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
				try:
					message = "attempting reboot"
					connectionSocket.send(headers + message)
					subprocess.check_output("reboot", shell=True).decode()
				except:
					message = "reboot failed:"
			elif path == "/rca":
				try:
					message = "attempting reboot"
					connectionSocket.send(headers + message)
					subprocess.check_output("./rca", shell=True).decode()
				except:
					message = "reboot failed"
			elif path == "/hdmi":
				try:
					message = "attempting reboot"
					connectionSocket.send(headers + message)
					subprocess.check_output("./hdmi", shell=True).decode()
				except:
					message = "reboot failed"
			elif path == "/volumeup":
				try:
					subprocess.check_output("./vol +", shell=True).decode()
					message = "volume increased"
				except:
					message = "volume change failed"
			elif path == "/volumedown":
				try:
					subprocess.check_output("./vol -", shell=True).decode()
					message = "volume decreased"
				except:
					message = "volume change failed"
		connectionSocket.send(headers + message)
		connectionSocket.close()
	finally:
		connectionSocket.close()
