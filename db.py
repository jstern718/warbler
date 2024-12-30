import sqlite3

#Function for setting up warbler_db database.

try:
    db = sqlite3.connect('warbler_db')
    print('Connected to the SQLite database')
except:
    print('Error connecting to the SQLite database')

cursor = db.cursor()
