# -*- coding: utf-8 -*-
__author__ = 'modulus'

import json
import urllib2 as urllib
import re
from bs4 import BeautifulSoup
from Item import Item


#json aspi db: http://dbtv.no/?op=ContentTail&t=q&vid=jomfru%20i%20n%C3%B8d&inapp=


# __settings__ = xbmcaddon.Addon(id="plugin.video.dbtv")
# __language__ = __settings__.getLocalizedString

def createMainMenu(baseUrl, handle):
    """
    Reads channels from dagbladet.no. When done sends them to Xbmc
    This is the plugin main menu
    """
    soup = BeautifulSoup(urllib.urlopen('http://dbtv.no/'))
    # Finds the <div> tag containing all the channels
    channels = soup.find('div', attrs={'id':re.compile('series')})
    # Feed it back to BeautifulSoup to get the actual channels
    soup = BeautifulSoup(str(channels))
    # Each channel name is it's own link (<a></a>)
    channels = soup.findAll('a')

    listing = []
    for channel in channels:
        url = channel['href']
        # The channel "Huset" doesn't have a category ID, which means it will not be added.
        # TODO: Huset
        if len(url) > 1 and url != "#serier":
            cat_id = url
            listing.append(Item(title=channel.contents[0], url="http://dbtv.no{cat}".format(cat=str(cat_id))))
    return listing


def createSubMenu(baseUrl, title, handle, cat_id, offset="0"):
    text = urllib.urlopen("{baseUrl}?op=ContentTail&t=q&vid={search}&inapp=".format(baseUrl=baseUrl, search=title.encode('utf-8')))

    data = json.load(text)

    listing = []
    for element in data:
        viewed = element["playsTotal"]
        thumb = element["videoStillUrl"]
        date = element["publishedDate"]
        stream_url = element["thumbnailUrl"] #data["url"]
        duration = element["length"]
        title = element["name"]
        progid = element["id"]
        rating = None
        votes = None
        category = None
        stream_url = element["url"]
        if thumb:
            thumb = thumb[thumb.index("src=")+4:]

        listing.append(Item(progid=progid, title=title, duration=duration,
                            viewed=viewed, date=date, rating=rating, votes=votes, thumb=thumb,
                            category=category, url=stream_url, isPlayable=True))
    return listing
