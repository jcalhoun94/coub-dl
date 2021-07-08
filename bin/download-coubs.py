#!/usr/bin/env python2

import argparse
import json
import os
import random
import sys
import tempfile
import urllib2

def get_relative_path():
    path = os.path.dirname(__file__)
    return '.' if path == '' else path

def try_channel(args, url):
    url += 'channel/' + urllib2.quote(args.search)
    try:
        return (url, json.loads(urllib2.urlopen(url).read()))
    except urllib2.HTTPError:
        return (url, None)

def try_community(args, url):
    url += 'community/' + urllib2.quote(args.search) + '/half'
    try:
        return (url, json.loads(urllib2.urlopen(url).read()))
    except urllib2.HTTPError:
        return (url, None)

def try_tag(args, url):
    url += 'tag/' + urllib2.quote(args.search)
    try:
        return (url, json.loads(urllib2.urlopen(url).read()))
    except urllib2.HTTPError:
        return (url, None)

def get_url_and_json(args, url):
    (coubs_url, coubs_json) = try_community(args, url)
    if coubs_json is None:
        (coubs_url, coubs_json) = try_channel(args, url)
    if coubs_json is None:
        (coubs_url, coubs_json) = try_tag(args, url)
    if coubs_json is None:
        raise RuntimeError
    return (coubs_url, coubs_json)

def get_coubs_info(args):
    (coubs_url, coubs_json) = get_url_and_json(args, 'https://coub.com/api/v2/timeline/')
    coubs_pages = range(coubs_json['total_pages'])
    if args.r:
        random.shuffle(coubs_pages)
    return (coubs_url, coubs_json, coubs_pages)

def get_page_info(args, coubs_url, coubs_json, page):
    page_json = json.loads(urllib2.urlopen(coubs_url + '?page=' + str(page + 1)).read())
    page_coubs = range(len(coubs_json['coubs']))
    if args.r:
        random.shuffle(page_coubs)
    return (page_json, page_coubs)

def get_coub_info(args, page_json, coub):
    if page_json['coubs'][coub]['recoub_to'] is None:
        permalink = page_json['coubs'][coub]['permalink']
    else:
        permalink = page_json['coubs'][coub]['recoub_to']['permalink']
    title = page_json['coubs'][coub]['title']
    user = page_json['coubs'][coub]['channel']['permalink']
    nsfw = page_json['coubs'][coub]['not_safe_for_work']
    return (permalink, title, user, nsfw)

def get_download_command(args, permalink, title, user, bin_path, mp4_path):
    filename = ('\"' + title + ' - ' + user + ' - ' + permalink + '.mp4' + '\"').encode('ascii', 'ignore')
    mp4_url = 'https://coub.com/views/' + permalink
    command = os.path.join(bin_path, 'coub-dl.js') + ' -i ' + mp4_url + ' -o ' + os.path.join(mp4_path, filename)
    if not args.a:
        command += ' -A'
    command += ' -C'
    return command

def download_coubs(args):
    project_path = os.path.join(get_relative_path(), '..')
    bin_path = os.path.join(project_path, 'bin')
    mp4_path = os.path.join(project_path, 'mp4')

    (coubs_url, coubs_json, coubs_pages) = get_coubs_info(args)

    current_count = 0
    max_count = args.n[0] if isinstance(args.n, list) else args.n
    for i in coubs_pages: #for each page
        (page_json, page_coubs) = get_page_info(args, coubs_url, coubs_json, i)
        for j in page_coubs: #for each coub
            try:
                (permalink, title, user, nsfw) = get_coub_info(args, page_json, j)
            except IndexError:
                continue
            if args.x and (nsfw != True):
                continue
            command = get_download_command(args, permalink, title, user, bin_path, mp4_path)
            with tempfile.NamedTemporaryFile(delete = True) as f:
                os.system(command + ' > ' + f.name)
                if f.read() != '':
                    continue
            current_count += 1
            if current_count == max_count:
                return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', action = 'store_true', default = False, help = 'randomize coubs')
    parser.add_argument('-n', nargs = 1, type = int, default = -1, help = 'max number of coubs to download')
    parser.add_argument('-a', action = 'store_false', default = True, help = 'download without audio')
    parser.add_argument('-x', action = 'store_true', default = False)
    parser.add_argument('search')
    download_coubs(parser.parse_args())
