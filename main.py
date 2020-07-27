#!/usr/bin/python

import os
import urllib2

CACHE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "cache")
KEYWORDS = ["same way", "same reason"]
SKIP = ["behaved the same way people did at the time",
        "flout school rules in the same way",
        "say something exactly the same way"]
RADIUS = 2

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

# Splits html up into a list of sentences. Buggy
def sentences(html):
    for junk in ["\n", "<br>", "<i>", "</i>"]:
        html = html.replace(junk, " ")
    parts = html.split(".")[:-1]
    return [part.strip() + "." for part in parts]

def windows(alist, length):
    answer = []
    for i in range(len(alist)):
        window = alist[i:i+length]
        if len(window) != length:
            break
        answer.append(window)
    return answer

def window_grep(parts):
    wins = windows(parts, 2 * RADIUS + 1)
    answer = []
    for win in wins:
        match = any(win[RADIUS].count(key) for key in KEYWORDS)
        if not match:
            continue
        if any(win[RADIUS].count(skip) for skip in SKIP):
            continue
        answer.append(win)
    return answer

# Generates markdown
def main():
    for url, title in feed():
        html = download(url)
        wins = window_grep(sentences(html))
        if not wins:
            continue
        print("## [" + title + "](" + url + ")")
        print("")
        for win in wins:
            for i, sentence in enumerate(win):
                if i == RADIUS:
                    sentence = "**" + sentence + "**"
                print(sentence)
            print("")
    
if __name__ == "__main__":
    main()
    
