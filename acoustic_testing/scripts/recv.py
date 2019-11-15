#!/usr/bin/python3
import time, sys, argparse
from chirpsdk import ChirpSDK, CallbackSet

class Callbacks(CallbackSet):
    def on_receiving(self, channel): 
        print('receiving')
    
    def on_received(self, payload, channel):
        if payload is not None:
            identifier = payload.decode('utf-8')
            print('Received:', payload)
        else:
            print('Decode failed')

def main(blockname='default'):
    chirp = ChirpSDK(block=blockname)
    chirp.set_callbacks(Callbacks())
    chirp.input_sample_rate = 48000 #USB mic requires 48Khz to function
    chirp.start(send=False, receive=True)

    try:
        print("SDK initialized successfully. Using",blockname,"configuration.")
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print('Exiting')

    chirp.stop()

if __name__ == '__main__': 
    parser = argparse.ArgumentParser(description='Listen for chirps.')
    parser.add_argument('-u', action='store_true', default=False, dest='ultrasonic',help='use ultrasonic protocol')
    results = parser.parse_args()
    if results.ultrasonic: 
        main(blockname='ultrasonic')
    else: 
        main(blockname='default')
