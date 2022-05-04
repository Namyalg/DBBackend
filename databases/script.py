import sqlite3

conn = sqlite3.connect("tables.db")
cur = conn.cursor()

cur.execute("PRAGMA foreign_keys = ON")
cur.execute("PRAGMA foreign_keys")

# cur.execute("""
#     create table TEST(age int)
# """)
# cur.execute("""
#     insert into TEST values(45)
# """)
cur.execute("""
    delete from TEST where age=12
""")

print(cur.fetchall())
conn.commit()
conn.close()