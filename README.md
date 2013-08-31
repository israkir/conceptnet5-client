Description
===========

This is a Python programming interface and an inference engine for [ConceptNet5 Web API](http://conceptnet5.media.mit.edu/). It supports investigating multiple concept relationships as a graph walk. 

The general documentation about ConceptNet5 project can be found in [here](https://github.com/commonsense/conceptnet5/wiki).


Dependencies
============

* `networkx` package (>=1.7) in order to manipulate query results using graph functions.

Instructions
============
Install:
    
    $ sudo python setup.py install

Create project:

    $ conceptnet-make.py
    
Command above will create a new folder 'myproject' under your current directory. In order to specify a project path/name, run:

    $ conceptnet-make.py -s /home/user/conceptnet_project

Web API
=======

There are 3 types of main API in ConceptNet which are supported by this package.


LookUp API
----------

This allows you to query for general facts about a concept. There are 3 arguments supported while initialization:

    # :param offset: skip the specified amount of first results
    # :type offset: integer
    # :param limit: change the number of results from the default of 50
    # :type limit: integer
    # :param filter: If 'core', only get edges from the ConceptNet 5 Core (not from ShareAlike resources), if 'core-assetions', search for edges by default, and there can be many edges representing the same assertion.
    # :type filter: Either 'core' or 'core-assertions'


Basic usage as follows:

    # get general facts about 'see movie'
    lookup = LookUp(limit=1)
    response = lookup.search_concept('see movie')
    
    # parse the response
    r = Result(response)
    edges = r.parse_all_edges(clean_self_ref = True) # this is a list of Edge objects
    [edge.print_edge() for edge in edges]
    # in order to print all attributes of edges
    [edge.print_all_attrs() for edge in edges]


Also, you can query for the concepts of a specific contibutor or source:

    lookup = LookUp()
    response1 = lookup.search_source('/s/wordnet/3.0')
    r1 = Result(response1)
    # print results in key = value format 
    r1.print_raw_results()
    
    response2 = lookup.search_source('/s/rule/sum_edges')
    r2 = Result(response2)
    # print results in key = value format 
    r2.print_raw_results()

Search API
----------

This allows more sophisticated queries regarding to any aspects of an assertion in ConceptNet database. Supported args:

    # :param {id, uri, rel, start, end, context, dataset, license}: giving a ConceptNet URI for any of these parameters will return edges whose corresponding fields start with the given path
    # :type {id, uri, rel, start, end, context, dataset, license}: uri
    # :param nodes: returns edges whose rel, start, or end start with the given URI
    # :type nodes: uri
    # :param {startLemmas, endLemmas, relLemmas}: returns edges containing the given lemmatized word anywhere in their start, end, or rel respectively
    # :type {startLemmas, endLemmas, relLemmas}: word
    # :param text: matches any of startLemmas, endLemmas, or relLemmas 
    # :type text: word
    # :param surfaceText: matches edges with the given word in their surface text. The word is not lemmatized, but it is a case-insensitive match
    # :type surfaceText: word
    # :param minWeight: filters for edges whose weight is at least weight
    # :type minWeight: float
    # :param limit: change the number of results from the default of 50
    # :type limit: integer
    # :param offset: skip the specified amount of first results
    # :type offset: integer 
    # :param features: Takes in a feature string (an assertion with one open slot), and returns edges having exactly that string as one of their features
    # :type features: string of uri
    # :param filter: If 'core', only get edges from the ConceptNet 5 Core (not from ShareAlike resources), if 'core-assetions', search for edges by default, and there can be many edges representing the same assertion.
    # :type filter: Either 'core' or 'core-assertions'


Basic usage:
   
    # Search for the edges whose relation is 'be often compared to'
    s = Search(rel='/c/en/be_often_compare_to')
    data = s.search()
    r = Result(data)
    # print results in key = value format 
    r.print_raw_results()
    
    # Search for any edge whose any of 'startLemmas', 'endLemmas' or 'relLemmas' matches 
    # 'mariah carey' and whose 'surfaceText' matches 'dion'. Here the arg'something' is 
    # not supported, so it will be ignored constructing query URL.
    s = Search(text='mariah carey', surfaceText='dion', something='anything')
    data = s.search()
    r = Result(data)
    # print results in key = value format 
    r.print_raw_results()

Association API
---------------

This allows to retrieve the similarity between two concepts or to retrieve list of concepts which are similar to several concepts.

Supported arguments:

    # :param limit: change the number of results from the default of 50
    # :type limit: integer
    # :param filter: return only results that start with the given URI. For example, filter=/c/en returns results in English.
    # :type filter: a uri, e.g. '/c/en/cat' (Different than lookup API!)


Basic usage:

    # get how similar cats and dogs 
    a = Association(filter='/c/en/dog', limit=1)
    data = a.get_similar_concepts('cat')
    r = Result(data)
    # print results in key = value format 
    r.print_raw_results()
    
    a = Association()
    data = a.get_similar_concepts_by_term_list(['toast', 'cereal', 'juice', 'egg'])
    r = Result(data)
    # print results in key = value format 
    r.print_raw_results()


Parsing response with `Result` class
----------------------------------

Two methods are supported at this moment:

1. `print_raw_results(self)`: Prints the results in key = value manner. Since only 'numFound, maxScore' and 'edges' are returned most of the time, so the keys will be those.

2. `parse_all_edges(self, clean_self_ref)`: Parses the edges for this result object, initiates an edge object for each and returns list of these edge objects. If `clean_self_ref` is set, the self referencing edges with any kind of relation, such as '/c/en/see_movie /r/Causes/ /c/en/see_move', will not be included in the returned list.
