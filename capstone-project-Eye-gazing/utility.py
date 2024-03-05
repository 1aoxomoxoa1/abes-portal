import cv2
from inspect import getsourcefile
from os.path import abspath
import os

def list_ports():
    is_working = True
    dev_port = 0
    working_ports = []
    available_ports = []
    while is_working:
        camera = cv2.VideoCapture(dev_port)
        if not camera.isOpened():
            is_working = False
            print("Port %s is not working." % dev_port)
        else:
            is_reading, img = camera.read()
            w = camera.get(3)
            h = camera.get(4)
            if is_reading:
                print("Port %s is working and reads images (%s x %s)" % (dev_port, h, w))
                working_ports.append(dev_port)
            else:
                print("Port %s for camera ( %s x %s) is present but does not reads." % (dev_port, h, w))
                available_ports.append(dev_port)
        dev_port += 1
    return available_ports, working_ports

#if its not already in capstone-project-Eye-gazing, we want it there cuz thats our WD
def normalize_path_for_cwd(cwd, path):
    #fix package path as global variable
    #get path of currently executing file insead of cwd
    path_to_utility = os.path.abspath(__file__)
    os.path.dirname

    
    if 'capstone-project-Eye-gazing' not in cwd:
        return 'capstone-project-Eye-gazing/' + path
    else:
        return path
    

normalize_path_for_cwd(os.cw)
    
list_ports()