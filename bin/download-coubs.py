#!/usr/bin/env python

import argparse
import json
import os
import random
import sys
import urllib2

def download_coubs(args):
    #get relative path to script
    PATH = os.path.dirname(__file__)
    if PATH == '':
        PATH = '.'
        
    coubs_url = 'https://coub.com/api/v2/timeline/' + ('tag/' if args.t else 'channel/') + urllib2.quote(args.search)
    coubs_json = json.loads(urllib2.urlopen(coubs_url).read())
    num_pages = coubs_json['total_pages']
    pages = range(num_pages)
    if args.r:
        random.shuffle(pages)

    coub_count = 0
    max_coubs = args.n[0] if isinstance(args.n, list) else args.n
    for page in pages: #for each page
        coubs_json = json.loads(urllib2.urlopen(coubs_url + '?page=' + str(page + 1)).read())
        coubs = range(len(coubs_json['coubs']))
        if args.r:
            random.shuffle(coubs)
        for i in coubs: #for each coub
            if args.x and coubs_json['coubs'][i]['not_safe_for_work'] == 0:
                continue
            permalink = coubs_json['coubs'][i]['permalink']
            title = coubs_json['coubs'][i]['title']
            filename = '\"' + permalink + ' - ' + title + '.mp4' + '\"'
            filename = filename.encode('ascii', 'ignore')
            mp4_url = 'https://coub.com/views/' + permalink
            command = PATH + '/coub-dl.js -i ' + mp4_url + ' -o ' + PATH + '/../mp4/' + filename
            if not args.a:
                command += ' -A'
            os.system(command + ' -C')
            coub_count += 1
            if coub_count == max_coubs:
                return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', action = 'store_true', default = False, help = 'randomize coubs')
    parser.add_argument('-n', nargs = 1, type = int, default = -1, help = 'max number of coubs to download')
    parser.add_argument('-a', action = 'store_false', default = True, help = 'download without audio')
    parser.add_argument('-t', action = 'store_true', default = False, help = 'change search from channel to tag')
    parser.add_argument('-x', action = 'store_true', default = False, help = '')
    parser.add_argument('search')
    download_coubs(parser.parse_args())
