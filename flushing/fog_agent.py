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
import threading, Queue

signal(SIGPIPE, SIG_DFL)

SERVER_CERTS = '/home/pi/ssl/ca-chain.cert.pem' #To verify server
STOP_ID = 1 #This raspberrie's id
MEASUREMENTS_URL = 'https://sensingbus.gta.ufrj.br/measurements_batch_sec/' #Endpoint of insertion api

# Variables for server-side validation:
PRIMARY_KEY='/home/pi/ssl/raspberry.key.pem'
LOCAL_CERTIFICATE='/home/pi/ssl/raspberry.cert.pem'

q = Queue.Queue()

def send_thread(thread_name,q):
    """Sends periodically stored data"""
    while True:
        output = {}
        output['stop_id'] = STOP_ID
        output['batches'] = []
        if not q.empty():
            while not q.empty():
                b = q.get()
                if ( b is not None):
                    output['batches'].append(b)
            cloud_client(output)    
       time.sleep(30)

def cloud_client(payload):
    """ Sends mensage to Cloud"""
    r = requests.post(MEASUREMENTS_URL,
                    json=payload,
                    verify=SERVER_CERTS,
                    cert=(LOCAL_CERTIFICATE, PRIMARY_KEY))
    print r

class S(BaseHTTPRequestHandler):
    def _set_headers(self): 
        """Creates header HTTP requisition"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_POST(self): 
        """Receives data from Arduino and sends to Cloud"""
        input_batches = {}
        post_size = int(self.headers['Content-Length'])
        print "Post size: {}".format(post_size)
        postvars = parse_qs(self.rfile.read(post_size),
                                                keep_blank_values=1)
        input_batches['node_id'] = postvars['node_id'][0]
        for line in postvars['load']:
            tmp = line.split('\n')

        #delete data with defective date
        delete_list = []
        for i in range(len(tmp)):
            if (tmp[i][0:-1] == 0):
                delete_list.append(i)
        for i in reversed(delete_list):
            del tmp[i]
                    
        input_batches['type'] = str(postvars['type'][0])
        input_batches['header'] = str(postvars['header'][0])
        input_batches['received'] = str(datetime.datetime.now())
        input_batches['load'] = tmp[0:-1] #the last line is always empty 
        q.put(input_batches)
        return

def run(server_class=HTTPServer, handler_class=S, port=50000):
    """Generates a server to receive POST method"""
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting Server Http'
    t = threading.Thread( target = send_thread, args=('alt',q))
    t.daemon = True
    t.start()
    httpd.serve_forever()
    t.join()

if __name__ == "__main__":
    run()
