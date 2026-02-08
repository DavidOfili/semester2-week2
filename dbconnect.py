import sqlite3

connection = sqlite3.connect("university.db")

cursor = connection.cursor()
result = cursor.execute("SELECT * FROM Department")

for data in result:
    print(data)