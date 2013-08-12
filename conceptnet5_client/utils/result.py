import ast

from conceptnet5_client.utils.debug import print_debug
from conceptnet5_client.utils.util import is_arg_valid

try: 
    import simplejson as json
except ImportError: 
    import json


# These are the primary keys returned by a query
SUPPORTED_KEYS = ['numFound', 'maxScore', 'edges', 'terms', 'similar']


class Result:
    '''
    This class implements the necessary methods for parsing a query result.
    '''
    def __init__(self, json_data):
        result = {}
        for key, value in json_data.items():
            if is_arg_valid(key, SUPPORTED_KEYS):
                result[key] = value
                # print_debug('%s : %s' % (key, value), 'arg')
            else:
                print_debug('%s : %s -- THIS KEY IS NOT SUPPORTED!' % (key, value), 'KeyError')
        self.result = result


    def print_raw_result(self):
        '''
        Prints the result of the query in key = value manner without any processing.
        '''
        for key, value in self.result.iteritems():
            print_debug('%s = %s' % (key, value))


    def get_num_found(self):
        '''
        Returns the number of edges returned in query result.
        '''
        return self.result['numFound']


    def parse_all_edges(self, clean_self_ref = False):
        '''
        Parses the edges for this result object, initiates an edge object for each
        and returns list of these edge objects.

        :param clean_self_ref: If it is set, the self referencing edges with any kind of 
        relation, such as '/c/en/see_movie /r/Causes/ /c/en/see_move', will not be included
        in the returned list.
        '''
        edges = []
        
        if not 'edges' in self.result:
            print_debug('This result does not have any edge! Printing raw result...', 'ResultTypeError')
            self.print_raw_result()
            return
        
        for edge_str in self.result['edges']:
            e = Edge(edge_str)
            if clean_self_ref:
                if e.start != e.end:
                    edges.append(e)
            else:
                edges.append(e)
        return edges


        
class Edge:
    '''
    This class implements the methods for representing a single edge and manipulating it.
    '''
    def __init__(self, edge_str):
        edge_dict = ast.literal_eval(str(edge_str))
        self.start = edge_dict['start']
        self.start_lemmas = edge_dict['startLemmas']
        self.rel = edge_dict['rel']
        self.end = edge_dict['end']
        self.end_lemmas = edge_dict['endLemmas']
        self.weight = edge_dict['weight']
        self.score = edge_dict['score']
        self.uri = edge_dict['uri']
        self.nodes = edge_dict['nodes']
        self.text = edge_dict['text']
        self.features = edge_dict['features']
        self.sources = edge_dict['sources']
        self.context = edge_dict['context']
        self.dataset = edge_dict['dataset']
        self.timestamp = edge_dict['timestamp']
        self.license = edge_dict['license']
        self.id = edge_dict['id']

    
    def print_assertion(self):
        '''
        Prints the lemmas of this edge with start, rel, end lemmas.
        '''
        print_debug('%s %s %s' % (self.start_lemmas, self.rel, self.end_lemmas))

    
    def print_edge(self):
        '''
        Prints the normalized edge data with start node, rel, end node.
        '''
        print_debug('%s %s %s' % (self.start, self.rel, self.end))

    
    def print_all_attrs(self):
        '''
        Prints all attributes regarding to this edge.
        '''
        attrs = vars(self)
        print_debug('\n'.join('%s: %s' % item for item in attrs.items()))
