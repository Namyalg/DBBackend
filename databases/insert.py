import sqlite3

conn = sqlite3.connect("tables.db")

cur = conn.cursor()

# cur.execute("""
#     select * from CENSUSCOLLECTOR
# """)

#cur.execute('''DELETE FROM THIRDPARTY WHERE orgname = D''')

# cur.execute("""
#     insert into PERSON values ( 
#             "10",
#             30,
#             "Asian",
#             20,
#             20,
#             "Male",
#             "India",
#             "Singer",
#             "Married",
#             15,
#             0,
#             "Private",
#             "India",
#             0
#         )
# """)


cur.execute("""
    insert into EDUCATION values(10, "High School")
""")
conn.commit()
conn.close()