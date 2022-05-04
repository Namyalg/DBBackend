
from flask import Flask, jsonify, send_file
from flask import request
import sqlite3
from generate_data import integrate
from multi import multilevel_generalise
import json, time, random
import csv
from flask_cors import CORS

def insert_census_collector():
    try:
        details = request.get_json()
        print(details)

        connection = sqlite3.connect("databases/tables.db")
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
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
        return {"response" : response, "status" : 1}
    except sqlite3.OperationalError:
        time.sleep(random.randint(10, 30))
        return {"response " : "waiting, try again", "status" : 0}
    except sqlite3.IntegrityError:
        return {"response " : "Violation of Foreign Key constraint", "status" : 0}
    except:
        return {"response" : "An unexpected error occured", "status" : 0}

def delete_census_collector(empid):
    try:
        connection = sqlite3.connect("databases/tables.db")
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
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
        return {"response" : response, "status" : 1}
    except sqlite3.OperationalError:
        time.sleep(random.randint(10, 20))
        return {"response " : "waiting, try again", "status" : 0}
    except sqlite3.IntegrityError:
        return {"response " : "Violation of Foreign Key constraint", "status" : 0}
    except:
        return {"response" : "An unexpected error occured", "status" : 0}

def get_census_collector():
    try:
        connection = sqlite3.connect("databases/tables.db")
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("""
            select * from CENSUSCOLLECTOR
        """)
        response = cursor.fetchall()
        connection.commit()
        connection.close()
        return {"response" : response, "status" : 1}
    except sqlite3.OperationalError:
        time.sleep(random.randint(10, 20))
        return {"response " : "waiting, try again", "status" : 0}
    except sqlite3.IntegrityError:
        return {"response " : "Violation of Foreign Key constraint", "status" : 0}
    except:
        return {"response" : "An unexpected error occured", "status" : 0}