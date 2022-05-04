import sqlite3

connection = sqlite3.connect("thirdparty.db")

cursor = connection.cursor()

# fname = input("Enter the first name ")
# lname = input("Enter the last name ")
# pay = input("Enter the pay ")

cursor.execute(""" CREATE TABLE  (FName TEXT, LName TEXT, pay INTEGER)""")
#cursor.execute("""INSERT INTO WORK VALUES (:f, :l, :p)""", {"f" : fname, "l" : lname, "p" : pay})

cursor.execute("""INSERT INTO work VALUES (:f, :l, :p)""", {"f" : "fname", "l" : "lname", "p" : "pay"})   
cursor.execute("""SELECT * FROM WORK""")

print(cursor.fetchall())

connection.commit()

connection.close()