import logging
import sys
import time

import requests

from config import API_BASE_URL


def _req(method, url, **kwargs):
    start = time.time()
    resp = requests.request(method, url, **kwargs)
    ms = (time.time() - start) * 1000
    logging.info(f"[CLIENT] {method.upper()} {url} -> {resp.status_code} ({ms:.0f}ms)")
    return resp


def check_api_health(retries=3, delay=3):
    logging.info(API_BASE_URL)
    for attempt in range(1, retries + 1):
        try:
            resp = _req("GET", f"{API_BASE_URL}/health", timeout=5)
            if resp.ok:
                logging.info(f"API reachable at {API_BASE_URL}")
                return
        except Exception:
            pass
        logging.warning(f"API not reachable (attempt {attempt}/{retries}), retrying in {delay}s...")
        time.sleep(delay)
    logging.critical(f"API at {API_BASE_URL} unreachable after {retries} attempts. Exiting.")
    sys.exit(1)


class SheetManager:
    def checkin_by_uuid(self, uuid):
        try:
            resp = _req("GET", f"{API_BASE_URL}/check-in/uuid/{uuid}", timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logging.error(f"Error during check-in for uuid {uuid}: {e}")
            return {"status": "api_error"}

    def checkin_by_pid(self, pid):
        try:
            resp = _req("GET", f"{API_BASE_URL}/check-in/pid/{pid}", timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logging.error(f"Error during check-in for pid {pid}: {e}")
            return {"status": "api_error"}

    def set_traffic_light(self, color):
        try:
            _req("POST", f"{API_BASE_URL}/traffic-light", json={"color": color}, timeout=5)
        except Exception as e:
            logging.error(f"Error setting traffic light: {e}")

    def get_traffic_light(self):
        try:
            resp = _req("GET", f"{API_BASE_URL}/traffic-light", timeout=5)
            return resp.json().get("color", "off")
        except Exception as e:
            logging.error(f"Error getting traffic light: {e}")
            return "off"

    def create_account(self, first_name, last_name, email, pid, rfid):
        try:
            resp = _req(
                "POST",
                f"{API_BASE_URL}/accounts",
                json={
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "pid": pid,
                    "rfid": rfid,
                },
                timeout=30,
            )
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logging.error(f"Error creating account: {e}")
            return None
