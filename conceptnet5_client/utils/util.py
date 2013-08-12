from itertools import tee, izip

def is_arg_valid(arg, arg_list):
    '''
    Check whether the passed argument during init is supported
    by ConceptNet5 API or not.
    '''
    return arg in arg_list


def pairwise(iterable):
    '''
    Creates a pairwise tuple of the iterable object.
    For example, for the list [1, 2, 3, 4], it will return (1, 2), (2, 3), (3, 4).
    '''
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)
