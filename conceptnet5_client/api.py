import sys
import urllib

from conceptnet5_client.utils.debug import print_debug
from conceptnet5_client.utils.http import make_http_request

try: 
    import simplejson as json
except ImportError: 
    import json

    

BASE_LOOKUP_URL = 'http://conceptnet5.media.mit.edu/data/5.1'
BASE_SEARCH_URL = 'http://conceptnet5.media.mit.edu/data/5.1/search'
BASE_ASSOCIATION_URL = 'http://conceptnet5.media.mit.edu/data/5.1/assoc'

# This is the supported query arguments for LookUp API
# :param offset: skip the specified amount of first results
# :type offset: integer
# :param limit: change the number of results from the default of 50
# :type limit: integer
# :param filter: If 'core', only get edges from the ConceptNet 5 Core (not from ShareAlike resources),
#                if 'core-assetions', search for edges by default, and there can be many edges 
#                representing the same assertion.
# :type filter: Either 'core' or 'core-assertions'
SUPPORTED_LOOKUP_ARGS = ['offset', 'filter', 'limit']


# This is the supported query arguments for Association API
# :param limit: change the number of results from the default of 50
# :type limit: integer
# :param filter: return only results that start with the given URI. For example, 
#                filter=/c/en returns results in English.
# :type filter: a uri, e.g. '/c/en/cat' (Different than lookup API!)
SUPPORTED_ASSOCIATION_ARGS = ['limit', 'filter']


# Supported arguments for Search API
# :param {id, uri, rel, start, end, context, dataset, license}: giving a ConceptNet URI for any of these 
#       parameters will return edges whose corresponding fields start with the given path
# :type {id, uri, rel, start, end, context, dataset, license}: uri
# :param nodes: returns edges whose rel, start, or end start with the given URI
# :type nodes: uri
# :param {startLemmas, endLemmas, relLemmas}: returns edges containing the given lemmatized word anywhere 
#       in their start, end, or rel respectively
# :type {startLemmas, endLemmas, relLemmas}: word
# :param text: matches any of startLemmas, endLemmas, or relLemmas 
# :type text: word
# :param surfaceText: matches edges with the given word in their surface text. The word is not lemmatized, 
#       but it is a case-insensitive match
# :type surfaceText: word
# :param minWeight: filters for edges whose weight is at least weight
# :type minWeight: float
# :param limit: change the number of results from the default of 50
# :type limit: integer
# :param offset: skip the specified amount of first results
# :type offset: integer 
# :param features: Takes in a feature string (an assertion with one open slot), and returns edges having 
#       exactly that string as one of their features
# :type features: string of uri
# :param filter: If 'core', only get edges from the ConceptNet 5 Core (not from ShareAlike resources),
#       if 'core-assetions', search for edges by default, and there can be many edges representing the same assertion.
# :type filter: Either 'core' or 'core-assertions'
SUPPORTED_SEARCH_ARGS = ['id', 'uri', 'rel', 'start', 'end', 'context', 'dataset', 
    'license', 'nodes', 'startLemmas', 'endLemmas', 'relLemmas', 'text',
    'surfaceText', 'minWeight', 'limit', 'offset', 'features', 'filter']

    

def is_arg_valid(arg, arg_list):
    '''
    Check whether the passed argument during init is supported
    by ConceptNet5 API or not.
    '''
    return arg in arg_list
    
    
    
class LookUp:
    '''
    This class implements the methods for querying about a concept or sources.
    '''
    def __init__(self, lang = 'en', **kwargs):
        query_args = {}
        for key, value in kwargs.iteritems():
            if is_arg_valid(key, SUPPORTED_LOOKUP_ARGS):
                query_args[key] = value
                # print_debug('%s : %s' % (key, value), 'arg')
            else:
                print_debug('%s : %s -- THIS ARG IS NOT SUPPORTED!' % (key, value), 'ArgError')
        self.encoded_query_args = urllib.urlencode(query_args)
        self.lang = lang
    
    
    def search_concept(self, concept):
        '''
        Constructs the search url for this instance of lookup object with specified query args 
        and specified concept and finally returns the result of the request in json format.

        :param concept: a concept word or phrase, e.g. 'toast', 'see movie' etc.
        '''
        concept = concept.replace(' ', '_')
        url = ''.join(['%s/c/%s/%s?' % (BASE_LOOKUP_URL, self.lang, concept)]) + self.encoded_query_args
        print_debug(url, 'url')
        data = make_http_request(url)
        return json.load(data)


    def search_source(self, source_uri = None):
        '''
        Constructs the search url for this instance of lookup object with specified query args 
        and specified uri and finally returns the 50 statements submitted by this source.

        :param source_uri: a uri specifying the source, e.g. '/s/contributor/omcs/rspeer', 
        '/s/wordnet/3.0', '/s/rule/sum_edges' etc.
        '''
        if source_uri:
            url = ''.join(['%s%s' % (BASE_LOOKUP_URL, source_uri)])
            print url
            data = make_http_request(url)
            return json.load(data)
        else:
            print_debug('You should pass argument \'source\'.', 'ArgError')
            sys.exit()


            
class Search:
    '''
    This class implements methods for more sophisticated query options.
    '''
    def __init__(self, **kwargs):
        query_args = {}
        for key, value in kwargs.iteritems():
            if is_arg_valid(key, SUPPORTED_SEARCH_ARGS):
                query_args[key] = value
                # print_debug('%s : %s' % (key, value), 'arg')
            else:
                print_debug('%s : %s -- THIS ARG IS NOT SUPPORTED!' % (key, value), 'ArgError')
        self.encoded_query_args = urllib.urlencode(query_args)
        
        
    def search(self):
        '''
        Constructs the search url for this instance of search object with specified query args 
        and returns the result of the request in json format.
        '''
        url = ''.join(['%s%s' % (BASE_SEARCH_URL, '?')]) + self.encoded_query_args
        print_debug(url, 'url')
        data = make_http_request(url)
        return json.load(data)

        

class Association:
    '''
    This class implements the methods for association and similarity of several concepts.
    '''
    def __init__(self, lang = 'en', **kwargs):
        query_args = {}
        for key, value in kwargs.iteritems():
            if is_arg_valid(key, SUPPORTED_ASSOCIATION_ARGS):
                query_args[key] = value
                # print_debug('%s : %s' % (key, value), 'arg')
            else:
                print_debug('%s : %s -- THIS ARG IS NOT SUPPORTED!' % (key, value), 'ArgError')
        self.encoded_query_args = urllib.urlencode(query_args)
        self.lang = lang


    def get_similar_concepts(self, concept):
        '''
        Returns the similar concepts with similarity scores for this passed 'concept' in json format.

        :param concept: a concept word or phrase, e.g. 'toast', 'see movie' etc.
        '''
        url = ''.join(['%s/c/%s/%s?' % (BASE_ASSOCIATION_URL, self.lang, concept)]) + self.encoded_query_args
        print_debug(url, 'url')
        data = make_http_request(url)
        return json.load(data)


    def get_similar_concepts_by_term_list(self, term_list):
        '''
        Returns the similar concepts with similarity scores for this term_list in json format.

        :param term_list: a list of concepts.
        '''
        terms = ','.join(term_list)
        url = ''.join(['%s/list/%s/%s' % (BASE_ASSOCIATION_URL, self.lang, terms)]) + self.encoded_query_args
        print_debug(url, 'url')
        data = make_http_request(url)
        return json.load(data)