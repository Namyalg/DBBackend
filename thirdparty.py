from flask import Flask, jsonify, send_file
from flask import request
import sqlite3
from generate_data import integrate
from multi import multilevel_generalise
import json, time, random
import csv
from flask_cors import CORS


def get_third_party():
    try:
        connection = sqlite3.connect("databases/tables.db")
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("""select * from THIRDPARTY""")
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


def insert_third_party():
    try:
        connection = sqlite3.connect("databases/tables.db")
        print(request.get_json())
        details = request.get_json()
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        #cursor.execute("""INSERT INTO WORK VALUES (:f, :l, :p)""", {"f" : det['f'], "l" : det['l'], "p" : det['p']})
        cursor.execute("""INSERT INTO THIRDPARTY VALUES (:orgname, :domain, :purpose, :country)""", {"orgname" : details['orgname'], 
            "domain" : details['domain'], "purpose" : details['purpose'], 
            "country" : details['country']})   

        cursor.execute("""
            select * from THIRDPARTY
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



def del_third_party(orgname):
    try:
        connection = sqlite3.connect("databases/tables.db")
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("""delete from THIRDPARTY where orgname = :org""", {"org" : orgname})   

        cursor.execute("""
            select * from THIRDPARTY
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


def update_purpose():
    try:
        connection = sqlite3.connect("databases/tables.db")
        print(request.get_json())
        details = request.get_json()
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("""update THIRDPARTY SET purpose = :purpose where orgname = :orgname""", {"orgname" : details["orgname"], "purpose" : details["purpose"]})   
        cursor.execute("""
            select * from THIRDPARTY
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
