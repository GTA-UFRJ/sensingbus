from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import simplejson
import random
import json
from client3 import ClientJson
class BSTNode(object):
	def __init__(self, key):
		self.key = key
		self.setaFilhos(None, None)
	def setaFilhos(self, left, right):
		self.left = left
		self.right = right
	def balanco(self):
		prof_left = 0
		if self.left:
			prof_left = self.left.profundidade()
		prof_right = 0
		if self.right:
			prof_right = self.right.profundidade()
		return prof_left - prof_right
	def profundidade(self):
		prof_left = 0
		if self.left:
			prof_left = self.left.profundidade()
		prof_right = 0
		if self.right:
			prof_right = self.right.profundidade()
		return 1 + max(prof_left, prof_right)
	
	def rotationLeft(self):
		self.key, self.right.key = self.right.key, self.key
		old_left = self.left
		self.setaFilhos(self.right, self.right.right)
		self.left.setaFilhos(old_left, self.left.left)
	def rotationRight(self):
		self.key, self.left.key = self.left.key, self.key
		old_right = self.right
		self.setaFilhos(self.left.left, self.left)
		self.right.setaFilhos(self.right.right, old_right)
	def rotationLeftRight(self):
		self.left.rotationLeft()
		self.rotationRight()
	def rotationRightLeft(self):
		self.right.rotationRight()
		self.rotationLeft()
	def executaBalanco(self):
		bal = self.balanco()
		if bal > 1:
			if self.left.balanco() > 0:
				self.rotationRight()
			else:
				self.rotationLeftRight()
		elif bal < -1:
			if self.right.balanco() < 0:
				self.rotationLeft()
			else:
				self.rotationRightLeft()
	
	def get(self, key):
		if key < self.key:
			return self.left.get(key) if self.left else None
		elif key > self.key:
			return self.right.get(key) if self.right else None
		else:
			return self
	def add(self, key):
		if key <= self.key:
			if not self.left:
				self.left = BSTNode(key)
			else:
				self.left.add(key)
		else:
			if not self.right:
				self.right = BSTNode(key)
			else:
				self.right.add(key)
		self.executaBalanco()
	def imprimeArvore(self, indent = 0):
		print " " * indent + str(self.key)
		if self.left:
			self.left.imprimeArvore(indent + 2)
		if self.right:
			self.right.imprimeArvore(indent + 2)
		
	
def ClientJson(ip, port, payload):
	import requests
	import json
	import simplejson
	#payload = {'key': '25'}
	r = requests.post('http://%s:%d' %(ip, port), simplejson.dumps(payload))
def FogArduino(mode, ip_host, port, msg):
	import socket
	if ( mode == 'SocketTCP'):
		tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		destino = (ip_host, port)
		tcp.connect(destino)
		tcp.send(msg)
		tcp.close()
	elif ( mode == 'SocketUDP'):
		udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		destino = (ip_host, port)
		udp.sendto(msg, destino)
		udp.close()
	else:
		ClientJson(ip_host, port, msg)
class S(BaseHTTPRequestHandler):
	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.end_headers()
	def do_GET(self):
		self._set_headers()
		f = open("index.html", "r")
		self.wfile.write(f.read())
	
	def do_HEAD(self):
		self._set_headers()
	
	def do_POST(self):
		self.ip = "192.168.0.115"
		self.port = 8000
		self._set_headers()
		print "post method"
		self.data_string = self.rfile.read(int(self.headers['Content-Length']))
		self.send_response(200)
		self.end_headers()
		
		data = simplejson.loads(self.data_string)
		with open("test123.json", "w") as outfile:
			simplejson.dump(data, outfile)
		#print "{}".format(data)
		#print 'zoeira'
		#print 'temperatura'
		
		if (data['module_id'] == '0000'):
			print 'nuvem'
			module_id = data['id_arduino']
			tree.add(module_id)
			tree.imprimeArvore()
		else:
			print 'arduino'
			#print data['data'][0]['temperature']
			#ClientJson(self.ip, self.port, data)
			temperature = data['data'][0]['temperature']
			module_id = data['module_id']
			found = tree.get(module_id)
			if found:
				print 'encontrado'
				#FogArduino(mode, ip_host, port, msg)
			else:
				print 'nao encontrado'
			pass
def run(server_class=HTTPServer, handler_class=S, port=80):
	server_address = ('', port)
	httpd = server_class(server_address, handler_class)
	print 'Iniciando Server Http'
	httpd.serve_forever()	

'''def run2(server_class=HTTPServer, handler_class=S, port=5000):
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
	tree = BSTNode(9999)
        print 'Starting httpd...'
        httpd.serve_forever()
        print 'a'
'''

if __name__ == "__main__":
	tree = BSTNode(4500)
	run()

