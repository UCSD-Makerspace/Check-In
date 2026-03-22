import logging
import time

import requests


def _req(method, url, **kwargs):
    start = time.time()
    resp = requests.request(method, url, **kwargs)
    ms = (time.time() - start) * 1000
    logging.info(f"[CLIENT] {method.upper()} {url} -> {resp.status_code} ({ms:.0f}ms)")
    return resp
