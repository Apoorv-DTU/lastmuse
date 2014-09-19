#!/usr/bin/python3

from __future__ import print_function
from __future__ import unicode_literals
from random import random

import requests
from lxml import html
from lastmuse.selector import *

class Track(object):

    def __init__(self, srl, name):
        self.srl = srl
        self.name = name
        self.url = None
        self.image = None
        self.lyrics = ""

        self._qs = _prepare_qs(self.name, ' ', '+')
        self._html = None

    def gen_url(self, hd=True, force=False):

        if not _validate(self.url, force):
            return

        head = _gen_headers()
        search_req = requests.get("http://vimeo.com/search?q=" + 
                                  self._qs,
                                  headers=head)

        res_tree = html.fromstring(search_req.text)
        xpath = ("/html/body/div[1]/div[2]/div[2]/div/div[1]/div[1]/"
                 "div[3]/ol")

        results = []
        for i in range(5):
            title = res_tree.xpath(xpath + "/li[" + str(i+1) + "]/a/@title")[0]
            results.append(title)

        result = select(self.name, results)
        index = results.index(result)
        xpath += "/li[" + str(index+1) + "]/a/@href"

        url = "http://vimeo.com" + res_tree.xpath(xpath)[0]

        vid_req = requests.get(url, headers=head)
        vid_tree = html.fromstring(vid_req.text)

        vid_xpath = ("/html/body/div[1]/div[2]/div[2]/div/div[1]/"
                     "div[1]/div/div/@data-config-url")

        vid_url = vid_tree.xpath(vid_xpath)[0]
        json_r = requests.get(vid_url, headers=head)
        j = json_r.json()

        if hd:
            try:
                raw_vid = j['request']['files']['h264']['hd']['url']
            except KeyError:
                raw_vid = j['request']['files']['h264']['sd']['url']
        else:
            raw_vid = j['request']['files']['h264']['sd']['url']

        self.url = raw_vid

    def gen_image(self, force=False):

        if not _validate(self.image, force):
            return

        if srl is 1:
            img_xpath = ("/html/body/div[1]/div/div[6]/div[1]/div"
                         "[1]/div/ol/li[1]/div/div/a[1]/div/div/img/@src")
        else:
            img_xpath = ("/html/body/div[1]/div/div[6]/div[1]/div[1]"
                         "/div/ol/li[" + srl + "]/div/div/a/img/@src")

        img_url = self._html.xpath(img_xpath)
        img_request = requests.get(img_url)
        self.image = img_request

    def gen_lyrics(self, force=False):

        if not _validate(self.lyrics, force):
            return

        url = _prepare_qs(self.name, '/', '')
        url = url.split('(')[0]
        
        lyr_r = requests.get("http://www.azlyrics.com/lyrics/" + url + ".html")
        lyr_html = lyr_r.text.replace('<i>', '').replace('</i>', '')
        lyr_tree = html.fromstring(lyr_html)
        lyrics_list = lyr_tree.xpath("/html/body/div[2]/div[3]/text()")

        self.lyrics = ''.join(lyrics_list)


def _validate(attrib, is_forced):

    if attrib:
        if not is_forced:
            return False
        else:
            return True
    else:
        return True


def _gen_headers():
    agents = ["Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; "
              "Trident/5.0; InfoPath.2; SLCC1; "
              ".NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; "
              ".NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0",

              "Mozilla/5.0 (Windows NT 6.3; Win64; x64) "
              "AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/37.0.2049.0 Safari/537.36",

              "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101"
              " Firefox/31.0",

              "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) "
              "AppleWebKit/537.13+ (KHTML, like Gecko) "
              "Version/5.1.7 Safari/534.57.2"]

    return {'User-Agent': agents[int(random() * 100000 % 4)]}


def fetch_tracks():
    url = "http://www.last.fm/charts/tracks/top/place/all"
    fm_r = requests.get(url, headers=_gen_headers())
    fm_tree = html.fromstring(fm_r.text)

    tracklist = [Track(1, fm_tree.xpath("/html/body/div[1]/div/div[6]/div[1]/"
                                        "div[1]/div/ol/li[1]/div/div/a[1]/h4/"
                                        "span[2]/text()")[0].replace('\u2013', '-'))]

    for srl in range(2, 21):
        track_xpath = ("/html/body/div[1]/div/div[6]/div[1]/div[1]/div/ol/"
                       "li[" + str(srl) + "]/div/div/a/h4/span[2]/text()")

        song = fm_tree.xpath(track_xpath)[0]
        song = song.replace("\u2013", '-')
        tracklist.append(Track(srl, song))
    return tracklist


def _prepare_qs(string, uni, space):

    url = string.replace(' - ', uni)
    url = url.replace('+', '%2B')
    url = url.replace('?', '%3F')
    url = url.replace(' ', space)
    url = url.replace('\'', '')
    url = url.replace('"', '')

    for symbol in "!@#$%^&*":
        url = url.replace(symbol, '')

    url = url.lower()
    url = url.split('(')[0]
    return url
