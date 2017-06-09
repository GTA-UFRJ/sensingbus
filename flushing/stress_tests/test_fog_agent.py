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

#SERVER_CERTS = '/home/pi/ssl/ca-chain.cert.pem' #To verify server
STOP_ID = 1 #This raspberrie's id
MEASUREMENTS_URL = 'https://sensingbus.gta.ufrj.br/measurements_batch_sec/' #Endpoint of insertion api

# Variables for server-side validation:
PRIMARY_KEY='/home/pi/ssl/raspberry.key.pem'
LOCAL_CERTIFICATE='/home/pi/ssl/raspberry.cert.pem'

q = Queue.Queue()

first = True
first_received = time.time()
last_received = time.time()
bytes_received = 0
posts_received = 0


test_size = 1 #Number of gathering nodes involved
test_runs = 120 #maximum seconds test should take
delay = 0.5
filename = "stats{}".format(test_size)


def get_stats(file):

    stats = {}
    stats['time_elapsed'] = last_received-first_received
    stats['bytes_received'] = bytes_received
    stats['Average throughput'] = bytes_received/(last_received-first_received)
    
    stats['mem'] = psutil.virtual_memory()
    stats['cpu'] = psutil.cpu_times()
    stats['cpu_percent'] = psutil.cpu_percent()
    stats['network'] = psutil.net_io_counters(pernic=True)
    pickle.dump(stats, file)

def execute_tests():
    global posts_received
    with open(filename, 'wb') as f:
        while(posts_received < 30*test_size || delay*2 < test_runs):
            get_stats(f)
            #print "run{}".format(runs)
            time.sleep(delay)
execute_tests()


def send_thread(thread_name,q):
    """Sends periodically stored data"""
    while True:
        #print "Time elapsed = {}".format(last_received-first_received)
        #print "Bytes received = {}".format(bytes_received)
        #print "Average throughput = {}".format(bytes_received/(last_received-first_received))
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
                    #verify=SERVER_CERTS,
                    cert=(LOCAL_CERTIFICATE, PRIMARY_KEY))
    print r.text

class S(BaseHTTPRequestHandler):

    def _set_headers(self): 
        """Creates header HTTP requisition"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_POST(self): 
        """Receives data from Arduino and sends to Cloud"""
        global bytes_received
        global last_received
        global first
        input_batches = {}
        post_size = int(self.headers['Content-Length'])

        bytes_received += post_size

        postvars = parse_qs(self.rfile.read(post_size),
                                                keep_blank_values=1)
        input_batches['node_id'] = postvars['node_id'][0]
        posts_received += 1

        #print "postvars load = {}".format(postvars['load'])
        if postvars['load'][0][-1] == '\n':
            postvars['load'] = [postvars['load'][0][0:-1]]

        #print "postvars load = {}".format(postvars['load'])

        for line in postvars['load']:
            tmp = line.split('\n')

        delete_list = []
        for i in range(len(tmp)):
            #print "tmp[{}] = {}".format(i, tmp[i])
            date = tmp[i].split(",")[0]
            try:
               date = datetime.datetime.strptime(date, "%d%m%y%H%M%S00")
            except ValueError:
                delete_list.append(i)
        for i in reversed(delete_list):
            #print "deleting deffective date {}".format(tmp[i])
            del tmp[i]
                   
        input_batches['type'] = str(postvars['type'][0])
        input_batches['header'] = str(postvars['header'][0])
        input_batches['received'] = datetime.datetime.now().strftime("%d%m%y%H%M%S00")
        input_batches['load'] = tmp
        #print "Received = {}".format(input_batches['received'])
        last_received = time.time()
        
        if first:
            first_received = time.time()
            first = False
        
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
    execute_tests()
