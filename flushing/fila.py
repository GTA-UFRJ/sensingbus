import threading, Queue
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

def cartridge(tmp):
	q = Queue.Queue()
	t = threading.Thread( target = send_thread, args=('alt',q))
	t.daemon = True
	t.start()


	


	
