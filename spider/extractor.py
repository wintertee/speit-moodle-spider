#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils import utils


def video(soup):
    """Find video in a page
    """
    try:
        return soup.find('video').find('source')['src']
    except AttributeError:
        return None


def image(soup):
    """Find image in a page
    """
    try:
        return soup.find('img', 'resourceimage')['src']
    except TypeError:
        return None


def audio(soup):
    """Find image in a page
    """
    try:
        return soup.find('audio').find('source')['src']
    except AttributeError:
        return None


def iframe(soup):
    """Find image in a page
    """
    try:
        return soup.find('iframe')['src']
    except TypeError:
        return None


def fname(extract):
    """Find file name in an <a> tab
    """
    # Happens when download in the root directory of a course
    if extract.find('span', "instancename") is not None:
        # `fname` is the filename displayed on the web site
        fname, *_ = extract.find('span', "instancename").stripped_strings
    # Happens when download in a folder of a course
    elif extract.find('span', "fp-filename") is not None:
        fname = extract.find('span', "fp-filename").get_text()
    else:
        return False

    return utils.legalize_fname(fname)


extractors = [video, image, audio, iframe]
