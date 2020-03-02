#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import cgi
import sys
import time
import logging

# LOG
if os.path.exists('spider.log'):
    os.remove('spider.log')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('spider.log')
fh.setLevel(logging.WARNING)
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
sh.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(sh)

# IMPORT MODULES
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    logger.critical(
        "Please install modules by using \"pip install requests bs4\" or \"pip3 install requests bs4\"")
    sys.exit(0)


# PERSONAL CONFIGURATION
try:
    import conf
except ImportError:
    logger.critical("Configuration error, please check conf.py")
    sys.exit(0)


def legalize_fname(fname, replaced_char='_'):
    """In case of some illegal file names
    """
    invalid_characters = '\\/:*?"<>|'
    for c in invalid_characters:
        fname = fname.replace(c, replaced_char)
    return fname


def find_video(response):
    """Find video in a page
    """
    video_soup = BeautifulSoup(response.text, 'html.parser')
    return video_soup.find('video').find('source')['src']


def find_image(response):
    """Find image in a page
    """
    video_soup = BeautifulSoup(response.text, 'html.parser')
    return video_soup.find('img', 'resourceimage')['src']


def find_audio(response):
    """Find image in a page
    """
    audio_soup = BeautifulSoup(response.text, 'html.parser')
    return audio_soup.find('audio').find('source')['src']


def download(extract, dir):
    """Download file from an <a> tab

    Args:
        extract: an <a> tab of html
        dir: download directory
    """

    # determinate file name
    # Happens when download in the root directory of a course
    if extract.find('span', "instancename") is not None:

        # `fname` is the filename displayed on the web site
        fname, useless = extract.find('span', "instancename").stripped_strings

    # Happens when download in a folder of a course
    elif extract.find('span', "fp-filename") is not None:
        fname = extract.find('span', "fp-filename").get_text()
    else:
        return
    fname = legalize_fname(fname)

    # Check if file already exists
    listdir = os.listdir(dir)
    listdir_del_extension = [os.path.splitext(name)[0] for name in listdir]

    if fname in listdir or fname in listdir_del_extension:
        logger.info('Exists already: ' + fname)
    else:
        logger.info('Downloading ' + fname)
        download_link = extract.get('href')

        flag = False
        try:
            time.sleep(conf.SLEEP_TIME)
            r = session.get(download_link)
            original_name = cgi.parse_header(
                r.headers['Content-Disposition'])[-1]['filename']
            flag = True
        except:
            try:
                # if the page contains a video
                download_link = find_video(r)
                time.sleep(conf.SLEEP_TIME)
                r = session.get(download_link)
                original_name = cgi.parse_header(
                    r.headers['Content-Disposition'])[-1]['filename']
                flag = True
            except:
                try:
                    # if the page contains a image
                    download_link = find_image(r)
                    time.sleep(conf.SLEEP_TIME)
                    r = session.get(download_link)
                    original_name = cgi.parse_header(
                        r.headers['Content-Disposition'])[-1]['filename']
                    flag = True
                except:
                    try:
                        # if the page contains a image
                        download_link = find_audio(r)
                        time.sleep(conf.SLEEP_TIME)
                        r = session.get(download_link)
                        original_name = cgi.parse_header(
                            r.headers['Content-Disposition'])[-1]['filename']
                        flag = True
                    except:
                        logger.warning("failed to download " + dir +
                                       fname + ' from ' + download_link + '. Please paste the link to your browser and download manually')
        if flag:
            # add filename extension
            extension = '.' + original_name.split('.')[-1]
            if os.path.splitext(fname)[-1] != extension:
                fname = fname + extension

            with open(dir + fname, 'wb') as f:
                f.write(r.content)
            logger.info('Successfully downloaded')


def download_files(soup, dir):
    """Download all files from a BeautifulSoup object

    Args:
        soup: a BeautifulSoup object
        dir: download directory
    """
    main = soup.find('div', role="main")
    for extract in main.find_all('a', href=re.compile(r"http://moodle.speit.sjtu.edu.cn/moodle/mod/resource/view.php\?id=[0-9]+")):
        download(extract, dir)
    for extract in main.find_all('a', href=re.compile(r"http://moodle.speit.sjtu.edu.cn/moodle/pluginfile.php/(.*)")):
        download(extract, dir)


def download_folders(soup, dir):
    """Download all files in folders from a BeautifulSoup object

    Args:
        soup: a BeautifulSoup object
        dir: download directory
    """
    for extract in soup.find('div', role="main").find_all('a', href=re.compile(r"http://moodle.speit.sjtu.edu.cn/moodle/mod/folder/view.php\?id=[0-9]+")):
        folder_link = extract.get('href')
        subdir, useless = extract.find('span', "instancename").stripped_strings
        subdir = dir+subdir+'/'
        logger.info('\nEnter sub directory: ' + subdir)
        os.makedirs(subdir, exist_ok=True)
        time.sleep(conf.SLEEP_TIME)
        response = session.get(url=folder_link)
        subsoup = BeautifulSoup(response.text, 'html.parser')

        download_files(subsoup, subdir)


if __name__ == '__main__':

    # LOG IN
    session = requests.Session()
    session.post(url=conf.LOGIN_URL, data=conf.DATA)

    # CHECK LOG IN STATUS
    response = session.head(conf.HOME_URL)
    if response.status_code == 200:
        logger.info('Log in succeed.')
    else:
        logger.critical(
            'log in failed. Please check your user name and password.')
        sys.exit(0)

    if conf.CRAZY_MODE:
        conf.COURSE_LIST = []
        time.sleep(conf.SLEEP_TIME)
        response = session.get(conf.HOME_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        for extract in soup.find('div', role="main").find_all('a', href=re.compile(r"http://moodle.speit.sjtu.edu.cn/moodle/course/view.php\?id=[0-9]+")):
            conf.COURSE_LIST.append(extract.get('href'))
    else:
        for i in range(len(conf.COURSE_LIST)):
            conf.COURSE_LIST[i] = "http://moodle.speit.sjtu.edu.cn/moodle/course/view.php?id=" + str(conf.COURSE_LIST[i])
    # TRAVERSE COURSES
    for url in conf.COURSE_LIST:

        time.sleep(conf.SLEEP_TIME)
        response = session.get(url=url)
        if not response.ok:
            logger.warning("URL is invalid: " + url +
                           ' . Please check COURSE_URL_LIST in conf.py')
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        course_name = soup.find('h1').get_text()
        dir = os.path.dirname(os.path.abspath(__file__)) + \
            '/download/' + course_name+'/'
        os.makedirs(dir, exist_ok=True)

        logger.info("\nDownloading files of " + course_name + ' to ' + dir)
        download_files(soup, dir)
        download_folders(soup, dir)

    logger.info("All finished. Please check the log in file spider.log for errors")
