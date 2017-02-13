#Auhor: Roberto Goncalves Pacheco
#Universidade do Estado do Rio de Janeiro
#Departamento de Eletronica e Telecomunicacoes
#Project: Sensing Bus
#Subject: Comunication between Cloud and Fog


from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
from signal import signal, SIGPIPE, SIG_DFL
from urlparse import parse_qs
from threading import Timer
import json
import requests
signal(SIGPIPE, SIG_DFL)
MEASUREMENTS_URL = 'https://sensingbus.gta.ufrj.br/measurements_batch_sec'
json_vect = []
TIME_CONFIG = 60
cont = 0


def set_interval(function, interval, *params, **kwparams):
	def set_timer(wrapper):
		wrapper.timer = Timer(interval, wrapper)
		wrapper.timer.start()
	def wrapper():
		function(*params, **kwparams)
		set_timer(wrapper)
	set_timer(wrapper)
	return wrapper
def clear_interval(wrapper):
	wrapper.timer.cancel()

def cloud_client(payload):
    """ Sends mensage to Cloud"""
    import requests

    headers = {'Content-Type' : 'application/json', 
                'Content-Length': str(len(payload))}
    r = requests.post('https://sensingbus.gta.ufrj.br/measurements_batch_sec/',
                      json.loads(payload),
                      headers=headers,
                      verify="~/ca-chain.cert.pem")

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
	cont = 0
        postvars = parse_qs(
                self.rfile.read(int(self.headers['Content-Length'])), 
                keep_blank_values=1)
        #print postvars
	#print json.dumps(postvars)
        self.send_response(200)
        self.end_headers()
        self.wfile.write("Ok")
	json_vect.append(postvars)
	json_input = '{"stop_id": 1, "batches": [%s ] }'%(json.dumps(json_vect))
	print json.loads(json_input)
        #set_interval(cloud_client(json_input), 60)
	while (cont < TIME_CONFIG):
			
		cloud_client(json_input)	
		time.sleep(1)
		cont = cont + 1
		
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

