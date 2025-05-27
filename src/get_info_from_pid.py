import requests
from typing import Any
import time
import datetime
from authlib.integrations.requests_client import OAuth2Session
import imp
import obf as oAuth

api_url = "https://api.ucsd.edu:8243/"

### Use a UCSD student or staff member ID# (a.k.a.) PID
### To find the person's name and email from UCSD's central DB.

### USAGE: create a contact_client object, then call either get_student_info or get_staff_info with pid as arguement

### intended return: list of [first name, last name, [list of emails on file]]. Students may have multiple, staff members only one. For consistency, emails will always be a list.

### when things go wrong: if the server is unresponsive (likely due to bad internet connection), we are likely to raise a ConnectionError or Timeout exception.  If the network connection is good but the request fails (i.e. the PID is not correct, or authentication fails), then False is returned.


class contact_client:
    def __init__(self):
        self.oauth2_client = OAuth2Session(
            oAuth.client_id, oAuth.client_secret, token_url=api_url + "token"
        )
        self.token = self.oauth2_client.fetch_token(
            api_url + "token", grant_type="client_credentials"
        )
    
    def get_student_info_pid(self, pid):
        if self.token["expires_at"] < time.time() + 60:
            self.token = self.oauth2_client.fetch_token(
                api_url + "token", grant_type="client_credentials"
            )

        token = self.token["access_token"]
        url = (
            api_url
            + "student_contact_info/v1/students/contactinfo_by_pids?studentIds="
            + str(pid)
        )

        response = self.safe_get(url, token)
        if not response or not response.ok:
            # HTTPS CONNECTION ERROR SECOND PART -> first at get_student_info in main_checkin_only
            return False
        fname = response.json()[0]["name"]["firstName"]
        lname = response.json()[0]["name"]["lastName"]
        # Formatting in API JSON: Under name, in the form of SP25, etc
        firstEnrTrm = response.json()[0]["name"]["firstEnrTrm"]
        lastEnrTrm = response.json()[0]["name"]["lastEnrTrm"]
        emails = []
        for entries in response.json()[0]["emailAddressList"]:
            emails.append(entries["emailAddress"])
        return [fname, lname, emails, pid, firstEnrTrm, lastEnrTrm]


    def get_student_info(self, barcode):
        if self.token["expires_at"] < time.time() + 60:
            self.token = self.oauth2_client.fetch_token(
                api_url + "token", grant_type="client_credentials"
            )

        token = self.token["access_token"]
        barcode_url = f"{api_url}student_contact_info/v1/students/{barcode}/student_id"
        barcode_response = self.safe_get(barcode_url, token)
        if not barcode_response or not barcode_response.ok:
            return False

        pid = barcode_response.json()["studentId"]
        url = (
            api_url
            + "student_contact_info/v1/students/contactinfo_by_pids?studentIds="
            + str(pid)
        )

        response = self.safe_get(
            url, token)
        if not response or not response.ok:
            # THIS IS PART 2 OF HTTPSCONNECTIONPOOL ERROR
            return False
        fname = response.json()[0]["name"]["firstName"]
        lname = response.json()[0]["name"]["lastName"]
        # Formatting in API JSON: Under name, in the form of SP25, etc
        firstEnrTrm = response.json()[0]["name"]["firstEnrTrm"]
        lastEnrTrm = response.json()[0]["name"]["lastEnrTrm"]
        emails = []
        for entries in response.json()[0]["emailAddressList"]:
            emails.append(entries["emailAddress"])
        return [fname, lname, emails, pid, firstEnrTrm, lastEnrTrm]

    # not yet tested, still need to be authorized access to employeeData API.
    def get_staff_info(self, pid):
        if self.token["expires_at"] < time.time() + 60:
            self.token = self.oauth2_client.fetch_token(
                api_url + "token", grant_type="client_credentials"
            )
        url = api_url + "employee_data/v1/employees/" + str(pid)
        token = self.token["access_token"]
        response = self.safe_get(url, token)
        if not response.ok:
            return False
        email = response.json()["officialEmail"]
        fname = response.json()["firstName"]
        lname = response.json()["lastName"]
        return [fname, lname, [email]]
    
    def safe_get(self, url, token, retries=2):
        for _ in range(retries):
            try:
                response = requests.get(
                    url, headers={"Authorization": f"Bearer {token}"}, timeout=4
                )
                if response.ok:
                    return response
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                pass
            time.sleep(0.5)  # small pause before retry
        return False

