#! /usr/bin/env python3

import subprocess
import logging
import argparse
import syslog
import sys

try :
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import os.path

chrome_domains = (
        "youtu.be",
        "youtube-nocookie.com",
        "m.youtube.com",
        "www.youtube.ae",
        "www.youtube.at",
        "www.youtube.az",
        "www.youtube.ba",
        "www.youtube.be",
        "www.youtube.bg",
        "www.youtube.bh",
        "www.youtube.bo",
        "www.youtube.by",
        "www.youtube.ca",
        "www.youtube.cat",
        "www.youtube.ch",
        "www.youtube.cl",
        "www.youtube.co",
        "www.youtube.co.ae",
        "www.youtube.co.at",
        "www.youtube.co.cr",
        "www.youtube.co.hu",
        "www.youtube.co.id",
        "www.youtube.co.il",
        "www.youtube.co.in",
        "www.youtube.co.jp",
        "www.youtube.co.ke",
        "www.youtube.co.kr",
        "www.youtube.co.ma",
        "www.youtube.co.nz",
        "www.youtube.co.th",
        "www.youtube.co.tz",
        "www.youtube.co.ug",
        "www.youtube.co.uk",
        "www.youtube.co.ve",
        "www.youtube.co.za",
        "www.youtube.co.zw",
        "www.youtube.com",
        "www.youtube.com.ar",
        "www.youtube.com.au",
        "www.youtube.com.az",
        "www.youtube.com.bd",
        "www.youtube.com.bh",
        "www.youtube.com.bo",
        "www.youtube.com.br",
        "www.youtube.com.by",
        "www.youtube.com.co",
        "www.youtube.com.do",
        "www.youtube.com.ec",
        "www.youtube.com.ee",
        "www.youtube.com.eg",
        "www.youtube.com.es",
        "www.youtube.com.gh",
        "www.youtube.com.gr",
        "www.youtube.com.gt",
        "www.youtube.com.hk",
        "www.youtube.com.hn",
        "www.youtube.com.hr",
        "www.youtube.com.jm",
        "www.youtube.com.jo",
        "www.youtube.com.kw",
        "www.youtube.com.lb",
        "www.youtube.com.lv",
        "www.youtube.com.ly",
        "www.youtube.com.mk",
        "www.youtube.com.mt",
        "www.youtube.com.mx",
        "www.youtube.com.my",
        "www.youtube.com.ng",
        "www.youtube.com.ni",
        "www.youtube.com.om",
        "www.youtube.com.pa",
        "www.youtube.com.pe",
        "www.youtube.com.ph",
        "www.youtube.com.pk",
        "www.youtube.com.pt",
        "www.youtube.com.py",
        "www.youtube.com.qa",
        "www.youtube.com.ro",
        "www.youtube.com.sa",
        "www.youtube.com.sg",
        "www.youtube.com.sv",
        "www.youtube.com.tn",
        "www.youtube.com.tr",
        "www.youtube.com.tw",
        "www.youtube.com.ua",
        "www.youtube.com.uy",
        "www.youtube.com.ve",
        "www.youtube.cr",
        "www.youtube.cz",
        "www.youtube.de",
        "www.youtube.dk",
        "www.youtube.ee",
        "www.youtube.es",
        "www.youtube.fi",
        "www.youtube.fr",
        "www.youtube.ge",
        "www.youtube.gr",
        "www.youtube.gt",
        "www.youtube.hk",
        "www.youtube.hr",
        "www.youtube.hu",
        "www.youtube.ie",
        "www.youtube.in",
        "www.youtube.iq",
        "www.youtube.is",
        "www.youtube.it",
        "www.youtube.jo",
        "www.youtube.jp",
        "www.youtube.kr",
        "www.youtube.kz",
        "www.youtube.lk",
        "www.youtube.lt",
        "www.youtube.lu",
        "www.youtube.lv",
        "www.youtube.ly",
        "www.youtube.ma",
        "www.youtube.me",
        "www.youtube.mk",
        "www.youtube.mx",
        "www.youtube.my",
        "www.youtube.net.in",
        "www.youtube.ng",
        "www.youtube.ni",
        "www.youtube.nl",
        "www.youtube.no",
        "www.youtube.pa",
        "www.youtube.pe",
        "www.youtube.ph",
        "www.youtube.pk",
        "www.youtube.pl",
        "www.youtube.pr",
        "www.youtube.pt",
        "www.youtube.qa",
        "www.youtube.ro",
        "www.youtube.rs",
        "www.youtube.ru",
        "www.youtube.sa",
        "www.youtube.se",
        "www.youtube.sg",
        "www.youtube.si",
        "www.youtube.sk",
        "www.youtube.sn",
        "www.youtube.sv",
        "www.youtube.tn",
        "www.youtube.tv",
        "www.youtube.ua",
        "www.youtube.ug",
        "www.youtube.uy",
        "www.youtube.vn",
        "www.youtube.voto"
        )

def http_url(url):
    if url.startswith('http://'):
        return url
    if url.startswith('https://'):
        return url
    else:
        syslog.syslog(syslog.LOG_ERR, sys.argv[0] + ": not an HTTP/HTTPS URL: '{}'".format(url))
        raise argparse.ArgumentTypeError(
            "not an HTTP/HTTPS URL: '{}'".format(url))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Handler for http/https URLs.'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        help='More verbose logging',
        dest="loglevel",
        default=logging.WARNING,
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        '-d',
        '--debug',
        help='Enable debugging logs',
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
    )
    parser.add_argument(
        'url',
        type=http_url,
        help="URL starting with 'http://' or 'https://'",
    )
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    logging.debug("args.url = '{}'".format(args.url))
    parsed = urlparse(args.url)
    logging.info("hostname = '{}'".format(parsed.hostname))
    
    if parsed.hostname in chrome_domains:
        browser = "google-chrome"
    else:
        browser = 'firefox'
    logging.info("browser = '{}'".format(browser))
    cmd = [browser, args.url]
    try :
        status = subprocess.check_call(cmd)
    except subprocess.CalledProcessError:
        syslog.syslog(syslog.LOG_ERR, sys.argv[0] + "could not open URL with browser '{}': {}".format(browser, args.url))
        raise
