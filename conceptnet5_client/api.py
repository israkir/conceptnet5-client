import sys
import urllib

from conceptnet5_client.utils.debug import print_debug
from conceptnet5_client.utils.http import make_http_request
from conceptnet5_client.utils.util import is_arg_valid


from conceptnet5_client.conf import settings


class LookUp:
    '''
    This class implements the methods for querying about a concept or sources.
    '''
    def __init__(self, lang = 'en', **kwargs):
        query_args = {}
        for key, value in kwargs.iteritems():
            if is_arg_valid(key, settings.SUPPORTED_LOOKUP_ARGS):
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
        url = ''.join(['%s/c/%s/%s?' % (settings.BASE_LOOKUP_URL, self.lang, concept)]) + self.encoded_query_args
        print_debug(url, 'url')
        json_data = make_http_request(url)
        return json_data


    def search_source(self, source_uri = None):
        '''
        Constructs the search url for this instance of lookup object with specified query args 
        and specified uri and finally returns the 50 statements submitted by this source.

        :param source_uri: a uri specifying the source, e.g. '/s/contributor/omcs/rspeer', 
        '/s/wordnet/3.0', '/s/rule/sum_edges' etc.
        '''
        if source_uri:
            url = ''.join(['%s%s' % (settings.BASE_LOOKUP_URL, source_uri)])
            print url
            json_data = make_http_request(url)
            return json_data
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
            if is_arg_valid(key, settings.SUPPORTED_SEARCH_ARGS):
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
        url = ''.join(['%s%s' % (settings.BASE_SEARCH_URL, '?')]) + self.encoded_query_args
        print_debug(url, 'url')
        json_data = make_http_request(url)
        return json_data

        

class Association:
    '''
    This class implements the methods for association and similarity of several concepts.
    '''
    def __init__(self, lang = 'en', **kwargs):
        query_args = {}
        for key, value in kwargs.iteritems():
            if is_arg_valid(key, settings.SUPPORTED_ASSOCIATION_ARGS):
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
        url = ''.join(['%s/c/%s/%s?' % (settings.BASE_ASSOCIATION_URL, self.lang, concept)]) + self.encoded_query_args
        print_debug(url, 'url')
        json_data = make_http_request(url)
        return json_data


    def get_similar_concepts_by_term_list(self, term_list):
        '''
        Returns the similar concepts with similarity scores for this term_list in json format.

        :param term_list: a list of concepts.
        '''
        terms = ','.join(term_list)
        url = ''.join(['%s/list/%s/%s' % (settings.BASE_ASSOCIATION_URL, self.lang, terms)]) + self.encoded_query_args
        print_debug(url, 'url')
        json_data = make_http_request(url)
        return json_data


