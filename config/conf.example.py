# You can check the latest version at https://github.com/wintertee/speit_moodle_spider
# -----------------------------------------
# PERSONAL CONFIGURATION
# -----------------------------------------
# Your user name and password
DATA = {
    'username': 'Enter your username here!',
    'password': 'Enter your password here!'
}

# Links of courses that you want to download
COURSE_URL_LIST = [
    # Change them into URLs of courses to crawl
    # Examples:
    # URL for Introduction to quantum physics and statistical physics
    'http://moodle.speit.sjtu.edu.cn/moodle/course/view.php?id=626',
    # URL for Probability & statistics
    'http://moodle.speit.sjtu.edu.cn/moodle/course/view.php?id=621'
]

# set True to ignore COURSE_URL_LIST and download all accessible courses
CRAZY_MODE = False

# -----------------------------------------
# GENERAL CONFIGURATION (DO NOT CHANGE IT)
# -----------------------------------------

# sleep before each HTTP get method
SLEEP_TIME = 1

DEBUG = False

LOGIN_URL = 'http://moodle.speit.sjtu.edu.cn/moodle/login/index.php'
HOME_URL = 'http://moodle.speit.sjtu.edu.cn/moodle/my/'
