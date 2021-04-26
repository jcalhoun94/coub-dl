#!/usr/bin/env python

import argparse
import json
import os
import random
import sys
import urllib2

randomize = False

def download_tag(tag, maxcoubs):
    #get relative path to script
    PATH = os.path.dirname(__file__)
    if PATH == '':
        PATH = '.'
        
    tag_url = 'https://coub.com/api/v2/timeline/tag/' + tag
    tag_json = json.loads(urllib2.urlopen(tag_url).read())
    num_pages = tag_json['total_pages']
    pages = range(num_pages)
    if randomize:
        random.shuffle(pages)

    coub_count = 0
    for page in pages: #for each page
        tag_json = json.loads(urllib2.urlopen(tag_url + '?page=' + str(page + 1)).read())
        coubs = range(len(tag_json['coubs']))
        if randomize:
            random.shuffle(coubs)
        for i in coubs: #for each coub
            permalink = tag_json['coubs'][i]['permalink']
            title = permalink + '.mp4'
            mp4_url = 'https://coub.com/views/' + permalink
            os.system(PATH + '/coub-dl.js -i ' + mp4_url + ' -o ' + PATH + '/../mp4/' + title + ' -A -C')
            coub_count += 1
            if coub_count == maxcoubs:
                return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', action = 'store_true')
    parser.add_argument('tag')
    parser.add_argument('num', type = int, default = -1)
    args = parser.parse_args()
    randomize = args.r
    download_tag(args.tag, args.num)
