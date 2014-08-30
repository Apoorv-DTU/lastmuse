#!/usr/bin/python3

from __future__ import print_function
from __future__ import unicode_literals
from random import random

import requests
from lxml import html


class Track(object):

    def __init__(self, srl, name):
        self.srl = srl
        self.name = name
        self.url = None
        self.image = None
        self.lyrics = None

        self._qs = _prepare_qs(self.name)
        self._html = None

    def gen_url(self, force=False):

        if self.url is not None:
            if not force:
                return
            else:
                pass
        else:
            pass

        head = _gen_headers()
        search_req = requests.get("http://vimeo.com/search?q=" + self._qs,
                                  headers=head)

        if search_req.status_code != 200:
            print("Error {:d}: {:s} from {:s}".format(search_req.status_code,
                                                      search_req.url,
                                                      head['User-Agent']))

        res_tree = html.fromstring(search_req.text)
        xpath = ("/html/body/div[1]/div[2]/div[2]/div/div[1]/div[1]/"
                 "div[3]/ol/li[2]/a/@href")

        url = "http://vimeo.com" + res_tree.xpath(xpath)[0]

        vid_req = requests.get(url, headers=head)
        vid_tree = html.fromstring(vid_req.text)

        vid_xpath = ("/html/body/div[1]/div[2]/div[2]/div/div[1]/"
                     "div[1]/div/div/@data-config-url")

        vid_url = vid_tree.xpath(vid_xpath)[0]
        json_r = requests.get(vid_url, headers=head)
        j = json_r.json()

        try:
            raw_vid = j['request']['files']['h264']['hd']['url']
        except KeyError:
            raw_vid = j['request']['files']['h264']['sd']['url']

        self.url = raw_vid

    def gen_image(self, force=False):

        if self.image is not None:
            if not force:
                return
            else:
                pass
        else:
            pass

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

        if self.lyrics is not None:
            if not force:
                return
            else:
                pass
        else:
            pass

        url = self.name.split(' \u2013 ')
        url = '/'.join(url)
        url = url.replace(' ', '')
        url = url.replace('&', '')
        url = url.replace('?', '')
        url = url.replace('!', '')
        url = url.lower()
        if "(" in url:
            url = url.split('(')[0]

        lyr_r = requests.get("http://www.azlyrics.com/lyrics/" + url + ".html")
        lyr_tree = html.fromstring(lyr_r.text)
        lyrics_list = lyr_tree.xpath("/html/body/div[2]/div[3]/text()")

        lyrics = ""
        for clause in lyrics_list:
            lyrics += clause

        self.lyrics = lyrics


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
    fm_r = requests.get(url)
    fm_tree = html.fromstring(fm_r.text)

    tracklist = [Track(1, fm_tree.xpath("/html/body/div[1]/div/div[6]/div[1]/"
                                        "div[1]/div/ol/li[1]/div/div/a[1]/h4/"
                                        "span[2]/text()")[0])]

    for srl in range(2, 21):
        track_xpath = ("/html/body/div[1]/div/div[6]/div[1]/div[1]/div/ol/"
                       "li[" + str(srl) + "]/div/div/a/h4/span[2]/text()")

        song = fm_tree.xpath(track_xpath)[0]
        tracklist.append(Track(srl, song))
    return tracklist


def _prepare_qs(string):
    url = string.replace(' \u2013 ', ' ')
    url = url.replace('+', '%2B')
    url = url.replace('?', '%3F')
    url = url.replace(' ', '+')
    url = url.replace('!', '')
    url = url.lower()
    url = url.split('(')[0]
    return url
