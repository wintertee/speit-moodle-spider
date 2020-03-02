# Speit_moodle_spider

A simple spider to crawl files at moodle

## Download

- Make a new directory: `mkdir moodle_spider && cd moodle_spider`

- Download the following links and put them into the directory just created:

	<https://github.com/wintertee/speit_moodle_spider/raw/master/speit_moodle_spider.py>  

	<https://github.com/wintertee/speit_moodle_spider/raw/master/conf.py>
	
- If you cannot access links above, you can also download at <https://www.wintertee.top/cloud_storage_wintertee/speit_moodle_spider/>

- Or you can simply use `git clone https://github.com/wintertee/speit_moodle_spider.git` 

## Usage

- Install Python 3 library `bs4` and `requests` :

  -  `pip install bs4 requests`

  - or `pip3 install bs4 requests`
  
- Edit the `conf.py` with your personal infos.  

- Run `speit_moodle_spider.py` with Python 3:

  - `python speit_moodle_spider.py`
  
  - or `python3 speit_moodle_spider.py`

## Notice

- Only tested with student accuonts.

- Cannot download file in`iframe` tag.(usually it is a `html` file).

## Support me

If this tiny script is helpful to you, please leave a **star** in the upper right corner of the home page :D

## Brother project

[Moodle-Notifier](https://github.com/davidliyutong/Moodle-Notifier)

