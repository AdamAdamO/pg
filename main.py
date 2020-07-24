#!/usr/bin/python

import os
import urllib2

CACHE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "cache")

# Returns a list of (url, title) pairs
def feed():
    response = urllib2.urlopen("http://www.aaronsw.com/2002/feeds/pgessays.rss")
    rss = response.read()
    parts = rss.split("<item>")
    answer = []
    for part in parts:
        link = part.split("<link>")[1].split("</link>")[0]
        title = part.split("<title>")[1].split("</title>")[0]
        if not link or not title:
            continue
        if not link.endswith("html"):
            continue
        answer.append((link, title))
    return answer

# Hits the cache if possible
def download(url):
    slug = url.split("/")[-1]
    fname = os.path.join(CACHE, slug)
    if os.path.exists(fname):
        return open(fname).read()

    print("downloading", url)
    response = urllib2.urlopen(url)
    html = response.read()
    file = open(fname, "w")
    file.write(html)
    file.close()
    return html

def main():
    for url, title in feed():
        print("url:", url)
        print("title:", title)
        html = download(url)
        print(title, "is", len(html), "long")
    
if __name__ == "__main__":
    main()
    
