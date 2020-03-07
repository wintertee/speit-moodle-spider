#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import sys
import time
from bs4 import BeautifulSoup

from . import path
from . import log
from . import downloader
from .session import session
from utils import utils


def run():
    try:
        # LOG
        log.clean_log()
        logger = log.init_logger('spider')
        logger.info('------------SPEIT-MOODLE-SPIDER V1.0------------')
        logger.info('https://github.com/wintertee/speit_moodle_spider')
        logger.info('------------------------------------------------')
        logger.info('Program started. Enter Ctrl+C to exit.')

        # PERSONAL CONFIGURATION
        try:
            from config import conf
        except ImportError:
            logger.error("Configuration error, please check config/conf.py")
            sys.exit(0)

        # LOG IN
        session.post(url=conf.LOGIN_URL, data=conf.DATA)
        response = session.head(conf.HOME_URL)
        if response is False:
            logger.error('log in failed. Please check your network connection.')
            sys.exit(0)
        if response.status_code == 200:
            logger.info('Log in succeed.')
        else:
            logger.error('log in failed. Please check your user name and password at config/conf.py .')
            sys.exit(0)

        # CRAZY MODE
        if conf.CRAZY_MODE:
            conf.COURSE_URL_LIST = []
            time.sleep(conf.SLEEP_TIME)
            response = session.get(conf.HOME_URL)
            if response is False:
                logger.error('Get course list failed. Please check your network connection.')
                sys.exit(0)
            soup = BeautifulSoup(response.text, 'html.parser')
            for extract in soup.find('div', role="main").find_all(
                    'a', href=re.compile(r"http://moodle.speit.sjtu.edu.cn/moodle/course/view.php\?id=[0-9]+")):
                conf.COURSE_URL_LIST.append(extract.get('href'))

        # TRAVERSE COURSES
        for url in conf.COURSE_URL_LIST:

            time.sleep(conf.SLEEP_TIME)
            response = session.get(url=url)
            if response is False:
                logger.warning('Failed to check course: ' + url + ' . Please retry later.')
                sys.exit(0)
            if not response.ok:
                logger.warning("URL is invalid: " + url + ' . Please check COURSE_URL_LIST in conf.py')
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            course_name = soup.find('h1').get_text()
            dir = path.BASE_DIR + '/downloads/' + course_name + '/'
            os.makedirs(dir, exist_ok=True)

            logger.info("downloading files of " + course_name)
            downloader.download_files(soup, dir)
            downloader.download_folders(soup, dir)
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt, exiting...")
        pass

    # UPDATE MTIME
    utils.update_dir_mtime(path.BASE_DIR + '/downloads/')

    logger.info("All finished. Please check spider.log for errors")
