import sys
import urllib
import urllib2

from urllib2 import HTTPError, URLError

from conceptnet5_client.utils.debug import print_debug


def make_http_request(url):
    request = urllib2.Request(url)
    try:
        data = urllib2.urlopen(request)
    except HTTPError, e:
        print_debug('Error code: %s' % e.code, 'HTTPError')
        sys.exit()
    except URLError, e:
        print_debug('Reason: %s' % e.reason, 'URLError')
        sys.exit()
    return data
