import hashlib
import os

try: 
    import simplejson as json
except ImportError: 
    import json


CACHE_DIR = 'cached_data/'


def cache(func):
    '''
    When method/function is called, returns the cache if it exists;
    otherwise executes the method and cache results.

    Specific to make_http_request() function, because it uses 'url'
    argument to create the cache key.
    '''
    def _wrapper(*args, **kwargs):
        cache_key = hashlib.sha1(args[0]).hexdigest()
        
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)

        print 'Looking for cache: %s' % args[0]

        # Check the value is cached, if cached return cached content
        for path, dirs, files in os.walk(CACHE_DIR):
            for filename in files:
                if filename == cache_key:
                    print 'Cache found: %s' % args[0]
                    fullpath = os.path.join(CACHE_DIR, filename)
                    data = open(fullpath, 'r').read()
                    return json.loads(data)
        
        print 'Cache not found, making request: %s' % args[0]
        # Cache returned data of the caller function and finally return the data
        json_data = func(*args, **kwargs) 
        f = open(os.path.join(CACHE_DIR, cache_key), 'w')
        json.dump(json_data, f)
        f.close()
        return json_data
    return _wrapper
