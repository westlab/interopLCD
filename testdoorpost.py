# -*- coding:  utf-8 -*-
import requests,urllib2,sys,time
from flask import json

while True:
    send_data = [{},{},{},{}]
    try:
        f = open('door_data.txt','r')

        raw_data = f.readline().strip()
        f.close()
        for i, data in enumerate(raw_data.split(',')):
            if i == 0:
                send_data[i].update({
                    'background': 'white',
                    'text': u'Packets Received: ' + str(data),
                    'color': 'black',
                    'showImage': ''
                    })
            if i == 1:
                send_data[i].update({
                    'background': 'white',
                    'text': u'Packets Processed: ' + str(data),
                    'color': 'black',
                    'showImage': ''
                    })
            if i == 2:
                send_data[i].update({
                    'background': 'white',
                    'text': u'TCP Streams Reconstructed: ' + str(data),
                    'color': 'black',
                    'showImage': ''
                    })
            if i == 3:
                send_data[i].update({
                    'background': 'white',
                    'text': u'String Matches: ' + str(data),
                    'color': 'black',
                    'showImage': ''
                    })
    except:
        raw_data = 'Interop,2016,Keio Univ.,WEST LAB'
        for i, data in enumerate(raw_data.split(',')):
            if i == 0:
                send_data[i].update({
                    'background': 'black',
                    'text': u'' + str(data),
                    'color': 'white',
                    'showImage': ''
                    })
            if i == 1:
                send_data[i].update({
                    'background': 'black',
                    'text': u'' + str(data),
                    'color': 'blue',
                    'showImage': ''
                    })
            if i == 2:
                send_data[i].update({
                    'background': 'black',
                    'text': u'' + str(data),
                    'color': 'green',
                    'showImage': ''
                    })
            if i == 3:
                send_data[i].update({
                    'background': 'black',
                    'text': u'' + str(data),
                    'color': 'red',
                    'showImage': ''
                    })
        pass

    print send_data

#    r = requests.post('http://172.16.12.52:5000/api/lcd',json = send_data)
    r = requests.post('http://localhost:5000/api/door',json = send_data)

    time.sleep(2)
