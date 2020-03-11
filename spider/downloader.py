#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import time
import cgi
from dateutil.parser import parse as parsedate
from bs4 import BeautifulSoup

from . import path  # noqa: F401
from . import extractor
from . import log
from .session import session
from config import conf
from utils import utils

logger = log.get_logger('spider.downloader')


def get_download_link(extract, fname='unknown'):
    """get the final download link in an <a> tab
    - support redirection to a file
    - support redirection to a webpage embedding a video/photo/audio
    - return None if cannot find the link
    """
    download_link_raw = extract.get('href')
    r = session.head(download_link_raw)
    if r is False:
        logger.warning('Failed to parse ' + download_link_raw)
        return None

    # redirection
    while r.is_redirect:
        download_link_raw = r.headers['location']
        r = session.head(download_link_raw)
        if r is False:
            logger.warning('Failed to parse ' + download_link_raw)
            return None

    # for embedded video/photo/audio, store the link in download_link
    if 'Content-Disposition' not in r.headers:
        r = session.get(download_link_raw)
        if r is False:
            logger.warning('Failed to parse ' + download_link_raw)
            return None
        soup = BeautifulSoup(r.text, 'html.parser')
        for fonction in extractor.extractors:
            download_link = fonction(soup)
            if download_link is not None:
                break
        if download_link is None:
            logger.warning('Failed to download ' + fname + ' from ' + download_link_raw)
        return download_link
    else:
        return download_link_raw


def get_remote_date(download_link):
    """"get the 'last-modified' date in an url
    """
    r = session.head(download_link)
    if r is False:
        return False
    else:
        remote_date = r.headers['last-modified']
        return parsedate(remote_date)


def download(dir, fname, download_link, remote_date=None):
    r = session.get(download_link)
    if r is False:
        logger.warning('Failed to download ' + fname + ' from ' + download_link)

    # remote date
    if remote_date is None:
        remote_date = get_remote_date(download_link)
        if remote_date is None:
            logger.warning('Failed to check remote date of ' + fname + ' from ' + download_link)
            return
        remote_date = utils.datetime_from_utc_to_local(remote_date)

    # in case of fname do not contains an extension
    original_name = cgi.parse_header(r.headers['Content-Disposition'])[-1]['filename']
    extension = '.' + original_name.split('.')[-1]
    if os.path.splitext(fname)[-1] != extension:
        fname = fname + extension

    with open(dir + fname, 'wb') as f:
        f.write(r.content)

    # from datetime to timestamp
    remote_date = time.mktime(remote_date.timetuple())
    # set mtime and atime
    os.utime(dir + fname, (remote_date, remote_date))
    logger.info("Done")


def download_proccess(extract, dir):
    """Download proccess from an <a> tab
    if file exists, check update
    if file do not exists, download it

    Args:
        extract: an <a> tab of html
        dir: download directory
    """
    # determinate file name
    fname = extractor.fname(extract)
    if fname is False:
        return

    download_link = get_download_link(extract, fname)
    if download_link is None:
        return

    # if file already exists
    if utils.file_exist(fname, dir):
        # check update
        fname = utils.file_exist(fname, dir)
        remote_date = get_remote_date(download_link)
        if remote_date is None:
            logger.warning('Failed to check remote date of ' + fname + ' from ' + download_link)
            return
        remote_date = utils.datetime_from_utc_to_local(remote_date)
        local_date = utils.get_local_date(fname, dir)
        if remote_date > local_date:
            logger.info('Updating ' + '\033[1;33m' + fname + '\033[0m')
            utils.older_file(fname, dir)
            download(dir, fname, download_link, remote_date=remote_date)
        else:
            logger.debug('no update: ' + fname + ' from ' + download_link)
    else:
        logger.info('Downloading ' + '\033[1;32m' + fname + '\033[0m')
        download(dir, fname, download_link)


def download_files(soup, dir):
    """Download all files from a BeautifulSoup object

    Args:
        soup: a BeautifulSoup object
        dir: download directory
    """
    main = soup.find('div', role="main")
    for extract in main.find_all(
            'a', href=re.compile(r"http://moodle.speit.sjtu.edu.cn/moodle/mod/resource/view.php\?id=[0-9]+")):
        download_proccess(extract, dir)
    for extract in main.find_all('a', href=re.compile(r"http://moodle.speit.sjtu.edu.cn/moodle/pluginfile.php/(.*)")):
        download_proccess(extract, dir)


def download_folders(soup, dir):
    """Download all files in folders from a BeautifulSoup object

    Args:
        soup: a BeautifulSoup object
        dir: download directory
    """
    for extract in soup.find('div', role="main").find_all(
            'a', href=re.compile(r"http://moodle.speit.sjtu.edu.cn/moodle/mod/folder/view.php\?id=[0-9]+")):
        folder_link = extract.get('href')
        subdir, *_ = extract.find('span', "instancename").stripped_strings
        logger.info('Enter sub directory: ' + subdir)
        subdir = dir + subdir + '/'
        os.makedirs(subdir, exist_ok=True)
        time.sleep(conf.SLEEP_TIME)
        response = session.get(url=folder_link)
        if response is False:
            logger.warning('Failed to prase sub directory: ' + subdir)
            return
        subsoup = BeautifulSoup(response.text, 'html.parser')

        download_files(subsoup, subdir)
