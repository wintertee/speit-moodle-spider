import requests
import time
import http
from . import path  # noqa: F401
from . import log
from config.conf import SLEEP_TIME


class Session(requests.Session):
    header_close = {'Connection': 'close'}
    logger = log.get_logger('spider.session')

    def get(self, url, **kwargs):
        time.sleep(SLEEP_TIME)
        for i in range(3):
            try:
                return super().get(url, headers=Session.header_close, **kwargs)
            except (requests.exceptions.ChunkedEncodingError, http.client.HTTPException, requests.exceptions.ConnectionError):
                Session.logger.debug('Session get failed')
                time.sleep(10)
                continue
            break
        return False

    def head(self, url, **kwargs):
        for i in range(3):
            try:
                return super().head(url, headers=Session.header_close, **kwargs)
            except (requests.exceptions.ChunkedEncodingError, http.client.HTTPException, requests.exceptions.ConnectionError):
                Session.logger.debug('Session head Error')
                time.sleep(10)
                continue
            break
        Session.logger.debug('Sesson head failed')
        return False


requests.adapters.DEFAULT_RETRIES = 5

session = Session()
session.keep_alive = False
