def cloud_client(ip, port):
	import requests
	#import json
	#import simplejson
	from signal import signal, SIGPIPE, SIG_DFL
	signal(SIGPIPE, SIG_DFL)
	payload = {'key1': 'value1', 'key2': 'value2'}
	headers = {'Content-Type': 'application/x-www-form-urlencoded', 
			'Content-Length': str(len(payload))}
	r = requests.post('http://%s:%d' %(ip, port), payload, headers=headers)
#print r.json()

if __name__ == "__main__":
	ip = '192.168.0.20'
	port = 50000
	cloud_client(ip, port)
