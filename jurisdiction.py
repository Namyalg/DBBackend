from flask import Flask, jsonify, send_file
from flask import request
import sqlite3
from generate_data import integrate
from multi import multilevel_generalise
import json
import time, random
import csv
from flask_cors import CORS

def get_jurisdiction():
    try:
        connection = sqlite3.connect("databases/tables.db")
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("""select * from JURISDICTION""")
        response = cursor.fetchall()
        connection.commit()
        connection.close()
        return {"response" : response, "status" : 1}
    except sqlite3.OperationalError:
        time.sleep(random.randint(10, 20))
        return {"response " : "waiting, try again", "status" : 0}
    except sqlite3.IntegrityError:
        return {"response " : "Violation of Foreign Key constraint", "status" : 0 }
    except:
        return {"response" : "An unexpected error occured",  "status" : 0}

def get_jurisdiction_by_id(j):
    try:
        connection = sqlite3.connect("databases/tables.db")
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("""select empid from JURISDICTION where jurisdiction = :j""", {"j" : j})
        response = cursor.fetchall()
        connection.commit()
        connection.close()
        return {"response" : response, "status" : 1}
    except sqlite3.OperationalError:
        time.sleep(random.randint(10, 20))
        return {"response " : "waiting, try again",  "status" : 0}
    except sqlite3.IntegrityError:
        return {"response " : "Violation of Foreign Key constraint",  "status" : 0}
    except:
        return {"response" : "An unexpected error occured",  "status" : 0}


def insert_jurisdiction():
    try:
        connection = sqlite3.connect("databases/tables.db")
        details = request.get_json()
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("""insert into JURISDICTION values(:empid, :loc)""", {"empid" : details["empid"], "loc" : details['jurisdiction']})
        cursor.execute("""select empid from JURISDICTION""")
        response = cursor.fetchall()
        connection.commit()
        connection.close()
        return {"response" : response,  "status" : 1}
    except sqlite3.OperationalError:
        time.sleep(random.randint(10, 20))
        return {"response " : "waiting, try again",  "status" : 0}
    except sqlite3.IntegrityError:
        return {"response " : "Violation of Foreign Key constraint",  "status" : 0}
    except:
        return {"response" : "An unexpected error occured",  "status" : 0}