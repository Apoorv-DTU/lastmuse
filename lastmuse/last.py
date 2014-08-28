#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from random import random
import requests
from lxml import html

def _gen_headers():
    agents = [("Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0;" 
                   "InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; "
                   ".NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0"),           

                   ("Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36"),

                   "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0",

                   ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13"
                    "+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2")]

    index = int(random() * 100000 % 4)
    return {'User-Agent': agents[index]}

def fetch_tracks():
    url = "http://www.last.fm/charts/tracks/top/place/all" 
    fm_r = requests.get(url)
    fm_tree = html.fromstring(fm_r.text)

    tracklist = []
    for srl in range(1, 21):
        if srl is 1:
            track_xpath = ("/html/body/div[1]/div/div[6]/div[1]/div[1]/div/ol/"
                            "li[1]/div/div/a[1]/h4/span[2]/text()") 
        else:
            track_xpath = ("/html/body/div[1]/div/div[6]/div[1]/div[1]/div/ol/"
                            "li[" + str(srl) + "]/div/div/a/h4/span[2]/text()")
                           
        song = fm_tree.xpath(track_xpath)[0]
        tracklist.append(song)
    return tracklist

def vimeo_url_from_track(track):
    url = track.replace(u' \u2013 ', ' ')
    url = url.replace('+', '%2B')
    url = url.replace('?', '%3F')
    url = url.replace(' ', '+')
    url = url.replace('!', '')
    url = url.lower()
    
    head = _gen_headers()

    search_req = requests.get("http://vimeo.com/search?q=" + url, headers=head)
    if search_req.status_code != 200:
        print "Error %d: %s from %s" % (search_req.status_code, search_req.url, head['User-Agent'])
        
    res_tree = html.fromstring(search_req.text)
    xpath = ("/html/body/div[1]/div[2]/div[2]/div/div[1]/div[1]/"
             "div[3]/ol/li[1]/a/@href")
    
    url = "http://vimeo.com" + res_tree.xpath(xpath)[0]

    vid_req = requests.get(url, headers=head)
    vid_tree = html.fromstring(vid_req.text)

    vid_xpath = ("/html/body/div[1]/div[2]/div[2]/div/div[1]/"
                    "div[1]/div/div/@data-config-url")

    vid_url = vid_tree.xpath(vid_xpath)[0]
    json_r = requests.get(vid_url, headers=head)
    j = json_r.json()
    try:
        raw_vid = j[u'request'][u'files'][u'h264'][u'hd'][u'url']
    except KeyError:
        raw_vid = j[u'request'][u'files'][u'h264'][u'sd'][u'url'] 
    return raw_vid


tracklist = fetch_tracks()
i = 1

for track in tracklist:
    print "[%d] %s" % (i, track)
    video = vimeo_url_from_track(track)
    print "%s\n" % video
    i += 1
