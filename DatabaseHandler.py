import sqlite3

from Account import Account


class DatabaseHandler():

    db: sqlite3.Connection

    def __init__(self):

        self.db = sqlite3.connect("ParkingManager.db")
        cursor = self.db.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS Accounts ("
                       "ID_1 INTEGER,"
                       "ID_2 INTEGER,"
                       "ID_3 INTEGER,"
                       "ID_4 INTEGER,"
                       "Name VARCHAR(32),"
                       "Surname VARCHAR(32),"
                       "PhoneNumber VARCHAR(16)"
                       "ParkingSpace INTEGER,"
                       "PRIMARY KEY (ID_1, ID_2, ID_3, ID_4))")

        self.db.commit()

    def insertAccount(self, account: Account):

        cursor = self.db.cursor()

        cursor.execute("INSERT INTO Accounts VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (account.uid[0],
                        account.uid[1],
                        account.uid[2],
                        account.uid[3],
                        account.name,
                        account.surname,
                        account.phoneNumber,
                        account.parkingSpace))

        self.db.commit()

    def updateAccount(self, account: Account):
        cursor = self.db.cursor()
        cursor.execute("UPDATE Accounts SET "
                       "Name = ?,"
                       "Surname = ?,"
                       "PhoneNumber = ?,"
                       "ParkingSpace = ?"
                       " WHERE "
                       "ID_1 = ? AND "
                       "ID_2 = ? AND "
                       "ID_3 = ? AND "
                       "ID_4 = ?",
                       (account.name,
                        account.surname,
                        account.phoneNumber,
                        account.parkingSpace,
                        account.uid[0],
                        account.uid[1],
                        account.uid[2],
                        account.uid[3]))

        self.db.commit()

    def deleteAccount(self, uid: [int, int, int, int] = None, phoneNumber: str = None):

        cursor = self.db.cursor()

        if uid is not None:
            cursor.execute("DELETE FROM Accounts WHERE "
                           "ID_1 = ? AND "
                           "ID_2 = ? AND "
                           "ID_3 = ? AND "
                           "ID_4 = ?",
                           (uid[0],
                            uid[1],
                            uid[2],
                            uid[3]))

            self.db.commit()
            return

        if phoneNumber is not None:
            cursor.execute("DELETE FROM Accounts WHERE PhoneNumber = ?", phoneNumber)
            self.db.commit()

    def getAccount(self, uid: [int, int, int, int], phoneNumber: str):

        cursor = self.db.cursor()
        records: list = None

        if uid is not None:
            cursor.execute("SELECT * FROM Accounts WHERE"
                           "ID_1 = ? AND "
                           "ID_2 = ? AND "
                           "ID_3 = ? AND "
                           "ID_4 = ?",
                           (uid[0],
                            uid[1],
                            uid[2],
                            uid[3]))
            records = cursor.fetchall()

        if phoneNumber is not None:
            cursor.execute("SELECT * FROM Accounts WHERE PhoneNumber = ?", phoneNumber)
            records = cursor.fetchall()

        if records is None or len(records) < 1:
            return None

        row = records[0]
        return Account(uid=[row[0], row[1], row[2], row[3]],
                       name=row[4],
                       surname=row[5],
                       phoneNumber=row[6],
                       parkingSpace=row[7])
