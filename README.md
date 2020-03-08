# SPEIT Moodle spider

A simple spider to crawl files at moodle.  

### NOTICE
- The current version (V1.0) is **NOT** compatible with any previous version. Please delete all files of the previous version before using it!
- Do **NOT** modify files downloaded, if you want to, copy them to another directory first.

## Download

- Make a new directory: `mkdir moodle_spider && cd moodle_spider`

- Go to [Release](https://github.com/wintertee/speit-moodle-spider/releases), download and unzip the source code.

- You can also download it at <https://www.wintertee.top/cloud_storage_wintertee/speit_moodle_spider/>

- Or you can simply use `git clone https://github.com/wintertee/speit-moodle-spider.git`

## Configuration

- Install requirements:

  - On Unix or Linux: `pip install -r requirements.txt` or `pip3 install -r requirements.txt`

  - On Windows: `pip install -r requirements-nt.txt` or `pip3 install -r requirements-nt.txt`

- Make a copy of `config/conf.exemple.py` and rename it as `conf.py`

- Edit the `config/conf.py` with your personal info.  

## Usage

- Run `speit-moodle-spider.py` with Python 3:

  - `python speit-moodle-spider.py`
  
  - or `python3 speit-moodle-spider.py`

## Notice

- Only tested with student account.

## Support me

If this tiny program is helpful to you, please leave a **star** in the upper right corner of the home page :D

## Brother project

[Moodle-Notifier](https://github.com/davidliyutong/Moodle-Notifier)
