#!/usr/bin/python3
import time

import MQTTHandler
from DatabaseHandler import DatabaseHandler


def go():
    db = DatabaseHandler()
    # db.clear()
    # db.populate()
    MQTTHandler.run()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        db.db.close()


if __name__ == "__main__":
    go()
