#!/usr/bin/env python

import json
import os
import random
import sys
import urllib2

def download_channel(channel, maxcoubs):
    #get relative path to script
    PATH = os.path.dirname(__file__)
    if PATH == '':
        PATH = '.'
        
    channel_url = 'https://coub.com/api/v2/timeline/random/' + channel
    channel_json = json.loads(urllib2.urlopen(channel_url).read())
    num_pages = channel_json['total_pages']
    pages = range(num_pages)
    random.shuffle(pages)

    coub_count = 0
    for page in pages: #for each page
        channel_json = json.loads(urllib2.urlopen(channel_url + '?page=' + str(page + 1)).read())
        coubs = range(len(channel_json['coubs']))
        random.shuffle(coubs)
        for i in coubs: #for each coub
            permalink = channel_json['coubs'][i]['permalink']
            title = permalink + '.mp4'
            mp4_url = 'https://coub.com/views/' + permalink
            os.system(PATH + '/coub-dl.js -i ' + mp4_url + ' -o ' + PATH + '/../mp4/' + title + ' -A -C')
            coub_count += 1
            if coub_count == maxcoubs:
                return

if __name__ == '__main__':
    argc = len(sys.argv)
    if argc == 2:
        download_channel(sys.argv[1], -1)
    elif argc == 3:
        download_channel(sys.argv[1], int(sys.argv[2]))
    else:
        raise 'usage: ./download-channel.py <channel> {<max coubs>}'
