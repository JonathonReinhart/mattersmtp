#!/usr/bin/env python3
import mattersend
import smtpd
import asyncore
import argparse
from email.parser import Parser
import logging

# Based loosely on https://github.com/kennethreitz/inbox.py

SMTP_PORT = 25

class MatterSmtp(smtpd.SMTPServer):
    def __init__(self, address):
        super().__init__(address, None)

    def process_message(self, peer, mailfrom, rcpttos, data):
        logging.info("Receiving message from {}".format(mailfrom))


def parse_args():
    ap = argparse.ArgumentParser(
            description = 'SMTP-Mattermost bridge',
            formatter_class = argparse.ArgumentDefaultsHelpFormatter,
            )

    ap.add_argument('addr', type=str, nargs='?', default='localhost',
            help = 'addr to bind to')
    ap.add_argument('port', type=int, nargs='?', default=SMTP_PORT,
            help = 'port to bind to')
    ap.add_argument('-s', '--section',
            help =' mattersend.conf section')
    ap.add_argument('--loglevel', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
            help = 'Set the logging level (default: %(default)s)', default='WARNING')
    return ap.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(level=args.loglevel)

    address = (args.addr, args.port)
    server = MatterSmtp(address)

    try:
        asyncore.loop()
    except KeyboardInterrupt:
        logging.info('Exiting due to KeyboardInterrupt')


if __name__ == '__main__':
    main()
