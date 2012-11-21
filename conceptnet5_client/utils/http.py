import sys
import urllib
import urllib2

try: 
    import simplejson as json
except ImportError: 
    import json

from urllib2 import HTTPError, URLError

from conceptnet5_client.utils.debug import print_debug
from conceptnet5_client.cache.file_cache import cache


@cache
def make_http_request(url):
    '''
    Makes and http request to the 'url', if response to that
    'url' is not cached yet.

    Returns the response in json format.
    '''
    request = urllib2.Request(url)
    try:
        data = urllib2.urlopen(request)
    except HTTPError, e:
        print_debug('Error code: %s' % e.code, 'HTTPError')
        sys.exit()
    except URLError, e:
        print_debug('Reason: %s' % e.reason, 'URLError')
        sys.exit()
    return json.load(data)
