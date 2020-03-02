# You can check the latest version at https://github.com/wintertee/speit-moodle-spider

# PERSONAL CONFIGURATION

# Your user name and password
DATA = {
    'username': 'Enter your username here!',
    'password': 'Enter your password here!'
}

# Links of courses that you want to download
# Change them into id of courses to crawl
# For Example, URL for Introduction to quantum physics and statistical physics is
# http://moodle.speit.sjtu.edu.cn/moodle/course/view.php?id=626'
# So its ID is 626
# For Example, URL for Functions of Complex Variables is
# http://moodle.speit.sjtu.edu.cn/moodle/course/view.php?id=623'
# So its ID is 623
COURSE_LIST = [
    626,
    623
]

# set True to ignore COURSE_URL_LIST and download all accessible courses
CRAZY_MODE = True

# -----

# GENERAL SETTINGS
LOGIN_URL = 'http://moodle.speit.sjtu.edu.cn/moodle/login/index.php'
HOME_URL = 'http://moodle.speit.sjtu.edu.cn/moodle/my/'

# sleep before each HTTP get method
SLEEP_TIME = 1
