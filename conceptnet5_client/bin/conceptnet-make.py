#!/usr/bin/python

import os
import errno

from optparse import OptionParser


VERSION = '0.1'


def print_info(parser):
    print 'Required option is missing.'
    parser.print_help()
    exit(-1)


def init_parser():
    parser = OptionParser()
    return parser


def add_options(parser):
    parser.add_option(
        '-s', 
        '--startproject', 
        dest = 'projectname',
        default = 'myproject',
        help = 'Creates a new ConceptNet project.')
    return parser


def create_project_folder(projectname):
    try:
        os.makedirs(projectname)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    return projectname


def create_settings(path):
    pass 


def execute(parser, opts, args):
    print 'args: %s' % args
    print 'opts: %s' % opts
    
    if opts.projectname:
        path = create_project_folder(opts.projectname)
        create_settings(path)
    else:
        print_info(parser)


def main():
    parser = init_parser()
    parser = add_options(parser)
    opts, args = parser.parse_args()
    execute(parser, opts, args)


if __name__ == '__main__':
    main()
