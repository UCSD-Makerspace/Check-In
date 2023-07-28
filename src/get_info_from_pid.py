import requests
from typing import Any
import time
import datetime
from authlib.integrations.requests_client import OAuth2Session
import imp
import obf as oAuth
#oAuth = imp.load_compiled("oAuth","obf.pyc")
api_url = "https://api.ucsd.edu:8243/"

### Use a UCSD student or staff member ID# (a.k.a.) PID
### To find the person's name and email from UCSD's central DB.

### USAGE: create a contact_client object, then call either get_student_info or get_staff_info with pid as arguement

### intended return: list of [first name, last name, [list of emails on file]]. Students may have multiple, staff members only one. For consistency, emails will always be a list.

### when things go wrong: if the server is unresponsive (likely due to bad internet connection), we are likely to raise a ConnectionError or Timeout exception.  If the network connection is good but the request fails (i.e. the PID is not correct, or authentication fails), then False is returned.

class contact_client:
    def __init__(self):
        self.oauth2_client = OAuth2Session(oAuth.client_id, oAuth.client_secret, token_url=api_url+"token")
        self.token = self.oauth2_client.fetch_token(api_url+"token", grant_type='client_credentials')

    def get_student_info (self, pid):
        if self.token['expires_at'] < time.time()+60:
            self.token = self.oauth2_client.fetch_token(api_url+"token", grant_type='client_credentials')
        url = api_url+'student_contact_info/v1/students/contactinfo_by_pids?studentIds='+str(pid)
        token = self.token["access_token"]
        response = requests.get(url, headers={'Authorization': f"Bearer {token}"}, timeout = 1)
        if not response.ok:
            return False
        fname= response.json()[0]['name']['firstName']
        lname = response.json()[0]['name']['lastName']
        emails=[]
        for entries in response.json()[0]['emailAddressList']:
            emails.append(entries['emailAddress'])
        return [fname,lname,emails]

# not yet tested, still need to be authorized access to employeeData API.
    def get_staff_info (self, pid):
        if self.token['expires_at'] < time.time()+60:
            self.token = self.oauth2_client.fetch_token(api_url+"token", grant_type='client_credentials')
        url = api_url+'employee_data/v1/employees/'+str(pid)
        token = self.token["access_token"]
        response = requests.get(url, headers={'Authorization': f"Bearer {token}"}, timeout = 1)
        if not response.ok:
            return False
        email=response.json()['officialEmail']
        fname= response.json()['firstName']
        lname = response.json()['lastName']
        return [fname,lname,[email]]
