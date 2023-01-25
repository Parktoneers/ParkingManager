import random
import sqlite3
from Account import Account
from Place import Place

class DatabaseHandler:

    db: sqlite3.Connection

    def __init__(self):

        self.db = sqlite3.connect("ParkingManager.db")
        cursor = self.db.cursor()

        q = """CREATE TABLE IF NOT EXISTS Accounts (
                       ID_1 INTEGER,
                       ID_2 INTEGER,     
                       ID_3 INTEGER,
                       ID_4 INTEGER,
                       Name VARCHAR(32),
                       Surname VARCHAR(32),
                       PhoneNumber VARCHAR(16),
                       ParkingSpace INTEGER,
                       PRIMARY KEY (ID_1, ID_2, ID_3, ID_4))"""

        cursor.execute(q)

        q2 = """CREATE TABLE IF NOT EXISTS Places (
                       ParkingSpace INTEGER,
                       Reserved INTEGER,
                       Occupied INTEGER,
                       PRIMARY KEY (ParkingSpace))"""
        cursor.execute(q2)
        self.db.commit()

    def populate(self):
        for i in range(1, 21):
            self.insertPlace(Place(i, 0, 0))
        accounts = [Account([54, 29, 127, 34], "john", "six", "666666666", None),
                    Account([251, 190, 167, 34], "andrew", "four", "444444444", None),
                    Account([187, 12, 152, 34], "bob", "two", "222222222", None),
                    Account([38, 12, 230, 34], "henry", "one", "111111111", None)]
        for acc in accounts:
            self.insertAccount(acc)

    def clear(self):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM Accounts")
        cursor.execute("DELETE FROM Places")
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

    def insertPlace(self, place: Place):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO Places VALUES (?, ?, ?)",
                       (place.parkingSpace, place.reserved, place.occupied))
        self.db.commit()


    def updateAccount(self, account: Account):
        cursor = self.db.cursor()
        params = (account.name, account.surname, account.phoneNumber, account.parkingSpace, account.uid[0], account.uid[1], account.uid[2], account.uid[3])
        q = f"""UPDATE Accounts SET 
                       Name = ?,
                       Surname = ?,
                       PhoneNumber = ?,
                       ParkingSpace = ?
                        WHERE 
                       ID_1 = ? AND 
                       ID_2 = ? AND 
                       ID_3 = ? AND 
                       ID_4 = ? """
        cursor.execute(q, params)
        self.db.commit()


    def updatePlace(self, place: Place):
        cursor = self.db.cursor()
        params = (place.occupied, place.reserved, place.parkingSpace)
        cursor.execute(f"""UPDATE Places SET 
                           Occupied = ?, Reserved = ?
                            WHERE 
                           ParkingSpace = ?""", params)
        self.db.commit()


    def deleteAccount(self, uid: [int, int, int, int] = None, phoneNumber: str = None):
        cursor = self.db.cursor()
        if uid is not None:
            params = (uid[0], uid[1], uid[2], uid[3])
            cursor.execute(f"""DELETE FROM Accounts WHERE 
                           ID_1 = ? AND 
                           ID_2 = ? AND 
                           ID_3 = ? AND 
                           ID_4 = ?""", params)
            self.db.commit()
            return
        if phoneNumber is not None:
            cursor.execute(f"DELETE FROM Accounts WHERE PhoneNumber = phoneNumber")
            self.db.commit()


    def deletePlace(self, place: Place):
        cursor = self.db.cursor()
        cursor.execute(f"DELETE FROM Places WHERE ParkingSpace = ?", (place.parkingSpace,))
        self.db.commit()

    def getPlace(self, parkingSpace):
        cursor = self.db.cursor()
        cursor.execute(f"SELECT * FROM Places WHERE ParkingSpace = ?", (parkingSpace,))
        place = cursor.fetchall()[0]
        return Place(place[0], place[1], place[2])


    def getFreePlace(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM Places WHERE Occupied = 0 AND Reserved = 0")
        places = cursor.fetchall()
        if len(places) == 0:
            return None
        index = random.randint(0, len(places) - 1)
        place = places[index]
        return Place(place[0], place[1], place[2])

    def getAccount(self, uid: [int, int, int, int] = None, phoneNumber: str = None):
        cursor = self.db.cursor()
        records: list = None
        if uid is not None:
            params = (uid[0], uid[1], uid[2], uid[3])
            cursor.execute(f"""SELECT * FROM Accounts WHERE
                           ID_1 = ? AND 
                           ID_2 = ? AND 
                           ID_3 = ? AND 
                            ID_4 = ? """, params)
            records = cursor.fetchall()

        if phoneNumber is not None:
            cursor.execute(f"SELECT * FROM Accounts WHERE PhoneNumber = ?", (phoneNumber,))
            records = cursor.fetchall()

        if records is None or len(records) < 1:
            return None

        row = records[0]
        return Account(uid=[row[0], row[1], row[2], row[3]],
                       name=row[4],
                       surname=row[5],
                       phoneNumber=row[6],
                       parkingSpace=row[7])
