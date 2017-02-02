from http.server import BaseHTTPRequestHandler, HTTPServer
import os

class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		os.system("python test.py")
		message = "Hello World!\n"
		self.wfile.write(bytes(message, 'utf8'))
		return

def run():
	portNo = 6666
	print("starting server at localhost:%d" % portNo)
	server_address= ("localhost", 6666)
	httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
	print("running server...")
	httpd.serve_forever()

run()