#!/usr/local/bin/python3
from ast import arg
from distutils import cmd
import structlog
import argparse
import time
from fabric import ThreadingGroup as Group
from getpass import getpass

log = structlog.get_logger()


def parse_arguments():
    parser = argparse.ArgumentParser(description='Execute command via SSH')
    parser.add_argument('-n', '--host_names',  nargs='+', required=True)
    parser.add_argument('-u', '--username', required=True)
    parser.add_argument('-k', '--key_file')
    parser.add_argument('-p', '--ask_pass', action='store_true')
    parser.add_argument('-c', '--cmd', nargs='*', required=True)
    # the below is a better way to store cmd separated by ### this is not used to keep the code simple
    # parser.add_argument('-c', '--cmd', nargs='*', type=lambda s: [i for i in s.split('###')],
    #                     dest="scanLibrary")
    return parser.parse_args()


def validate_arguments(args):
    if not args.ask_pass and args.key_file == None:
        log.fatal("you must provide key file or password",
                  ask_pass=args.ask_pass, key=args.key_file)
    if args.ask_pass and args.key_file != None:
        log.fatal("provide key file or password not both",
                  ask_pass=args.ask_pass, key=args.key_file)


def transform_arguments(args):
    args.host_names = args.host_names[0].split(",")
    args.cmd = args.cmd[0].split("###")
    if args.ask_pass:
        args.password = getpass()


def get_connect_cfg(args):
    if args.ask_pass:
        return {
            "password": args.password,
        }
    return {
        "key_filename": args.key_file,
    }


def group(args):
    connection_group = Group(*args.host_names, user=args.username,
                             connect_kwargs=get_connect_cfg(args))

    for c in args.cmd:
        results = connection_group.run(c)

        for connection, result in results.items():
            print("{0.host}: {1.stdout}".format(connection, result))


if __name__ == "__main__":
    start = time.time()
    args = parse_arguments()

    validate_arguments(args)
    transform_arguments(args)

    group(args)
    log.info("done", elapsed_time=time.time() - start)
