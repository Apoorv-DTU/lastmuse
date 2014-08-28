#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from random import random
import requests
from lxml import html

def gen_headers():
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

def yt_url_from_track(track):
    url = track.replace(u' \u2013 ', '/_/')
    url = url.replace('+', '%2B')
    url = url.replace('?', '%3F')
    url = url.replace(' ', '+')
    
    music_r = requests.get("http://www.last.fm/music/" + url)
    
    music_tree = html.fromstring(music_r.text)
    video_xpath = ("/html/body/div[2]/article/div[1]/div[1]/section[4]/div/"
                    "div/div[1]/object/param[1]/@value")

    url = music_tree.xpath(video_xpath)
    video_id = ur
    return url

def vimeo_url_from_track(track):
    url = track.replace(u' \u2013 ', ' ')
    url = url.replace('+', '%2B')
    url = url.replace('?', '%3F')
    url = url.replace(' ', '+')
    url = url.replace('!', '')
    url = url.lower()
    
    head = gen_headers()

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

def yt_search(search_str):
   
    qs = ''.join(i if ord(i) < 128 else '' for i in search_str)
    qs.replace('+', '%2B');
    qs.replace(' ', '+'); 

    payload = {
        'search_query': qs
    }
    
    agent = ("Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0)" 
             "Gecko/20100101 Firefox/31.0") 
    header = {
        'User-Agent': agent
    }
    search_req = requests.get("http://youtube.com/results", 
                                params=payload, 
                                headers=header);

    results_tree = html.fromstring(search_req.text)
    for i in range(1, 11):

        result_xpath = ("/html/body/div[2]/div[3]/div/div[5]/div/div/div/"
                        "div[1]/div/div[2]/div[2]/ol/li/ol/li[" + str(i) + "]"
                        "/div/div[2]")
        result_title = results_tree.xpath(result_xpath + "/h3/a/text()")[0]
        result_desc = str(results_tree.xpath(result_xpath + 
                                         "/div[1]/ul/li[1]/b/a/text()"))
        
        if "VEVO" not in result_desc and "Mix" not in result_title:
            result_href = results_tree.xpath(result_xpath + "/h3/a/@href")[0]
            code = result_href.split('=', 1)[1]
            return code

    return None

tracklist = fetch_tracks()
i = 1

for track in tracklist:
    print "[%d] %s" % (i, track)
    video = vimeo_url_from_track(track)
    print "%s\n" % video
    i += 1
