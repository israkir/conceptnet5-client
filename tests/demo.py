from conceptnet5_client.utils.debug import print_debug
from conceptnet5_client.web.api import LookUp, Search, Association
from conceptnet5_client.utils.result import Result
from conceptnet5_client.inference.path import Path


def demonstrate_lookup(concept):
    print 'Demonstrating LookUp concept API'
    lookup = LookUp(offset=1, limit=1)
    data = lookup.search_concept(concept)
    r = Result(data)
    edges = r.parse_all_edges()
    for edge in edges:
        edge.print_edge()
        edge.print_all_attrs()
    print
    
    print 'Demonstrating LookUp concept API cleaning self referencing edges'
    lookup = LookUp(offset=1, limit=1)
    data = lookup.search_concept(concept)
    r = Result(data)
    r.print_raw_result()
    print


def demonstrate_source_lookup(source_uri):
    print 'Demonstrating LookUp source API'
    lookup = LookUp()
    data = lookup.search_source(source_uri)
    r = Result(data)
    r.print_raw_result()
    print


def demonstrate_search():
    print 'Demonstrating Search API'
    s = Search(rel='/c/en/be_often_compare_to')
    data = s.search()
    r = Result(data)
    r.print_raw_result()
    print
    
    s = Search(text='mariah carey', surfaceText='dion', something='anything')
    data = s.search()
    r = Result(data)
    r.print_raw_result()
    print


def demonstrate_association():
    print 'Demonstrating Association API'
    a = Association(filter='/c/en/dog', limit=1)
    data = a.get_similar_concepts('cat')
    r = Result(data)
    r.print_raw_result()
    print
    
    a = Association()
    data = a.get_similar_concepts_by_term_list(['toast', 'cereal', 'juice', 'egg'])
    r = Result(data)
    r.print_raw_result()
    print
    r.parse_all_edges()
    print


def demonstrate_inference():
    concepts = ['/c/en/cat', '/c/en/animal', '/c/en/living']
    relations = ['/r/IsA', '/r/HasProperty', '/r/HasProperty'] 
    p = Path(concepts, relations)
    #print p.does_exist(print_where_breaks=True)
    #for a in p.assertions:
    #    a.print_assertion()
    concepts_tuples = p.get_all_tuple_of_concepts()
    for concept_tuple in concepts_tuples:
        for index, elem in enumerate(concept_tuple):
            if index == len(relations):
                print '%s' % (elem), 
            else:
                print '%s -- %s -- ' % (elem, relations[index]), 
        print

    
def main():
    #demonstrate_lookup('see movie')
    #demonstrate_search()
    #demonstrate_association()
    #demonstrate_source_lookup('/s/contributor/omcs/rspeer')
    #demonstrate_source_lookup('/s/rule/sum_edges')
    #demonstrate_source_lookup('/s/wordnet/3.0')
    demonstrate_inference()


if __name__ == '__main__':
    main()
