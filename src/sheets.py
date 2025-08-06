import time
import gspread
import os
import logging
from oauth2client.service_account import ServiceAccountCredentials


class Sheet:
    CACHE_TIME = 60 * 30

    def __init__(self, db):
        self.db = db
        self.data = None
        self.last_updated = time.time()

    def get_sheet(self):
        return self.db

    def get_data(self, force_update):
        curr_time = time.time()
        if (
            not self.data
            or force_update
            or curr_time - self.last_updated > self.CACHE_TIME
        ):
            try:
                logging.info("Writing to Google Sheets")
                try:
                    self.data = self.db.get_all_records(numericise_ignore=["all"])
                except gspread.exceptions.GSpreadException as e:
                    if "header row in the worksheet is not unique" in str(e):
                        logging.warning("Duplicate headers found, attempting to get raw values")
                        all_values = self.db.get_all_values()
                        if all_values:
                            headers = all_values[0]
                            seen_headers = set()
                            duplicates = []
                            for header in headers:
                                if header in seen_headers:
                                    duplicates.append(header)
                                seen_headers.add(header)
                            if duplicates:
                                logging.error(f"Duplicate headers found: {duplicates}")

                            records = [] 
                            for row_values in all_values[1:]:
                                record = {}
                                header_counts = {}
                                for i, header in enumerate(headers):
                                    if header in header_counts:
                                        header_counts[header] += 1
                                        unique_header = f"{header}_{header_counts[header]}"
                                    else:
                                        header_counts[header] = 1
                                        unique_header = header
                                    
                                    if i < len(row_values):
                                        record[unique_header] = row_values[i]
                                    else:
                                        record[unique_header] = ""
                                records.append(record)
                            self.data = records
                        else:
                            raise e
                    else:
                        raise e
                self.last_updated = curr_time
            except Exception as e:
                logging.warning("Unable to update Google Sheets", exc_info=True)
                if self.data is None:
                    raise e

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
                client.open("User Database").sheet1
            )  # Open the spreadhseet

            logging.info("User Database Loaded")
            self.activity_db = Sheet(
                client.open_by_url(
                    "https://docs.google.com/spreadsheets/d/1aLBb1J2ifoUG2UAxHHbwxNO3KrIIWoI0pnZ14c5rpOM/edit?usp=drive_web&ouid=104398832910104737872"
                ).sheet1
            )
            logging.info("Activity Database Loaded")
            self.waiver_db = Sheet(client.open("Waiver Signatures").sheet1)
            logging.info("Waiver Database Loaded")
        except Exception as e:
            logging.warning(
                "An ERROR has ocurred connecting to google sheets", exc_info=True
            )
            raise Exception("Failed to connect to Google Sheets... check the wifi?")

    def get_user_db(self):
        return self.user_db.get_sheet()

    def get_activity_db(self):
        return self.activity_db.get_sheet()

    def get_waiver_db(self):
        return self.waiver_db.get_sheet()

    def get_user_db_data(self, force_update=False):
        return self.user_db.get_data(force_update)

    def get_activity_db_data(self, force_update=False):
        return self.activity_db.get_data(force_update)

    def get_waiver_db_data(self, force_update=False):
        return self.waiver_db.get_data(force_update)
