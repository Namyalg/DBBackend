import sqlite3

conn = sqlite3.connect("thirdparty.db")

cur = conn.cursor()

cur.execute("""
        create table THIRDPARTY (orgname text, domain text, purpose, country text)
""")

conn.commit()
conn.close()