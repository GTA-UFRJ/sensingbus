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
SERVER_CERTIFICATE='/home/pi/ssl/ca-chain.cert.pem'

# Variables for server-side validation:
#MEASUREMENTS_URL = 'https://146.164.69.186/measurements_batch_sec/'
#PRIMARY_KEY='/home/pi/ssl/raspberry1.key.pem'
#LOCAL_CERTIFICATE='/home/pi/ssl/raspberry1.cert.pem'


#Cruz: repara que essa variável payload é primeiro um dicionário (quando ela ainda é postvars, no do_POST);
#depois ela é uma string json, quando você faz json.dumps pra criar o json_input; 
# depois, ela entra no cloud_client e é transformada de novo em um dicionário, pra ir pro requests.post. 
#Talvez tenha um jeito mais maneiro de fazer isso, usando ela como um dicionário direto =p
def cloud_client(payload):
    """ Sends mensage to Cloud"""
    headers = {'Content-Type' : 'application/json', 
                'Content-Length': str(len(payload))}
    r = requests.post(MEASUREMENTS_URL,
                    json.loads(payload),
                    headers=headers,
                    verify=SERVER_CERTIFICATE)#,
                    #cert=(LOCAL_CERTIFICATE, PRIMARY_KEY))
    print r

# Repara também que as bibliotecas que você está usando fazem com que nenhum dos 
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
        postvars = parse_qs(
                self.rfile.read(int(self.headers['Content-Length'])), 
                keep_blank_values=1)
        #print "Originalmente: "
        #print postvars
        #print "un-json: "
        #print json.dumps(postvars)
        #Cruz: O Json.dumps(d) pega um dicionário e transforma em uma string json
        # o Json.loads(s) pega uma string (em formato json) e transforma em dicionário.
        self.send_response(200)
        self.end_headers()
        self.wfile.write("Ok")
        json_vect.append(postvars)
        #Cruz: aqui era melhor você usar um dicionário, ao invés de construir um Json
        #Cruz: se você construir um dicionário output = {"stop_id": 1, "batches": []}, a
        # vida vai ser mais bonita. Depiois, você faz payload = json.dumps(output)
        json_input = '{"stop_id": 1, "batches": [%s ] }'%(json.dumps(json_vect))

        print json.loads(json_input)
        return

def run(server_class=HTTPServer, handler_class=S, port=50000):
    """Generates a server to receive POST method"""
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Iniciando Server Http'
    httpd.serve_forever()

if __name__ == "__main__":
    run()
