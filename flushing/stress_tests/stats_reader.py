import cPickle as pickle
#import numpy as np, scipy.stats as st
from os import listdir
from os.path import isfile, join

test_sizes = [1]#, 5, 10, 15, 20] #Number of gathering nodes involved

results_dir = "results"

cpu_usage = {}
mem_usage = {}
net_usage = {}
avg_throughput = {}
#bytes_received = {}


total_cpu_usage = []
total_mem_usage = []
total_net_usage = []
total_avg_throughput = []
total_cpu_usage_err = []
total_mem_usage_err = []
total_net_usage_err = []
total_avg_throughput_err = []

for test_size in test_sizes:
    tests_dir = join(results_dir, str(test_size))
    files = [f for f in listdir(tests_dir) if isfile(join(tests_dir, f))]

    cpu_usage[test_size] = []
    mem_usage[test_size] = []
    net_usage[test_size] = []
    avg_throughput[test_size] = []

    #Every file holds data of a single run
    for filename in files:
        results = []

        first_received = 0
        last_received = 0

        with open(join(tests_dir, filename), "rb") as f:
            #Collecting data and discovering the time interval when tests happened
            while True:
                try:
                    r = pickle.load(f)
                    results.append(r)
                    #print r
                    if r['first_received'] > first_received:
                        first_received = r['first_received']
                    if r['last_received'] > last_received:
                        last_received = r['last_received']
                except EOFError:
                    break
            print "First received = {}".format(first_received)
            print "Last received = {}".format(last_received)
            print "Number of measurements = {}".format(len(results))
            tmp_cpu_usage = []
            tmp_mem_usage = []
            tmp_net_usage = []
            tmp_avg_throughput = []
            for r in results:
                if r['time'] > first_received and r['time'] < last_received:
                    tmp_cpu_usage.append(r['cpu_percent'])
                    tmp_mem_usage.append(r['mem'].percent)
                    #tmp_net_usage.append(r['wlan0'].dropin + r['wlan0'].dropout)
                    tmp_avg_throughput.append(r['average_throughput'])

            print "CPU Usage = {}".format(tmp_cpu_usage)
            print "Mem Usage = {}".format(tmp_mem_usage)
            print "Avg Throughput = {}".format(tmp_avg_throughput)

            #cpu_usage[test_size].append(np.mean(tmp_cpu_usage))
            #mem_usage[test_size].append(np.mean(tmp_mem_usage))
            #net_usage[test_size].append(np.mean(control_packets))
            #avg_throughput[test_size].append(np.mean(tmp_avg_throughput))


    print "CPU Usage = {}".format(cpu_usage)
    print "Mem Usage = {}".format(mem_usage)
    print "Avg Throughput = {}".format(avg_throughput)
"""
    #Calculating avg and confidence for a certain test size
    total_cpu_usage.append(np.mean(cpu_usage[test_size]))
    confidence = st.t.interval(0.95,
        len(cpu_usage[test_size])-1,
        loc=np.mean(cpu_usage[test_size]),
        scale=st.sem(cpu_usage[test_size]))
    total_cpu_usage_err.append(confidence[1] - confidence[0])

    total_mem_usage.append(np.mean(mem_usage[test_size]))
    confidence = st.t.interval(0.95,
        len(mem_usage[test_size])-1,
        loc=np.mean(mem_usage[test_size]),
        scale=st.sem(mem_usage[test_size]))
    total_mem_usage_err.append(confidence[1] - confidence[0])

    total_net_usage.append(np.mean(net_usage[test_size]))
    confidence = st.t.interval(0.95,
        len(net_usage[test_size])-1,
        loc=np.mean(net_usage[test_size]),
        scale=st.sem(net_usage[test_size]))
    total_net_usage_err.append(confidence[1] - confidence[0])

    total_avg_throughput.append(np.mean(avg_throughput[test_size]))
    confidence = st.t.interval(0.95,
        len(avg_throughput[test_size])-1,
        loc=np.mean(avg_throughput[test_size]),
        scale=st.sem(avg_throughput[test_size]))
    total_avg_throughput_err.append(confidence[1] - confidence[0])
"""
#results now has all the results
#print results
