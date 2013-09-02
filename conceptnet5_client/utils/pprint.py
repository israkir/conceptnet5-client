# Based on: http://ginstrom.com/scribbles/2007/09/04/pretty-printing-a-table-in-python/

import sys

reload(sys)
sys.setdefaultencoding("UTF-8")


def format_num(num):
    '''
    Format a number according to given places.
    Adds commas, etc. Will truncate floats into ints!
    '''
    try:
        inum = int(num)
        return locale.format("%.*f", (0, inum), True)

    except (ValueError, TypeError):
        return str(num)


def get_max_width(table, index):
    '''
    Get the maximum width of the given column index.
    '''
    return max([len(format_num(row[index])) for row in table])


def pprint_paths(out, paths, relations=None):
    '''
    Prints out 'paths'
    @param out: Output stream (file-like object)
    @param paths: A list of lists.
    Each row must have the same number of columns.
    '''
    col_paddings = []
    
    for i in range(len(paths[0])):
        col_paddings.append(get_max_width(paths, i))

    length = 0
    for col_padding in col_paddings:
        length += col_padding + 3
    
    print >> out, '=' * length

    for row in paths:
        # left col
        print >> out, row[0].ljust(col_paddings[0] + 1), 
        
        # rest of the cols
        for i in range(1, len(row)):
            col = format_num(row[i]).rjust(col_paddings[i] + 2)
            print >> out, col,
                
        print >> out

    print >> out, '=' * length
