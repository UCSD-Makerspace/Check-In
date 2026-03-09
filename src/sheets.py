import logging
import sys
import time

import requests

from config import API_BASE_URL


def check_api_health(retries=3, delay=3):
    logging.info(API_BASE_URL)
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(f"{API_BASE_URL}/health", timeout=5)
            if resp.ok:
                logging.info(f"API reachable at {API_BASE_URL}")
                return
        except Exception:
            pass
        logging.warning(f"API not reachable (attempt {attempt}/{retries}), retrying in {delay}s...")
        time.sleep(delay)
    logging.critical(f"API at {API_BASE_URL} unreachable after {retries} attempts. Exiting.")
    sys.exit(1)


class _SheetProxy:
    def __init__(self, endpoint):
        self._endpoint = endpoint

    def append_row(self, row):
        try:
            requests.post(f"{API_BASE_URL}{self._endpoint}", json={"row": row}, timeout=10)
        except Exception as e:
            logging.error(f"Error appending row to {self._endpoint}: {e}")


class SheetManager:
    def get_user_db(self):
        return _SheetProxy("/users")

    def get_activity_db(self):
        return _SheetProxy("/activity")

    def get_user_by_card(self, uuid):
        try:
            resp = requests.get(f"{API_BASE_URL}/users/{uuid}", timeout=10)
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logging.error(f"Error fetching user by card {uuid}: {e}")
            return None

    def check_waiver(self, pid, email):
        try:
            resp = requests.get(f"{API_BASE_URL}/waivers/check", params={"pid": pid, "email": email}, timeout=10)
            resp.raise_for_status()
            return resp.json()["has_waiver"]
        except Exception as e:
            logging.error(f"Error checking waiver for pid={pid}: {e}")
            return False
