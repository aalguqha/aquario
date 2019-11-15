import time, os, sys, argparse, random, json
from chirpsdk import ChirpSDK, CallbackSet, CHIRP_SDK_STATE_STOPPED
from playsound import playsound
timeSent = -1
current = None

class Callbacks(CallbackSet):	
    def on_state_changed(self, previous_state, current_state):
        if current_state == CHIRP_SDK_STATE_STOPPED:
            print("ChirpSDK has stopped")

    def on_receiving(self, channel):
        delay = time.time() - timeSent
        current['received'] = True
        current['receive_delay'] = delay
        print('receiving after %.02f'%delay, 'seconds')
        

    def on_received(self, payload, channel):
        
        if payload is None:
            print('Decode failed')
        else:
            delay = time.time() - timeSent
            current['decoded'] = True
            current['decode_delay'] = delay - current['receive_delay']
            print('Received data: ', ord(payload), end='\n\n')


'''
test acoustic channel by sending and receiving prerecorded chirps
'''
def test(protocol, chirps):
    global timeSent, current 
    
    logdir = 'results/{}/'.format(time.strftime("%Y%m%d-%H%M%S"))
    
    os.makedirs(logdir, exist_ok=True)
    
    if protocol == 'standard': 
        protocol = 'default'
    
    chirp = ChirpSDK(block=protocol, debug=True, config='config')
    
    chirp.audio.wav_filename = logdir + 'debug.wav'
    chirp.input_sample_rate = 48000 #USB mic requires 48Khz to function
    chirp.set_callbacks(Callbacks())
    chirp.start(send=False, receive=True)

    log = []
    for chirp in chirps:
        data = chirp.split('/')[-1].replace('.mp3', '')
        current = {
            'sent': data, 
            'received' : False, 
            'receive_delay': -1, 
            'decoded': False,
            'decode_delay': -1
            }
        print('sending {}'.format(data))
        timeSent = time.time()
        playsound(chirp, block=True) #async playback not supported on linux for some reason
        time.sleep(1) 
        log.append(current)
    
    print('tests complete, saving results...')

    with open(logdir+'log.json', 'w') as outfile: 
        json.dump({'log': log}, outfile, indent=4)
    print('done.')


'''
Returns a list containing chirp mp3 files for testing. 
'''
def loadChirps(protocol='standard', num=10, shuffle=False): 
    chirps = []
    prefix = 'payloads/{}/'.format(protocol)
    if num > 256: 
        print('num must be <= 256')
        return
    for i in range(256): 
        chirps.append(prefix+str(i)+'.mp3')
    
    if shuffle: 
        random.shuffle(chirps)
    
    return chirps[:num]
    

def main(): 
    chirps = loadChirps(protocol='ultrasonic', num=50, shuffle=True)
    test(protocol='ultrasonic', chirps)

if __name__ == '__main__':
    main()