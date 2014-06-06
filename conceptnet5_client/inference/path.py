import copy
import networkx as nx

from conceptnet5_client.web.api import Search
from conceptnet5_client.utils.util import pairwise
from conceptnet5_client.utils.result import Result, Assertion
    

class Path:
    '''
    This class implements the methods for creating a single graph walk on ConceptNet5.
    '''
    def __init__(self, concepts = [], relations = []):
        self.concepts = concepts
        self.relations = relations
        self.assertions = self._create_assertions() if len(concepts) > 0 and len(relations) == len(concepts)-1 else None


    def _create_assertions(self):
        assertions = []
        for index, concepts in enumerate(pairwise(self.concepts)):
            assertion = Assertion(start=concepts[0], relation=self.relations[index], end=concepts[1])
            assertions.append(assertion)
        return assertions


    def get_all_tuples_of_concepts(self):
        '''
        Returns list of tuples of concepts connected by 'self.relations' sequence in the path.
        '''
        graph = nx.DiGraph()

        for relation in self.relations:
            search = Search(rel=relation, limit=1000)
            data = search.search()
            result = Result(data)
            edges = result.parse_all_edges()
            for e in edges:
                graph.add_node(e.start)
                graph.add_node(e.end)
                graph.add_edge(e.start, e.end)
                graph[e.start][e.end]['relation'] = relation
        
        concepts_tuples = []
        
        for index, r in enumerate(self.relations):
            for edge in graph.edges(data=True):
                start = edge[0]
                end = edge[1]
                relation = edge[2]['relation']
                
                if relation == r:
                    if index == 0:
                        concept_tuple = [start, end]
                        concepts_tuples.append(concept_tuple)
                    else:
                        for concept_tuple in concepts_tuples:
                            if len(concept_tuple) == index+1:
                                concepts_tuples.remove(concept_tuple)
                                next_candidates = []
                                for next_edge in graph.edges(data=True):
                                    next_edge_start = next_edge[0]
                                    next_edge_end = next_edge[1]
                                    next_edge_relation = next_edge[2]['relation']
                                    if next_edge_relation == r and concept_tuple[-1] == next_edge_start:
                                        next_candidates.append(next_edge_end)
                                for candidate in next_candidates:
                                    concept_tuple_copy = copy.deepcopy(concept_tuple)
                                    concept_tuple_copy.append(candidate)
                                    concepts_tuples.append(concept_tuple_copy)
    
        return concepts_tuples

    
    def get_all_tuples_of_relations(self):
        '''
        Returns list of tuples of relations which connects 'self.concepts' sequence in the path.
        '''
        relations_tuples = []
        
        for index, (concept1, concept2) in enumerate(pairwise(self.concepts)):
            search = Search(start=concept1, end=concept2)
            data = search.search()
            result = Result(data)
            if result.get_num_found() > 0:
                edges = result.parse_all_edges()
                if index == 0:
                    for e in edges:
                        if not [e.rel] in relations_tuples:
                            relations_tuples.append([e.rel])
                else:
                    for relation_tuple in relations_tuples:
                        if len(relation_tuple) == index:
                            for e in edges:
                                relation_tuple_copy = copy.deepcopy(relation_tuple)
                                relation_tuple_copy.append(e.rel)
                                if not relation_tuple_copy in relations_tuples:
                                    relations_tuples.append(relation_tuple_copy)
                            
        for relation_tuple in relations_tuples:
            if len(relation_tuple) != len(self.concepts)-1:
                relations_tuples.remove(relation_tuple)

        return relations_tuples


    def does_exist(self, print_where_breaks=False):
        '''
        Checks whether this path exists in ConceptNet5.

        :param print_where_breaks: prints the assertion, if the assertion does not exist in the path.
        '''
        for assertion in self.assertions:
            search = Search(start=assertion.start, rel=assertion.relation, end=assertion.end, limit=1000)
            data = search.search()
            result = Result(data)
            if result.get_num_found() == 0:
                if print_where_breaks == True:
                    print 'Assertion breaking the path: [ %s --> (%s) --> %s) ]' % (
                        assertion.start, assertion.relation, assertion.end)
                return False
        return True


    def print_path(self):
        print 'Path instance: ',
        print '[ %s ' % self.concepts[0],  
        for index, concept in enumerate(self.concepts[1:]):
            print '--> (%s) --> %s' % (self.relations[index], concept),
        print ']'
