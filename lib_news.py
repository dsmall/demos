"""
    BBC News Headlines
    ~~~~~~~~~~~~~~~~~~
    Support for reading and parsing the BBC RSS news feed
    dsmall 19 Apr 2013 
"""
from flask import Blueprint, render_template, request
public = Blueprint('lib_news', __name__, template_folder='templates')

import httplib
import xml.dom.minidom

from server import RASCAL, env
if env == RASCAL:
    import pytronics
    
debug = False

def _getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def getHeadlines(feed):
    feeds = [ '', '/world', '/uk', '/world/us_and_canada',
        '/science_and_environment', '/technology', '/entertainment_and_arts',
        '/business', '/system/latest_published_content' ]
    conn = httplib.HTTPConnection('feeds.bbci.co.uk')
    conn.request("GET", "/news" + feeds[feed] + "/rss.xml")
    r1 = conn.getresponse()
    print '## getHeadlines ## {0} {1} {2}'.format(feeds[feed], r1.status, r1.reason)
    data1 = r1.read()
    conn.close()
    dom = xml.dom.minidom.parseString(data1)
    items = dom.getElementsByTagName("item")
    headlines = []
    count = 1
    for item in items:
        title = item.getElementsByTagName("title")[0]
        try:
            strTitle = _getText(title.childNodes)
        except:
            strTitle = ''
        description = item.getElementsByTagName("description")[0]
        try:
            strDescription = _getText(description.childNodes)
        except:
            strDescription = ''
        link = item.getElementsByTagName("link")[0]
        try:
            strLink = _getText(link.childNodes)
        except:
            strLink = ''
        pubDate = item.getElementsByTagName("pubDate")[0]
        try:
            strPubDate = _getText(pubDate.childNodes)
        except:
            strPubDate = ''
        if strTitle != '' and strDescription != '' and strLink != '':
            dictItem = {}
            dictItem['title'] = strTitle
            dictItem['description'] = strDescription
            dictItem['link'] = strLink
            dictItem['pubDate'] = strPubDate
            headlines.append(dictItem)
        if len(headlines) >= 15:
            break
        count += 1
        if count >= 20:
            headlines = [ { 'title' : 'News not available' } ]
            break
    return headlines

if debug:
    for headline in getHeadlines(0):
        print headline

# local globals
headlines = [ { 'title' : 'No news yet' } ]
lastFeed = 0
lastSlot = 20
lastUpdate = 'Not known'

@public.route('/headlines', methods=['POST'])
def headlines():
    global headlines, lastFeed, lastSlot, lastUpdate
    import time, json
    try:
        feed = int(request.form['feed'])
    except KeyError:
        feed = 0
    try:
        temp = pytronics.i2cRead(0x48, 0, 'I', 2)
        strTemp = '{0:0.1f}{1}C'.format(((temp[0] << 4) | (temp[1] >> 4)) * 0.0625, unichr(176))
    except:
        strTemp = ''
    now = time.localtime()
    # Update headlines every five minutes
    slot = now.tm_min / 5
    if feed != lastFeed or slot != lastSlot:
        headlines = getHeadlines(feed)
        lastFeed = feed
        lastSlot = slot
        lastUpdate = time.strftime('%H:%M %Z', now)
        updated = True
    else:
        updated = False
    data = {
        'date' : time.strftime('%a, %d %b %Y %H:%M %Z', now),
        'temp' : strTemp,
        'headlines' : headlines,
        'updated' : updated,
        'lastUpdate' : lastUpdate
    }
    return json.dumps(data)
