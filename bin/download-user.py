#!/usr/bin/env python

import json
import os
import sys
import urllib2

def download_user(username, maxcoubs):
    #get relative path to script
    PATH = os.path.dirname(__file__)
    if PATH == '':
        PATH = '.'
        
    user_url = 'https://coub.com/api/v2/timeline/channel/' + username
    user_json = json.loads(urllib2.urlopen(user_url).read())
    num_pages = user_json['total_pages']

    coubs = 0
    for page in range(num_pages): #for each page
        user_json = json.loads(urllib2.urlopen(user_url + '?page=' + str(page + 1)).read())
        for i in range(len(user_json['coubs'])): #for each coub
            permalink = user_json['coubs'][i]['permalink']
            title = permalink + '.mp4'
            mp4_url = 'https://coub.com/views/' + permalink
            os.system(PATH + '/coub-dl.js -i ' + mp4_url + ' -o ' + PATH + '/../mp4/' + title + ' -A -C')
            coubs += 1
            if coubs == maxcoubs:
                return

if __name__ == '__main__':
    argc = len(sys.argv)
    if argc == 2:
        download_user(sys.argv[1], -1)
    elif argc == 3:
        download_user(sys.argv[1], int(sys.argv[2]))
    else:
        raise 'usage: ./download-user.py <username> {<max coubs>}'
