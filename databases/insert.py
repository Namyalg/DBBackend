import sqlite3

conn = sqlite3.connect("thirdparty.db")

cur = conn.cursor()

#cur.execute("""delete from THIRDPARTY values ("B pvt.ltd", "Clothes manufacture", "Setting up industry", "India")""")

cur.execute("""delete from THIRDPARTY where orgname = 'C pvt.ltd' """)

conn.commit()
conn.close()