from __future__ import print_function

import os
import sys
fuzzer_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(fuzzer_dir)
sys.path.append(root_dir)
from boofuzz import sessions

import logging
import time
import click

@click.group()
def cli():
    pass

@cli.command(name='open')
@click.option('--debug', help='Print debug info to console', is_flag=True)
@click.option('--ui-port',
              help='Port on which to serve the web interface (default {0})'.format(26005),
              type=int, default=26005)
@click.option('--ui-addr', help='Address on which to serve the web interface (default localhost). Set to empty '
                                'string to serve on all interfaces.', type=str, default='10.15.33.211')
@click.argument('filename')
def open_file(debug, filename, ui_port, ui_addr):
    if debug:
        logging.basicConfig(level=logging.DEBUG)

    sessions.open_test_run(db_filename=filename, port=ui_port, address=ui_addr)

    print('Serving web page at http://{0}:{1}. Hit Ctrl+C to quit.'.format(ui_addr, ui_port))
    while True:
        time.sleep(.001)

def main():
    cli()

if __name__ == "__main__":
    main()