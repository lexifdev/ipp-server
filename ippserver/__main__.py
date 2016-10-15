from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import logging
import sys

from . import behaviour
from .server import run_server, ThreadedTCPServer, ThreadedTCPRequestHandler


def parse_args():
	parser = argparse.ArgumentParser(description='An IPP server')
	parser.add_argument('-v', '--verbose', action='count', help='Add debugging')
	parser.add_argument('-H', '--host', type=str, default='localhost', metavar='HOST', help='Address to listen on')
	parser.add_argument('-p', '--port', type=int, required=True, metavar='PORT', help='Port to listen on')

	parser_action = parser.add_subparsers(help='Actions', dest='action')

	parser_save = parser_action.add_parser('save', help='Write any print jobs to disk')
	parser_save.add_argument('directory', metavar='DIRECTORY', help='Directory to save files into')

	parser_command = parser_action.add_parser('run', help='Run a command when recieving a print job')
	parser_command.add_argument('command', nargs=argparse.REMAINDER, metavar='COMMAND', help='Command to run')

	return parser.parse_args()

def behaviour_from_args(args):
	if args.action == 'save':
		return behaviour.SaveFilePrinter(directory=args.directory)
	if args.action == 'run':
		return behaviour.RunCommandPrinter(command=args.command)
	raise RuntimeError(args)

def main(args):
	logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

	server = ThreadedTCPServer(
		(args.host, args.port),
		ThreadedTCPRequestHandler,
		behaviour_from_args(args))
	run_server(server)

if __name__ == "__main__":
	main(parse_args())
