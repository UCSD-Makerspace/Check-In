import logging

import requests

from config import API_BASE_URL


class fabman:
    def createFabmanAccount(self, firstName, lastName, emailAddress, RFIDtag):
        try:
            resp = requests.post(
                f"{API_BASE_URL}/members",
                json={
                    "first_name": firstName,
                    "last_name": lastName,
                    "email": emailAddress,
                    "rfid_tag": RFIDtag,
                },
                timeout=30,
            )
            if not resp.ok:
                logging.warning(f"Fabman account creation failed: {resp.status_code}")
        except Exception as e:
            logging.error(f"Error creating Fabman account: {e}")
