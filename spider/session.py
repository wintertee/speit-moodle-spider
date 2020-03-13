import requests
import time
import http
from . import path  # noqa: F401
from config.conf import SLEEP_TIME


class Session(requests.Session):
    header_close = {'Connection': 'close'}

    def get(self, url, **kwargs):
        time.sleep(SLEEP_TIME)
        for i in range(3):
            try:
                return super().get(url, headers=Session.header_close, **kwargs)
            except (requests.exceptions.ChunkedEncodingError, http.client.HTTPException, requests.exceptions.ConnectionError):
                time.sleep(10)
                continue
            break
        return False

    def head(self, url, **kwargs):
        for i in range(3):
            try:
                return super().head(url, headers=Session.header_close, **kwargs)
            except (requests.exceptions.ChunkedEncodingError, http.client.HTTPException, requests.exceptions.ConnectionError):
                time.sleep(10)
                continue
            break
        return False


requests.adapters.DEFAULT_RETRIES = 5

session = Session()
session.keep_alive = False
