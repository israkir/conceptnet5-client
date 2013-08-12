from conceptnet5_client.web.api import Search
from conceptnet5_client.utils.util import pairwise
from conceptnet5_client.utils.result import Result


class Path:
    '''
    This class implements the methods for creating a single graph walk on ConceptNet5.
    '''
    def __init__(self, concepts = [], relations = []):
        self.concepts = concepts
        self.relations = relations


    def does_exist(self, print_where_breaks=False):
        '''
        Checks whether this path exists in ConceptNet5.

        :param print_where_breaks: prints the assertion, if the assertion does not exist in the path.
        '''
        for concept1, concept2 in pairwise(self.concepts):
            for relation in self.relations:
                search = Search(start=concept1, rel=relation, end=concept2)
                data = search.search()
                result = Result(data)
                if result.get_num_found() == 0:
                    if print_where_breaks == True:
                        print 'This assertion breaks the path: (%s --> %s --> %s)' % (
                            concept1, relation, concept2)
                    return False
        return True
