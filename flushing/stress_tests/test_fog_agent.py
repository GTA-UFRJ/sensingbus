#Authors: Roberto Goncalves Pacheco
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
import psutil
import cPickle as pickle
import zlib
from os import listdir
from os.path import isfile, join

signal(SIGPIPE, SIG_DFL)

#SERVER_CERTS = '/home/pi/ssl/ca-chain.cert.pem' #To verify server
STOP_ID = 1 #This raspberrie's id
#MEASUREMENTS_URL = 'https://sensingbus.gta.ufrj.br/measurements_batch_sec/' #Endpoint of insertion api
MEASUREMENTS_URL = 'https://sensingbus.gta.ufrj.br/zip_measurements_batch_sec/' #Endpoint of insertion api
COMPRESSION_LEVEL = 9

# Variables for server-side validation:
PRIMARY_KEY='/home/pi/ssl/raspberry.key.pem'
LOCAL_CERTIFICATE='/home/pi/ssl/raspberry.cert.pem'

q = Queue.Queue()

first = True
first_received = time.time()
last_received = time.time()
bytes_received = 0
posts_received = 0

posts = {}

test_size = 1 #Number of gathering nodes involved
posts_per_client = 15 #Number of posts each gathering node makes
delay = 0.05 #Delay of each measurement
results_dir = join("results", str(test_size))

files = [f for f in listdir(results_dir) if isfile(join(results_dir, f))]
elapsed_runs = [int(x) for x in files]
print elapsed_runs
try:
    test_run = max(elapsed_runs) + 1
except (ValueError):
    test_run = 0
filename = join(results_dir, str(test_run))

def get_stats():
    stats = {}
    stats['time'] = time.time()
    stats['last_received'] = last_received
    stats['first_received'] = first_received
    stats['posts_received'] = posts_received
    stats['bytes_received'] = bytes_received
    if (last_received-first_received) > 0:
        stats['average_throughput'] = bytes_received/(last_received-first_received)
    else:
        stats['average_throughput'] = 0
    stats['mem'] = psutil.virtual_memory()
    stats['cpu'] = psutil.cpu_times()
    stats['cpu_percent'] = psutil.cpu_percent()
    stats['network'] = psutil.net_io_counters(pernic=True)
    with open(filename, 'ab') as f:
        pickle.dump(stats, f)

def execute_tests(run_event):
    while run_event.is_set():
        get_stats()
        time.sleep(delay)

def send_thread(thread_name,q, run_event):
    """Sends periodically stored data"""
    while run_event.is_set():
        print "Time elapsed = {}".format(last_received-first_received)
        print "Bytes received = {}".format(bytes_received)
        if (last_received-first_received) > 0:
            print "Average throughput = {}".format(bytes_received/(last_received-first_received))
        else:
            print "Average throughput = {}".format(0)
        print "Posts received = {}".format(posts_received)
        for i in posts:
            print "Node {} posts: {}".format(i, posts[i])
        output = {}
        output['stop_id'] = STOP_ID
        output['batches'] = []
        if not q.empty():
            while not q.empty():
                b = q.get()
                if ( b is not None):
                    output['batches'].append(b)
            cloud_client(output)
        time.sleep(5)

def cloud_client(payload):
    """ Sends mensage to Cloud"""
    payload = zlib.compress(json.dumps(payload).encode('utf-8').encode('zlib_codec'), COMPRESSION_LEVEL)
    r = requests.post(MEASUREMENTS_URL,
                    	data=payload,
                        #json=payload,
                        headers={'Content-Encoding':'text/plain'},
                    #verify=SERVER_CERTS,
                    cert=(LOCAL_CERTIFICATE, PRIMARY_KEY))
    #print r.json

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
        global posts_received
        global posts
        
        input_batches = {}
        post_size = int(self.headers['Content-Length'])

        bytes_received += post_size

        postvars = parse_qs(self.rfile.read(post_size),
                                                keep_blank_values=1)
        input_batches['node_id'] = postvars['node_id'][0]
        posts_received += 1
        posts[input_batches['node_id']] = posts.get(input_batches['node_id'], 0) + 1
        #print "postvars load = {}".format(postvars['load'])
        if postvars['load'][0][-1] == '\n':
            postvars['load'] = [postvars['load'][0][0:-1]]

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
            print "First"
            first_received = time.time()
            first = False

        q.put(input_batches)
        return


def run(server_class=HTTPServer, handler_class=S, port=50000):
    """Generates a server to receive POST method"""
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting Watch Thread'
    run_event = threading.Event()
    run_event.set()
    t = threading.Thread( target = send_thread, args=('alt',q, run_event))
    u = threading.Thread( target = execute_tests, args=(run_event,))
    t.daemon = True
    u.deamon = True
    t.start()
    u.start()
    try:
        print 'Starting Server Http'
        httpd.serve_forever()
    except KeyboardInterrupt:
        print "attempting to close threads"
        run_event.clear()
        t.join()
        u.join()
        print "threads successfully closed"

if __name__ == "__main__":
    run()
