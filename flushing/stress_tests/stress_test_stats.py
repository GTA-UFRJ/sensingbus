import psutil
import cPickle as pickle
import time
import thread

test_size = 1 #Number of gathering nodes involved
test_runs = 30 #number of times test is repeated
delay = 1
filename = "stats{}".format(test_size)


def get_stats(file):
    stats = {}
    stats["mem"] = psutil.virtual_memory()
    stats["cpu"] = psutil.cpu_times()
    stats["cpu_percent"] = psutil.cpu_percent()
    stats["network"] = psutil.net_io_counters(pernic=True)
    pickle.dump(stats, file)

def execute_tests():
    runs = 0
    with open(filename, 'wb') as f:
        while(runs < test_runs):
            runs+=1
            get_stats(f)
            print "run{}".format(runs)
            time.sleep(delay)
execute_tests()
