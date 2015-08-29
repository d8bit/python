import sys
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup
import urllib2
import re
import requests

def getLinks(url, result, base):
    try:
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
    for link in links:
        if base in link.get('href') and link.get('href') not in result and link.get('href') != None:
            result.append(link.get('href'))
            result.extend(getLinks(link.get('href'), result, base))

    return result


if len(sys.argv) != 2:
    print 'File path needed'
    sys.exit(0)

url = sys.argv[1]
base = urlparse(url).netloc
pages = []
getLinks(url, pages, base)
