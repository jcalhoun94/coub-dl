#!/usr/bin/env python

import argparse
import json
import os
import random
import sys
import urllib2

audio = True
randomize = False

def download_channel(channel, maxcoubs):
    #get relative path to script
    PATH = os.path.dirname(__file__)
    if PATH == '':
        PATH = '.'
        
    channel_url = 'https://coub.com/api/v2/timeline/random/' + urllib2.quote(channel)
    channel_json = json.loads(urllib2.urlopen(channel_url).read())
    num_pages = channel_json['total_pages']
    pages = range(num_pages)
    if randomize:
        random.shuffle(pages)

    coub_count = 0
    for page in pages: #for each page
        channel_json = json.loads(urllib2.urlopen(channel_url + '?page=' + str(page + 1)).read())
        coubs = range(len(channel_json['coubs']))
        if randomize:
            random.shuffle(coubs)
        for i in coubs: #for each coub
            permalink = channel_json['coubs'][i]['permalink']
            title = permalink + '.mp4'
            mp4_url = 'https://coub.com/views/' + permalink
            command = PATH + '/coub-dl.js -i ' + mp4_url + ' -o ' + PATH + '/../mp4/' + title
            if not audio:
                command += ' -A'
            os.system(command + ' -C')
            coub_count += 1
            if coub_count == maxcoubs:
                return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', action = 'store_true')
    parser.add_argument('-n', nargs = 1, type = int, default = -1)
    parser.add_argument('-a', action = 'store_false', default = True)
    parser.add_argument('channel')
    args = parser.parse_args()
    randomize = args.r
    audio = args.a
    download_channel(args.channel, args.n)
