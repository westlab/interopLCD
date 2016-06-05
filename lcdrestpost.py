# -*- coding:  utf-8 -*-
import requests,urllib2,sys,time
from flask import json

except_data=[{
    'background': "black",
    'text': "Interop 2016",
    'color': "white",
    'showImage': "miku"
},
{
    'background': "black",
    'text': "慶應義塾大学西研究室",
    'color': "blue",
    'showImage': ""
},
{
    'background': "black",
    'text': "Service-oriented Router",
    'color': "red",
    'showImage': ""
}
]

while True:
    opened_url = True
    try:
        url = "http://localhost:80/api/v1/word_rank"
        openurl = urllib2.urlopen(url)

        raw_data = openurl.read()
        openurl.close()
        opened_url = True
    except:
        raw_data = json.dumps(except_data)
        opened_url = False
        pass

    decoded_data = json.loads(raw_data)
#    print raw_data
#    print decoded_data

    i = 0
    send_data = [{},{},{}]
    for data in decoded_data:
#        print data
        if opened_url:
            if i == 0:
                send_data[0].update({
                        'background': 'white',
                        'text': u'１位の単語は:' + str(data.get('name','')),
                        'color': 'black',
                        'showImage': ''
                    })
            if i == 1:
                send_data[1].update({
                        'background': 'black',
                        'text': u'２位の単語は:' + str(data.get('name','')),
                        'color': 'white',
                        'showImage': ''
                    })
            if i == 2:
                send_data[2].update({
                        'background': 'black',
                        'text': u'３位の単語は:' + str(data.get('name','')),
                        'color': 'red',
                        'showImage': ''
                    })
            if i > 2:
                break
        else:
            if i == 0:
                send_data[0].update({
                        'background': data.get('background',''),
                        'text': u''.join(data.get('text','')),
                        'color': data.get('color',''),
                        'showImage': data.get('showImage','')
                    })
            if i == 1:
                send_data[1].update({
                        'background': data.get('background',''),
                        'text': u''.join(data.get('text','')),
                        'color': data.get('color',''),
                        'showImage': data.get('showImage','')
                    })
            if i == 2:
                send_data[2].update({
                        'background': data.get('background',''),
                        'text': u''.join(data.get('text','')),
                        'color': data.get('color',''),
                        'showImage': data.get('showImage','')
                    })
            if i > 2:
                break

        i = i + 1

    print send_data

#    r = requests.post('http://192.168.1.2:5000/api/lcd',json = send_data)

    time.sleep(18000)
