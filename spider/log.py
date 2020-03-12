#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os

from . import path
from config.conf import DEBUG


def get_logger(name):
    return logging.getLogger(name)


def init_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(path.LOG_DIR)
    fh.setLevel(logging.WARNING)
    sh = logging.StreamHandler()
    # if DEBUG:
    #     sh.setLevel(logging.DEBUG)
    #     formatter = logging.Formatter('%(asctime)s %(name)s : %(levelname)s - %(message)s')
    # else:
    #     sh.setLevel(logging.INFO)
    #     formatter = logging.Formatter('%(levelname)s: %(message)s')

    formatter = logging.Formatter('%(asctime)s %(name)s : %(levelname)s - %(message)s')

    fh.setFormatter(formatter)
    # sh.setFormatter(formatter)

    logger.addHandler(fh)
    # logger.addHandler(sh)

    return logger


def clean_log():
    if os.path.exists(path.LOG_DIR):
        os.remove(path.LOG_DIR)
