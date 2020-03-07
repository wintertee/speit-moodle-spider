#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import datetime
import time

if os.name == 'nt':
    import win32api
    import win32con


def legalize_fname(fname, replaced_char='_'):
    """In case of some illegal file names
    """
    invalid_characters = '\\/:*?"<>|'
    for c in invalid_characters:
        fname = fname.replace(c, replaced_char)
    return fname


def file_exist(fname, dir):
    """Check if file already exists, where fname can be without extension
    """
    # to replace listdir = os.listdir(dir)
    # in case of some non ASCII file name in OS X
    import unicodedata
    listdir = [unicodedata.normalize('NFC', f) for f in os.listdir(dir)]
    listdir_del_extension = [os.path.splitext(name)[0] for name in listdir]

    if fname in listdir:
        return fname

    elif fname in listdir_del_extension:
        index = listdir_del_extension.index(fname)
        return listdir[index]
    else:
        return False


def add_local_time_zone(date_time):
    return date_time.replace(tzinfo=datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo)


def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.datetime.fromtimestamp(now_timestamp) - datetime.datetime.utcfromtimestamp(now_timestamp)
    # add local time zone
    return add_local_time_zone(utc_datetime + offset)


def get_local_date(fname, dir):
    """get the ctime of a local file
    """
    date = datetime.datetime.fromtimestamp(os.path.getmtime(dir + fname))
    # add local time zone
    return add_local_time_zone(date)


def older_file(fname, dir):
    if file_exist(os.path.splitext(fname)[0] + '.old' + os.path.splitext(fname)[1], dir):
        older_file(os.path.splitext(fname)[0] + '.old' + os.path.splitext(fname)[1], dir)
    os.rename(dir + fname, os.path.splitext(dir + fname)[0] + '.old' + os.path.splitext(dir + fname)[1])


def folder_is_hidden(p):
    if os.name == 'nt':
        attribute = win32api.GetFileAttributes(p)
        return attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
    else:
        return p.startswith('.')  # linux-osx


def update_dir_mtime(dir):
    import unicodedata
    listdir = [unicodedata.normalize('NFC', f) for f in os.listdir(dir)]
    listdir = [f for f in listdir if not folder_is_hidden(f)]
    for sub in listdir:
        if os.path.isdir(dir + sub + '/'):
            update_dir_mtime(dir + sub + '/')
    date_list = [get_local_date(fname, dir) for fname in listdir]
    if len(date_list) == 0:
        date = 0
    else:
        date = time.mktime(max(date_list).timetuple())
    os.utime(dir, (date, date))
