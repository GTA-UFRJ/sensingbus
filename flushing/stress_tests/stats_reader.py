import cPickle as pickle

test_size = 1 #Number of gathering nodes involved
filename = "stats{}".format(test_size)

results = []
with open("filename", "rb") as f:
    while True:
        try:
            results.append(pickle.load(f))
        except EOFError:
            break

#results now has all the results
print results