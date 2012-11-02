def is_arg_valid(arg, arg_list):
    '''
    Check whether the passed argument during init is supported
    by ConceptNet5 API or not.
    '''
    return arg in arg_list
