from conceptnet5_client.utils.debug import print_debug
from conceptnet5_client.lookup import LookUp
from conceptnet5_client.search import Search
from conceptnet5_client.result import Result
from conceptnet5_client.association import Association

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
    edges = r.parse_all_edges(clean_self_ref = True)
    [edge.print_edge() for edge in edges]
    print


def demonstrate_source_lookup(source_uri):
    print 'Demonstrating LookUp source API'
    lookup = LookUp()
    data = lookup.search_source(source_uri)
    r = Result(data)
    r.print_raw_results()
    print


def demonstrate_search():
    print 'Demonstrating Search API'
    s = Search(rel='/c/en/be_often_compare_to')
    data = s.search()
    r = Result(data)
    r.print_raw_results()
    print
    
    s = Search(text='mariah carey', surfaceText='dion', something='anything')
    data = s.search()
    r = Result(data)
    r.print_raw_results()
    print


def demonstrate_association():
    print 'Demonstrating Association API'
    a = Association(filter='/c/en/dog', limit=1)
    data = a.get_similar_concepts('cat')
    r = Result(data)
    r.print_raw_results()
    print
    
    a = Association()
    data = a.get_similar_concepts_by_term_list(['toast', 'cereal', 'juice', 'egg'])
    r = Result(data)
    r.print_raw_results()
    print

def main():
    demonstrate_lookup('see movie')
    demonstrate_search()
    demonstrate_association()
    demonstrate_source_lookup('/s/contributor/omcs/rspeer')
    demonstrate_source_lookup('/s/rule/sum_edges')
    demonstrate_source_lookup('/s/wordnet/3.0')


if __name__ == '__main__':
    main()
