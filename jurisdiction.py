from flask import Flask, jsonify, send_file
from flask import request
import sqlite3
from generate_data import integrate
from multi import multilevel_generalise
import json
import csv
from flask_cors import CORS

def get_jurisdiction():
    connection = sqlite3.connect("databases/tables.db")
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("""select * from JURISDICTION""")
    response = cursor.fetchall()
    connection.commit()
    connection.close()
    return {"response" : response}

def get_jurisdiction_by_id(j):
    connection = sqlite3.connect("databases/tables.db")
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("""select empid from JURISDICTION where jurisdiction = :j""", {"j" : j})
    response = cursor.fetchall()
    connection.commit()
    connection.close()
    return {"response" : response}


def insert_jurisdiction():
    connection = sqlite3.connect("databases/tables.db")
    details = request.get_json()
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("""insert into JURISDICTION values(:loc, :empid)""", {"empid" : details["empid"], "loc" : details['jurisdiction']})
    cursor.execute("""select empid from JURISDICTION""")
    response = cursor.fetchall()
    connection.commit()
    connection.close()
    return {"response" : response}