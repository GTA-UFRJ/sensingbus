import os
import sys

params = sys.argv[1]

os.system("mv ./%s.py manager_fog.py" %(params))

os.system("scp ./manager_fog.py pi@192.168.0.1:/home/pi/manager_fog")

os.system("mv ./manager_fog.py %s.py" %(params))
