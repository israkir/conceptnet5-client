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
        #usage = "conceptnet-make.py [-s] [projectname]", 
        #version = "conceptnet-make.py %s" % VERSION)
    return parser


def add_options(parser):
    parser.add_option(
        '-s', 
        '--startproject', 
        dest = 'projectname',
        default = 'myproject',
        help = 'creates a new conceptnet project with your custom settings.')
    return parser


def create_project_folder(projectname):
    try:
        #project_dir_path = '/'.join([os.getcwd(), projectname])
        project_dir_path = '/'.join([projectname])
        os.makedirs(project_dir_path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    return project_dir_path


def create_settings(path):
    pass 


def execute(parser, opts, args):
    print 'args: %s' % args
    print 'opts: %s' % opts
    #if len(args) < 2:
    #    parser.error('Incorrect number of arguments.')
    if opts.projectname:
        path = create_project_folder(opts.projectname)
        print 'project_dir_path: %s' % path
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
