#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import sys
import time
from bs4 import BeautifulSoup
import colorama
from colorama import Fore

from . import path
from . import downloader
from .session import session
from utils import utils
from utils.FileTree import file_tree


def run():
    try:
        colorama.init(autoreset=True)

        print('-----------SPEIT-MOODLE-SPIDER V1.1.1-----------')
        print('https://github.com/wintertee/speit-moodle-spider')
        print('------------------------------------------------')
        print('Program started. Enter Ctrl+C to exit.')

        # PERSONAL CONFIGURATION
        try:
            from config import conf
        except ImportError:
            print(Fore.RED + 'ERROR: Configuration error, please check config/conf.py')
            print()
            sys.exit(0)

        # LOG IN
        session.post(url=conf.LOGIN_URL, data=conf.DATA)
        response = session.head(conf.HOME_URL)
        if response is False:
            print(Fore.RED + 'ERROR: log in failed. Please check your network connection.')
            sys.exit(0)
        if response.status_code == 200:
            print('Log in succeed.')
        else:
            print(Fore.RED + 'ERROR: log in failed. Please check your user name and password at config/conf.py .')
            sys.exit(0)

        # CRAZY MODE
        if conf.CRAZY_MODE:
            conf.COURSE_URL_LIST = []
            time.sleep(conf.SLEEP_TIME)
            response = session.get(conf.HOME_URL)
            if response is False:
                print(Fore.RED + 'ERROR: Get course list failed. Please check your network connection.')
                sys.exit(0)
            soup = BeautifulSoup(response.text, 'html.parser')
            for extract in soup.find('div', role="main").find_all(
                    'a', href=re.compile(r"http://moodle.speit.sjtu.edu.cn/moodle/course/view.php\?id=[0-9]+")):
                conf.COURSE_URL_LIST.append(extract.get('href'))

        print('---------------------LEGEND---------------------')
        print(Fore.GREEN + 'Green for downloaded')
        print(Fore.YELLOW + 'Yellow for updated')
        print(Fore.RED + 'Red for error')
        print('--------------------FileTree--------------------')
        file_tree.print('downloads', 0)

        # TRAVERSE COURSES
        for url in conf.COURSE_URL_LIST:

            time.sleep(conf.SLEEP_TIME)
            response = session.get(url=url)
            if response is False:
                print(Fore.RED + 'ERROR: Failed to check course: ' + url + ' . Please retry later.')
                sys.exit(0)
            if not response.ok:
                print(Fore.RED + 'ERROR: URL is invalid: ' + url + ' . Please check COURSE_URL_LIST in conf.py')
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            course_name = soup.find('h1').get_text()
            dir = path.DOWNLOAD_DIR + course_name + '/'
            os.makedirs(dir, exist_ok=True)

            file_tree.print(course_name, 1)

            downloader.download_files(soup, dir)
            downloader.download_folders(soup, dir)
    except KeyboardInterrupt:
        print("KeyboardInterrupt, stop downloading...")
        pass

    # UPDATE MTIME
    utils.update_dir_mtime(path.DOWNLOAD_DIR)
    print('Done.')
