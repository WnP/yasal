#!/usr/bin/env python2
# -*- coding: utf8 -*-
from __future__ import unicode_literals
import sys
import os
import urllib2
import argparse
import ConfigParser
import traceback
from BeautifulSoup import BeautifulSoup


desktop_skeleton = '''[Desktop Entry]
Encoding=UTF-8
Icon={0}
Type=Link
Name={1}
URL={2}
[InternetShortcut]
URL={2}'''
config_parser = ConfigParser.RawConfigParser()


def check_fname(fname):
    return fname.endswith('.url')


def get_info(section, option):
    try:
        return config_parser.get(section, option)
    except Exception as e:
        if isinstance(e, (ConfigParser.NoOptionError, ConfigParser.NoSectionError)):
            return False


def get_title(url):
    ''' get title from given url '''
    res = urllib2.urlopen(url)
    html = res.read()
    soup = BeautifulSoup(html)
    return soup.html.head.title.contents[0]


def convert(fname, icon_flag):
    ''' convert a single file '''
    config_parser.read(fname)

    url = get_info('InternetShortcut', 'URL')
    if not url:
        print 'ERROR: url not found in: "{0}"'.format(fname)
        return

    title = get_title(url)

    desktop = desktop_skeleton.format(
        'text-html' if icon_flag else 'firefox',
        title,
        url)

    return desktop, title


def write(args, path, title, desktop):
    if args.out:
        out_name = os.path.join(args.out, ''.join((title, '.desktop')))
    else:
        out_name = os.path.join(path, ''.join((title, '.desktop')))

    if args.verbose:
        print out_name
    with open(out_name, 'wb') as f:
        f.write(desktop.encode('utf-8'))


def sanitize_args(args, parser):
    ''' Clean all input strings '''
    args.file = args.file if args.file is None else args.file.decode('utf-8')
    args.out = args.out if args.out is None else args.out.decode('utf-8')
    args.recursive = args.recursive if args.recursive is None else args.recursive.decode('utf-8')

    if args.out and not os.path.isdir(args.out):
        print 'ERROR: -o --out must point on a directory'
        parser.print_help()
        sys.exit(1)
    if args.recursive and not os.path.isdir(args.recursive):
        print 'ERROR: -r --recursive must point on a directory'
        parser.print_help()
        sys.exit(1)


def make_file(file_name, root_path, args):
    try:
        desktop, title = convert(file_name, args.icontexthtml)
        write(args, root_path, title, desktop)
    except Exception:
        if args.verbose:
            print '-' * 80
            print 'ERROR: file {file_name}:'.format(file_name=file_name)
            for l in traceback.format_exc().splitlines():
                print l
        else:
            print 'ERROR: file {file_name}: {error}'.format(
                file_name=file_name,
                error=traceback.format_exc().splitlines()[-1:][0],
            )


def do_recursive(args):
    for root, dirs, files in os.walk(args.recursive):
        if args.verbose:
            print '-' * 80
            print 'root: ', root
            print 'dirs: ', dirs
            print 'files: ', files
        for fname in files:
            if check_fname(fname):
                make_file(os.path.join(root, fname), root, args)


def main():
    # configure arguments
    parser = argparse.ArgumentParser(
        'yasal', description='''Yet Another Save As Link:
    Saves an internet link externally as a Windows Shortcut File (*.url) a UNIX Desktop file (*.desktop)
    .desktop file are named with the given url page title,
    the output file will be placed in the same folder if not specified''')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--file', help='specify file FILE to be convert')
    group.add_argument('-r', '--recursive', help='recursive mode, will convert all .url file in directory RECURSIVE')
    parser.add_argument('-o', '--out', help='specify output directory OUT for .desktop files')
    parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')
    parser.add_argument(
        '-i', '--icontexthtml',
        action="store_true",
        help="set the .desktop icon field to 'text-html' default is 'firefox'")

    try:
        args = parser.parse_args()
    except UnicodeDecodeError:
        # in case someone pass a filename without the flag
        parser.print_help()
        return

    # avoid UnicodeDecodeError
    sanitize_args(args, parser)

    # no arguments are mandatory but the programe does nothing if at least one is provided
    # so we'll print the help message
    if len(sys.argv) == 1:
        parser.print_help()

    # case for a unique file
    elif args.file:
        path, fname = os.path.split(args.file)

        if check_fname(fname):
            make_file(args.file, path, args)
        else:
            print 'ERROR: you must provide a .url file'
            sys.exit(1)

    # recursive case
    elif args.recursive:
        do_recursive(args)

    # this case should never happened
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
