
def insert_census_collector():
    details = request.get_json()
    print(details)

    connection = sqlite3.connect("databases/censuscollector.db")
    cursor = connection.cursor()
    cursor.execute("""
        insert into CENSUSCOLLECTOR values(:empid, :age, :salary, :country)
    """, {"empid" : details['empid'], "age" : details['age'], "salary" : details['salary'], "country" : details['country']})
    # # response = (cursor.fetchall())
    cursor.execute("""
        select * from CENSUSCOLLECTOR
    """)
    response = cursor.fetchall()
    connection.commit()
    connection.close()
    return {"response" : response}

def delete_census_collector(empid):
    connection = sqlite3.connect("databases/censuscollector.db")
    cursor = connection.cursor()
    cursor.execute("""select * from CENSUSCOLLECTOR""")
    print(cursor.fetchall())
    cursor.execute("""
        delete from CENSUSCOLLECTOR where empid = :empid
    """, {"empid" : empid})
    cursor.execute("""
        select * from CENSUSCOLLECTOR
    """)
    response = cursor.fetchall()
    connection.commit()
    connection.close()
    return {"response" : response}


def get_census_collector():
    connection = sqlite3.connect("databases/censuscollector.db")
    cursor = connection.cursor()
    cursor.execute("""
        select * from CENSUSCOLLECTOR
    """)
    response = cursor.fetchall()
    connection.commit()
    connection.close()
    return {"response" : response}