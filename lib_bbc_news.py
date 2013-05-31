"""
    BBC News Headlines
    ~~~~~~~~~~~~~~~~~~
    Support for reading and parsing the BBC RSS news and weather feeds
    dsmall 12 Jul 2012, 19 Apr 2013, 31 May 2013 
"""
from flask import Blueprint, render_template, request
public = Blueprint('lib_bbc_news', __name__, template_folder='templates')

from server import RASCAL, env, CONFIG_FILE
if env == RASCAL:
    import pytronics

import requests
import xml.etree.ElementTree as ET

def parseHeadlines(xmldata):
    """ Minimal RSS parser for items title, description, link and pubDate """
    root = ET.fromstring(xmldata)
    headlines = []
    count = 1
    channel = root.find('channel/title').text
    for item in root.findall('channel/item'):
        title = item.find('title').text
        description = item.find('description').text
        link = item.find('link').text
        pubDate = item.find('pubDate').text
        if title != '' and description != '' and link != '':
            dictItem = {}
            dictItem['title'] = title
            dictItem['description'] = description
            dictItem['link'] = link
            dictItem['pubDate'] = pubDate
            headlines.append(dictItem)
        if len(headlines) >= 20:
            break
        count += 1
    if len(headlines) == 0:
        headlines = [ { 'title': 'Not available' } ]
    return (channel, headlines)

def getFeed(url, etag = None, lastModified = None):
    """ Minimal RSS reader with support for etag and last-modified """
    if etag:
        headers = { 'If-None-Match': etag }
    elif lastModified:
        headers = { 'If-Modified-Since': lastModified }
    else:
        headers = { }
    r = requests.get(url, headers=headers)
    status = r.status_code
    if status == 200:
        tag = r.headers['etag'] if 'etag' in r.headers else '""'
        lastMod = r.headers['last-modified'] if 'last-modified' in r.headers else ''
        return { 'status': status, 'tag': tag, 'lastMod': lastMod, 'data': parseHeadlines(r.content) }
    else:
        return { 'status': status }

def logStatus(which, what, status):
    """ Log status in uwsgi public.log """
    if status == requests.codes.ok:
        desc = 'OK'
    elif status == requests.codes.not_modified:
        desc = 'Not Modified'
    else:
        desc = 'Server couldn\'t fulfill the request'
    print '## {0} ## {1} {2} {3}'.format(which, what, status, desc)

def getHeadlines(section, lastModified):
    """ Get BBC News headlines for specified section, cache control with last-modified  """
    sections = [ '', '/world', '/uk', '/world/us_and_canada',
        '/science_and_environment', '/technology', '/entertainment_and_arts',
        '/business', '/system/latest_published_content' ]
    url = 'http://feeds.bbci.co.uk/news' + sections[section] + '/rss.xml'
    feed = getFeed(url, lastModified = lastModified)
    logStatus('getHeadlines', sections[section], feed['status'])
    return feed

def getWeather(locationID, forecast, etag):
    """ Get BBC Weather for specified location, cache control with etag """
    forecasts = [ 'observations', '3dayforecast']
    url = 'http://open.live.bbc.co.uk/weather/feeds/en/{0}/{1}.rss'.format(locationID, forecasts[forecast])
    feed = getFeed(url, etag = etag)
    logStatus('getWeather', '{0} {1}'.format(locationID, forecasts[forecast]), feed['status'])
    return feed

def getLocationID():
    """ Get weather locationID from config file public.conf """
    import ConfigParser
    config = ConfigParser.SafeConfigParser()
    config.read(CONFIG_FILE)
    try:
        locationID = config.getint('Headlines', 'locationID')
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
        # Default is Rascal Micro home (Boston, USA)
        locationID = 4930956
    except Exception, e:
        print '## getLocationID ## Unexpected error: %s' % str(e)
        locationID = 4930956
    return locationID

# local globals
headlines = ('BBC News', [ { 'title': 'No news yet' } ])
headlinesTag = '""'
headlinesLastMod = ''
weather = ('BBC Weather', [ { 'title': 'No weather yet' } ])
weatherTag = '""'
weatherLastMod = ''
lastFeed = 0
lastForecast = 0
lastSlot = 20
lastUpdate = 'Not known'

@public.route('/headlines', methods=['POST'])
def headlines():
    global headlines, headlinesTag, headlinesLastMod, weather, weatherTag, weatherLastMod, lastFeed, lastForecast, lastSlot, lastUpdate
    import time, json
    try:
        feed = int(request.form['feed'])
    except KeyError:
        feed = 0
    try:
        forecast = int(request.form['forecast'])
    except KeyError:
        forecast = 0
    locationID = getLocationID()
    try:
        temp = pytronics.i2cRead(0x48, 0, 'I', 2)
        strTemp = '{0:0.1f}{1}C'.format(((temp[0] << 4) | (temp[1] >> 4)) * 0.0625, unichr(176))
    except:
        strTemp = ''
    try:
        now = time.localtime()
        # Update headlines every five minutes
        slot = now.tm_min / 5
        updated = False
        if feed != lastFeed or forecast != lastForecast or slot != lastSlot:
            try:
                if feed != lastFeed:
                    headlinesTag = '""'
                    headlinesLastMod = ''
                result = getHeadlines(feed, headlinesLastMod)
                if result['status'] == 200:
                    headlinesTag = result['tag']
                    headlinesLastMod = result['lastMod']
                    headlines = result['data']
                    lastUpdate = time.strftime('%H:%M %Z', now)
                    updated = True
            except Exception, e:
                print '## getHeadlines ## Unexpected error: %s' % str(e)
            try:
                result = getWeather(locationID, forecast, weatherTag)
                if result['status'] == 200:
                    weatherTag = result['tag']
                    weatherLastMod = result['lastMod']
                    weather = result['data']
                    if not updated:
                        lastUpdate = time.strftime('%H:%M %Z', now)
                        updated = True
            except Exception, e:
                print '## getWeather ## Unexpected error: %s' % str(e)
            lastFeed = feed
            lastForecast = forecast
            lastSlot = slot
        data = {
            'date' : time.strftime('%a, %d %b %Y %H:%M %Z', now),
            'temp' : strTemp,
            'headlines' : headlines,
            'weather' : weather,
            'updated' : updated,
            'lastUpdate' : lastUpdate
        }
        return json.dumps(data)
    except Exception, e:
        print '## headlines ## Unexpected error: %s' % str(e)
        return 'Bad request', 400
