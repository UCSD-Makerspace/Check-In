import logging
import sys
import time

from config import API_BASE_URL
from api._client import _req



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


class ApiClient:
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

    def lookup_by_pid(self, pid):
        """Returns dict with first_name/last_name/email/pid, or None if not found."""
        try:
            resp = _req("GET", f"{API_BASE_URL}/accounts/lookup/pid/{pid}", timeout=10)
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logging.error(f"Error looking up student by pid {pid}: {e}")
            return None

    def lookup_by_barcode(self, barcode):
        """Returns dict with first_name/last_name/email/pid, or None if not found."""
        try:
            resp = _req("GET", f"{API_BASE_URL}/accounts/lookup/barcode/{barcode}", timeout=10)
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logging.error(f"Error looking up student by barcode: {e}")
            return None

    def create_account(self, rfid, *, barcode=None, pid=None, first_name=None, last_name=None, email=None):
        try:
            payload = {"rfid": rfid}
            if barcode:
                payload["barcode"] = barcode
            if pid:
                payload["pid"] = pid
            if first_name:
                payload["first_name"] = first_name
            if last_name:
                payload["last_name"] = last_name
            if email:
                payload["email"] = email
            resp = _req("POST", f"{API_BASE_URL}/accounts", json=payload, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logging.error(f"Error creating account: {e}")
            return None
