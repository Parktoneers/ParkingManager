import sqlite3

class DatabaseHandler():

    db: sqlite3.Connection
    def __init__(self):
        self.db = sqlite3.connect("ParkingManager.db")

    def insertAccount(self):
        pass

    def updateAccount(self):
        pass

    def deleteAccount(self):
        pass

