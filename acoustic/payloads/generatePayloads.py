import http.client

API_KEY = 'MjU5Y2VBMWY3OURiMUNmYmU3YTU4RENhRTpGQjVhZkYwRTE2RTlhOGFiZEZhOTlFNEEwRUQyYmQ0MzQxMTREMmZEZGVCNDU1YmRkRA=='

headers = {
    'Authorization' : 'Basic ' + API_KEY
}
conn = http.client.HTTPSConnection('audio.chirp.io')


def getChirp(data, protocol): 
    conn.request('GET', '/v3/{}/{}'.format(protocol, data), headers=headers)
    return conn.getresponse().read()

'''
downloads chirp mp3 for all possible single byte payloads
'''
def getPayloads(protocol='standard'):
    for i in range(256): 
        data = '%0.2X' % i #convert int to hex string
        chirpAudio = getChirp(data, protocol)
        fname = '{}/{}.mp3'.format(protocol,i)
        print('writing to', fname)
        
        with open(fname, 'wb') as f: 
            f.write(chirpAudio)
        

def main(): 
    getPayloads('standard')
    getPayloads('ultrasonic')

if __name__ == '__main__': 
    main()
