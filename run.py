# we habe done multiThreading here

import multiprocessing
import subprocess

# To run luna
def startLuna():
    print("starting Luna")
    from main import start
    start()

# To run hotward detection
def listenHotword():
    print("running hotword detection")
    from engine.features import hotword
    hotword()

#start both process
if __name__ == '__main__':
        p1 = multiprocessing.Process(target=startLuna)
        p2 = multiprocessing.Process(target=listenHotword)
        p1.start()
        p2.start()
        p1.join()

        if p2.is_alive(): 
            p2.terminate()
            p2.join()

        print("system stop")            
        