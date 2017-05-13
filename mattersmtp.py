#!/usr/bin/env python3
import mattersend
import smtpd
import asyncore
import argparse
from email.parser import Parser
import logging
import yaml

# Based loosely on https://github.com/kennethreitz/inbox.py

SMTP_PORT = 25

class MatterSmtp(smtpd.SMTPServer):
    def __init__(self, address):
        logging.info("Binding to {}".format(address))
        super().__init__(address, None)

    def process_message(self, peer, mailfrom, rcpttos, data):
        logging.info("Receiving message from {}".format(mailfrom))

class Config:
    def __init__(self, **kwargs):
        self.set_defaults()
        self.__dict__.update(kwargs)

    @classmethod
    def load_yml(cls, path):
        """Load mattersmtp.yml"""
        with open(path, 'r') as f:
            data = yaml.safe_load(f) or {}

        # TODO: Lots of validation of yaml data

        return cls(**data)

    def set_defaults(self):
        self.loglevel = 'WARNING'
        self.bind = dict(addr='localhost', port=25)

    def merge_args(self, args):
        if args.loglevel:
            self.loglevel = args.loglevel
        if args.addr:
            self.bind['addr'] = args.addr
        if args.port:
            self.bind['port'] = args.port


def parse_args():
    ap = argparse.ArgumentParser(
            description = 'SMTP-Mattermost bridge',
            formatter_class = argparse.ArgumentDefaultsHelpFormatter,
            )

    ap.add_argument('--addr', type=str,
            help = 'Override address to which to bind')
    ap.add_argument('--port', type=int,
            help = 'Override port to wich to bind')
    ap.add_argument('-c', '--config', default='mattersmtp.yml',
            help = 'Path to mattersmtp.yml config file')
    ap.add_argument('--loglevel', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
            help = 'Override the logging level')
    return ap.parse_args()


def main():
    args = parse_args()

    cfg = Config.load_yml(args.config)
    cfg.merge_args(args)

    logging.basicConfig(level=cfg.loglevel)

    address = (cfg.bind['addr'], cfg.bind['port'])
    server = MatterSmtp(address)

    try:
        asyncore.loop()
    except KeyboardInterrupt:
        logging.info('Exiting due to KeyboardInterrupt')


if __name__ == '__main__':
    main()
