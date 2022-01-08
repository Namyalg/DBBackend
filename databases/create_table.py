import sqlite3

#conn = sqlite3.connect("person.db")
conn = sqlite3.connect("provides.db")
cur = conn.cursor()


cur.execute("""
        create table PROVIDES (country text, ano text, date DATE, FOREIGN KEY(country) references PARENT(GOV), FOREIGN KEY(ano) references PARENT(PERSON)
        )
""")
# cur.execute("""
#         create table PERSON (ano text PRIMARY KEY UNIQUE, age integer, race text, capital_loss integer, hours integer, sex text, native_country text, speciality text, marital_status text, edno integer, fnlwgt integer, workclass text, country text, capital_gain integer)
# """)

# cur.execute("""create table GOV (country text PRIMARY KEY UNIQUE, census_officer text)
# """)

# cur.execute("""
#         create table CENSUSCOLLECTOR (empid text PRIMARY KEY UNIQUE, age integer, salary integer, country text, FOREIGN KEY(country) references parent(GOV))
# """)


# cur.execute("""
#         create table JURISDICTION (empid text, jurisdiction text, FOREIGN KEY(empid) references PARENT(CENSUSCOLLECTOR))
# """)

# cur.execute("""
#         create table THIRDPARTY (orgname text PRIMARY KEY UNIQUE, domain text, purpose text, country text, FOREIGN KEY(country) references PARENT(GOV))
# """)

# cur.execute("""
#         create table EDUCATION (ano text, education text, FOREIGN KEY(ano) REFERENCES PARENT(PERSON))
# """)
conn.commit()
conn.close()