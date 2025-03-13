import time
import gspread
import os
import logging
from oauth2client.service_account import ServiceAccountCredentials
import threading

class Sheet:
    CACHE_TIME = 60 * 5

    def __init__(self, db):
        self.db = db
        self.data = None
        self.last_updated = time.time()

    def get_sheet(self):
        return self.db
    
    def update_cache(self):
        try:
            logging.info("Updating database from web")
            self.data = self.db.get_all_records(numericise_ignore=["all"])
            self.last_updated = time.time()
            logging.info("Finished updating database from web")
        except Exception as e:
            logging.warning("Unable to update Google Sheets", exc_info=True)

    def get_data(self, force_update):
        curr_time = time.time()
        if (not self.data or force_update):
            self.update_cache()
        # Do it asynchronously when time has expired
        elif (curr_time - self.last_updated > self.CACHE_TIME):
            update_thread = threading.Thread(target=self.update_cache)
            update_thread.start()

        return self.data


class SheetManager:
    def __init__(self):
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive",
        ]
        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                os.path.abspath("creds.json"), scope
            )
            client = gspread.authorize(creds)
            self.user_db = Sheet(
                client.open("User Database Basement").sheet1
            )  # Open the spreadhseet

            logging.info("User Database Loaded")
            self.activity_db = Sheet(client.open("Activity Log Entrepreneurship Center").sheet1)
            logging.info("Activity Database Loaded")
        except Exception as e:
            logging.warning(
                "An ERROR has ocurred connecting to google sheets", exc_info=True
            )
            raise Exception("Failed to connect to Google Sheets... check the wifi?")

    def get_user_db(self):
        return self.user_db.get_sheet()

    def get_activity_db(self):
        return self.activity_db.get_sheet()

    def get_user_db_data(self, force_update=False):
        return self.user_db.get_data(force_update)

    def get_activity_db_data(self, force_update=False):
        return self.activity_db.get_data(force_update)
