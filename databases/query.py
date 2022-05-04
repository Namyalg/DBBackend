import sqlite3

#conn = sqlite3.connect("person.db")
conn = sqlite3.connect("tables.db")
cur = conn.cursor()

cur.execute("""
    insert into GOV values ("India", "xyz")
""")

# cur.execute("""
#         insert into CENSUSCOLLECTOR VALUES("1", 23, "asian", 100, 40, "F", "India", "professor", "not married", 20, 0, "teacher", "India", 200)
# """)



# cur.execute("""
#         insert into JURISDICTION values ("Blore", "E3")
# """)
# conn.commit()

# cur.execute("""
#         select * from JURISDICTION
# """)

# cur.execute("""
#     drop table JURISDICTION
# """)

print(cur.fetchall())
conn.commit()
conn.close()