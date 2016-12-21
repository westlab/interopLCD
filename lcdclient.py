# -*- coding: utf-8 -*-
import json
import time
from itertools import islice

import requests


#door_endpoint = 'http://localhost:5000/api/v1/word_rank'
lcd_endpoint = 'http://192.168.1.2:5000/api/lcd'

default_data = [{
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

lcd_temp = dict(background='', text = '', color='', showImage='')
bg_colors = ['white', 'black', 'black']
txt_colors = ['balck', 'white', 'red']


def get_door_word_rank():
# ignore proxy
    session = requests.Session()
    session.trust_env = False
    try:
        r = session.get(door_endpoint)
        if r.status_code < 400:
            return json.loads(r.text)
	else:
	    return None
    except Exception as e:
        return None

def door2lcd(door_data):
    r = []
    for idx, word in enumerate(islice(door_data, 3)):
        d = lcd_temp.copy()
        d['background'] = bg_colors[idx]
        d['color'] = txt_colors[idx]
        d['text'] = word.get('name', '')
        r.append(d)
    return r

def main():
    while True:
        lcd_data = []
        data = get_door_word_rank()
        if data is None:
            lcd_data = default_data
	    print lcd_data
        else:
            lcd_data = door2lcd(data)
	    print lcd_data
        session = requests.Session()
        session.trust_env = False
        session.post(lcd_endpoint, json=lcd_data)

        time.sleep(60 * 5)

if __name__ == '__main__':
    main()
