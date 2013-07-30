# These URLs basically points to MIT's conceptnet5 setup for Web API
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
