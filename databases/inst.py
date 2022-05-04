import sqlite3

conn = sqlite3.connect("tables.db")
cur = conn.cursor()

# cur.execute("""
#     create table TEST(age int)
# """)
# cur.execute("""
#     insert into TEST values(45)
# """)
# cur.execute("""
#     insert into CENSUSCOLLECTOR values("E10", 26, 24305, "India")
# """)

# cur.execute("""
#     insert into THIRDPARTY values("Tesla", "Automobile", "Manufacture", "India")
# """)
cur.execute("PRAGMA foreign_keys = ON")
cur.execute("PRAGMA foreign_keys")

# cur.execute("""
#     delete from CENSUSCOLLECTOR where empid="E01"
# """)

# cur.execute(""" 
#     insert into JURISDICTION values("E01", "bangalore")
# """)

# cur.execute("""
#     create table RECORDS(ano int, country text, date text, FOREIGN KEY(ano) REFERENCES PERSON(ano), FOREIGN KEY(country) REFERENCES GOV(country))
# """)
cur.execute("""
    insert into RECORDS values(4, "India", "12-10-2011")
""")

print(cur.fetchall())
conn.commit()
conn.close()