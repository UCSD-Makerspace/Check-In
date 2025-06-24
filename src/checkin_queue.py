import time
import logging
from threading import Thread
import global_

class CheckInLogger:
    def __init__(self):
        self.queue = []
        self.last_scan_time = 0
        self.last_UUID = None
        self.writer_thread = Thread(target=self._queue_writer, daemon = True)
        self.writer_thread.start()

    def enqueue_row(self, row, tag):
            now = time.time()
            if tag != self.last_UUID or now - self.last_scan_time > 5:
                self.queue.append(row)
                self.last_scan_time = now
                self.last_UUID = tag
                logging.debug(f"Enqueued row: {row}")

    def _queue_writer(self):
            while True:
                time.sleep(1)
                now = time.time()
                if self.queue and now - self.last_scan_time > 5:
                    row = self.queue.pop(0)
                    try:
                        global_.sheets.get_activity_db().append_row(row)
                        logging.debug(f"Row written to Google Sheets: {row}")
                        time.sleep(3)
                    except Exception as e:
                        logging.error("Error writing row from queue for tag {row[3]}")
                        # Reinsert after popping in case of failing a write
                        self.queue.insert(0, row)
        
