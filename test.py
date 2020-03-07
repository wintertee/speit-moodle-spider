#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from spider import path
from utils import utils


# import extractor

# LOGIN_URL = 'http://moodle.speit.sjtu.edu.cn/moodle/login/index.php'
# network.session.post(url=LOGIN_URL, data=conf.DATA)

# r=network.session.head("http://moodle.speit.sjtu.edu.cn/moodle/pluginfile.php/18131/mod_resource/content/1/Cours%200.pdf")
# print(network.download.get_remote_time("http://moodle.speit.sjtu.edu.cn/moodle/pluginfile.php/18131/mod_resource/content/1/Cours%200.pdf"))
# print(extractor.__file__)
utils.update_file_mtime(path.BASE_DIR + '/downloads/')