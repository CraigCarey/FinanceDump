#! /usr/bin/env python3

import threading
import time
import inspect

# class Thread(threading.Thread):
#     def __init__(self, t, *args):
#         threading.Thread.__init__(self, target=t, args=args)
#         self.start()

count = 0
lock = threading.Lock()

def incre():
    global count
    caller = inspect.getouterframes(inspect.currentframe())[1][3]
    print(f"Inside             {caller}")
    print(f"Acquiring lock     {caller}")
    with lock:
        print(f"Lock Acquired      {caller}")
        count += 1  
        time.sleep(2)  

def bye():
    while count < 5:
        incre()

def hello():
    while count < 5:
        incre()

def main():    
    h_t = threading.Thread(name='hello_thread', target=hello).start()
    g_t = threading.Thread(name='bye_thread', target=bye).start()


if __name__ == '__main__':
    main()
