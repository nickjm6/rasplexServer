from HTTPServer import BaseHTTPRequestHandler, HTTPServer
import subprocess


class HTTPServerHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		message = "INVALID REQUEST\n"
		pathArr = self.path.split("?")
		self.path = pathArr[0]
		varString = pathArr[1]
		if self.path == "/":
			message = "TRUE\n"
		elif self.path == "/currentOS":
			message = "rasplex\n"
		self.wfile.write(bytes(message))
		return

	def do_POST(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		message = "INVALID REQUEST"
		if self.path == "/switchOS":
			varibles = self.getVars()
			if "osName" in varibles.keys():
				newOS = varibles["osName"].lower()
				if newOS == 'raspbian' or newOS == 'retropie' or newOS == "kodi":
					try:
						message = subprocess.check_output(newOS, shell=True).decode()
					except Exception as e:
						message = "Switch was not succesffully excecuted: %s" % str(e)
				else:
					message = "Invalid OS"
			else:
				message = "Please enter an OS to switch to"
		elif self.path == "/reboot":
			try:
				message = subprocess.check_output("reboot", shell=True).decode()
			except:
				message = "reboot failed"
		elif self.path == "/rca":
			try:
				message = subprocess.check_output("rca", shell=True).decode()
			except:
				message = "reboot failed"
		elif self.path == "/hdmi":
			try:
				message = subprocess.check_output("hdmi", shell=True).decode()
			except:
				message = "reboot failed"
		self.wfile.write(bytes(message))

	def getVars(self):
		varString = self.rfile.read(int(self.headers['Content-Length'])).decode()
		varArray = varString.split("&")
		varDict = {}
		for v in varArray:
			name = v.split("=")[0]
			value = v.split("=")[1]
			varDict[name] = value
		return varDict



def run():
	portNo = 9876
	print("starting server at localhost:%d" % portNo)

	#checkServer
	server_address = ("localhost", 9876)
	httpdCheckServer = HTTPServer(server_address, HTTPServerHandler)
	httpdCheckServer.serve_forever()


	print("running server...")

run()
