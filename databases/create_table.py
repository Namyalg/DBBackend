import sqlite3


conn = sqlite3.connect("table.db")
cur = conn.cursor()


cur.execute("""
        create table PROVIDES (country text, ano text, date DATE, FOREIGN KEY(country) references GOV(country), FOREIGN KEY(ano) references PARENT(ano)
        )
""")
# cur.execute("""
#         create table PERSON (ano text PRIMARY KEY UNIQUE NOT NULL, age integer, race text, capital_loss integer, hours integer, sex text, native_country text, speciality text, marital_status text, edno integer, fnlwgt integer, workclass text, country text, capital_gain integer)
# """)

# cur.execute("""create table GOV (country text PRIMARY KEY UNIQUE NOT NULL, census_officer text)
# """)

# cur.execute("""
#         drop table CENSUSCOLLECTOR
# """)
# cur.execute("""
#         create table CENSUSCOLLECTOR (empid text PRIMARY KEY NOT NULL, age integer, salary integer, country text, FOREIGN KEY(country) references GOV(country))
# """)

#cur.execute("drop table JURISDICTION")

#create table e2(a text, FOREIGN key (a) REFERENCES e1(a) on DELETE CASCADE)

# cur.execute("""
#         create table JURISDICTION (empid text, jurisdiction text, FOREIGN KEY(empid) references CENSUSCOLLECTOR(empid) ON DELETE CASCADE ON UPDATE CASCADE)
# """)

# cur.execute("""
#         create table THIRDPARTY (orgname text PRIMARY KEY UNIQUE NOT NULL, domain text, purpose text, country text, FOREIGN KEY(country) references GOV(country))
# """)

# cur.execute("""
#         create table EDUCATION (ano text, education text, FOREIGN KEY(ano) REFERENCES PERSON(ano))
# """)
conn.commit()
conn.close()