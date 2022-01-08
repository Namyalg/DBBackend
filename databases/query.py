import sqlite3

#conn = sqlite3.connect("person.db")
conn = sqlite3.connect("person.db")
cur = conn.cursor()


cur.execute("""
        insert into PERSON VALUES("1", 23, "asian", 100, 40, "F", "India", "professor", "not married", 20, 0, "teacher", "India", 200)
""")

conn.commit()

cur.execute("""
        select * from PERSON
""")

print(cur.fetchall())
conn.commit()
conn.close()