import logging

import requests

from config import API_BASE_URL


class contact_client:
    def get_student_info(self, barcode):
        try:
            resp = requests.get(f"{API_BASE_URL}/students/barcode/{barcode}", timeout=5)
            if not resp.ok:
                return False
            d = resp.json()
            return [d["first_name"], d["last_name"], d["emails"], d["pid"], d["first_enr_term"], d["last_enr_term"]]
        except Exception as e:
            logging.error(f"Error fetching student by barcode: {e}")
            return False

    def get_student_info_pid(self, pid):
        try:
            resp = requests.get(f"{API_BASE_URL}/students/pid/{pid}", timeout=5)
            if not resp.ok:
                return False
            d = resp.json()
            return [d["first_name"], d["last_name"], d["emails"], d["pid"], d["first_enr_term"], d["last_enr_term"]]
        except Exception as e:
            logging.error(f"Error fetching student by pid: {e}")
            return False

    # TODO: I assume this was probably to add in support for employee checkin, when reimplemented
    # TODO: it should be started with an implementation on the api side
    # # not yet tested, still need to be authorized access to employeeData API.
    # def get_staff_info(self, pid):
    #     if self.token["expires_at"] < time.time() + 60:
    #         self.token = self.oauth2_client.fetch_token(
    #             api_url + "token", grant_type="client_credentials"
    #         )
    #     url = api_url + "employee_data/v1/employees/" + str(pid)
    #     token = self.token["access_token"]
    #     response = self.safe_get(url, token)
    #     if not response.ok:
    #         return False
    #     email = response.json()["officialEmail"]
    #     fname = response.json()["firstName"]
    #     lname = response.json()["lastName"]
    #     return [fname, lname, [email]]
    #
    # def safe_get(self, url, token, retries=2):
    #     for _ in range(retries):
    #         try:
    #             response = requests.get(
    #                 url, headers={"Authorization": f"Bearer {token}"}, timeout=4
    #             )
    #             if response.ok:
    #                 return response
    #         except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
    #             pass
    #         time.sleep(0.5)  # small pause before retry
    #     return False
