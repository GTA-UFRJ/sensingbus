#Author: Roberto Goncalves Pacheco
#Universidade do Estado do Rio de Janeiro
#Departamento de Eletronica e Telecomunicacoes
#Project: Sensing Bus
#Subject: Comunication between Cloud and Fog


from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
from signal import signal, SIGPIPE, SIG_DFL
from urlparse import parse_qs
import json
import requests
import time
import datetime

signal(SIGPIPE, SIG_DFL)
SERVER_CERTS = '/home/pi/ssl/ca-chain.cert.pem'
STOP_ID = 1
SERVER_URL = 'https://sensingbus.gta.ufrj.br/measurements_batch_sec/'


def cloud_client(payload):
    """ Sends mensage to Cloud"""
    print "cloud client"
  
    r = requests.post(SERVER_URL,
                      json=payload,
                      verify=SERVER_CERTS)
    
  
    print r


class S(BaseHTTPRequestHandler):
    def _set_headers(self): 
        """Creates header HTTP requisition"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
    def do_GET(self):
        """ Handles GET method"""
        self._set_headers()
        f = open("index.html", "r")
        self.wfile.write(f.read())
    
    def do_HEAD(self):
        self._set_headers()
    
    def do_POST(self): 
        """Receives POST method"""
	output = {}
	input_batches = {}
	output['stop_id'] = STOP_ID
	output['batches'] = []
        postvars = parse_qs(self.rfile.read(int(self.headers['Content-Length'])), keep_blank_values=1)
	input_batches['node_id'] = postvars['node_id'][0]
	for line in postvars['load']:
		tmp = line.split('\n')
	input_batches['type'] = str(postvars['type'][0])
	input_batches['header'] = str(postvars['header'][0])
	input_batches['received'] = str(datetime.datetime.now())
	input_batches['load'] = tmp[0:-1] #the last line is always empty 
	output['batches'].append(input_batches)
	print output
	cloud_client(output)
        #self.send_response(200)
        #self.end_headers()
        #self.wfile.write("Ok")
	
        return
    
def run(server_class=HTTPServer, handler_class=S, port=50000):
    """ generates a server to receive POST method"""
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Iniciando Server Http'
    httpd.serve_forever()    

if __name__ == "__main__":
    run()
    
    #cloud_client(TASK_MANAGER_IP, 8000, 'msg')

