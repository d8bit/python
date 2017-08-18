import sys
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup
import urllib2
import re
import requests

def isSocialLink(url):
    socialUrls = ['facebook', 'twitter']
    for socialUrl in socialUrls:
        if socialUrl in url:
            return True

def isMailLink(url):
    return 'mailto' in url.lower()

def isImageLink(url):
    # check extensions
    extensions = ['jpeg', 'jpg', 'png']
    urlArray = url.split('.')
    count = len(urlArray)
    return urlArray[count -1] not in extensions

def isValidLink(url):
    if not isSocialLink(url) and not isMailLink(url) and not isImageLink(url):
        return True
    return False


def getLinks(url, result, base):
    if isValidLink(url):
        return result
    try:
        # get page
        html_page = urllib2.urlopen(url)
        print url
    except urllib2.HTTPError:
        print 'Error on ',url
        return result
    except urllib2.URLError:
        print 'Error on ',url
        return result
    except ValueError:
        print 'Error on ',url
        return result
    except AttributeError:
        print 'Error on ',url
        return result

    soup = BeautifulSoup(html_page)
    links = soup.findAll('a')
    # foreach link in page
    for link in links:
        if '#' in link.get('href'):
            print "Found '#' on ", url, '(',link.get('href'),')'
        if base in link.get('href') and link.get('href') not in result and link.get('href') != None:
            result.append(link.get('href'))
            result.extend(getLinks(link.get('href'), result, base))

    return result

# Expecting URL as parameter
if len(sys.argv) != 2:
    print 'File path needed'
    sys.exit(0)

url = sys.argv[1]
base = urlparse(url).netloc
baseArray = base.split('.')
if 3 == len(baseArray):
    base = ''.join((baseArray[1], '.', baseArray[2]))

pages = []
getLinks(url, pages, base)
