#!/usr/bin/env python

import json
import os
import re
import sys
from unidecode import unidecode
import urllib2

def download_coubs(username, maxcoubs):
    PATH = os.path.dirname(__file__)
    coubs = 0 # keep count of downloads
    user_url = 'https://coub.com/api/v2/timeline/channel/' + username # json url
    json_data = json.loads(urllib2.urlopen(user_url).read()) # read json
    for page in range(1, json_data["total_pages"] + 1): # for each page
        for i in range(len(json_data["coubs"])): # for each coub
            permalink = json_data["coubs"][i]["permalink"] # get the unique id
            title = (re.sub('\s+', ' ', unidecode(json_data["coubs"][i]["title"])) + ' ' + permalink + '.mp4').lstrip() # use a standard filenamen
            mp4_url = 'https://coub.com/views/' + permalink # coub link
            os.system(PATH + '/coub-dl.js -i ' + mp4_url + ' -o ' + PATH + '/../mp4/"' + title + '" -A -C') # invoke coub-dl
            coubs = coubs + 1 # increment coub
            if coubs == maxcoubs: # if at maximum, return
                return
        user_url = user_url.rsplit('?', 1)[0] + '?page=' + str(page + 1) # go to next page
        json_data = json.loads(urllib2.urlopen(user_url).read()) # read new page

def main(argc, argv):
    if argc == 2:
        download_coubs(argv[1], -1) # download all coubs from user
    elif argc == 3:
        download_coubs(argv[1], int(argv[2])) # specify upper limit
    else:
        raise "invalid arguments" # must specify user

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
