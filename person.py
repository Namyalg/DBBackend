from flask import Flask, jsonify, send_file
from flask import request
import sqlite3
from generate_data import integrate
from multi import multilevel_generalise
import json
import csv
from flask_cors import CORS

def get_person():
    connection = sqlite3.connect("databases/person.db")
    cursor = connection.cursor()
    cursor.execute("""
        select * from PERSON
    """)
    response = cursor.fetchall()
    connection.commit()
    connection.close()
    return {"response" : response}


def get_person_age(lage, hage):
    connection = sqlite3.connect("databases/person.db")
    cursor = connection.cursor()
    cursor.execute("""
        select * from PERSON where age >= :lage and age <= :hage
    """, {"lage" : lage, "hage" : hage})
    response = (cursor.fetchall())
    connection.commit()
    connection.close()
    return {"response" : response}


def get_person_workclass(wclass):
    connection = sqlite3.connect("databases/person.db")
    cursor = connection.cursor()
    cursor.execute("""
        select * from PERSON where workclass = :wclass
    """, {"wclass" : wclass})
    response = (cursor.fetchall())
    connection.commit()
    connection.close()
    return {"response" : response}

def insert_person():
    connection = sqlite3.connect("databases/person.db")
    cursor = connection.cursor()
    print(request.get_json())
    details = request.get_json()
    cursor.execute("""
        insert into PERSON values (:ano, :age, :race, :capital_loss, :hours, :sex, :native_country, :speciality, :marital_status, :edno, :fnlwgt, :workclass, :country, :capital_gain)
    """, {"ano" : details["ano"], "age" : details["age"], "race" : details["race"], "capital_loss" : details["capital_loss"], "hours": details["hours"], "sex" : details["sex"], "native_country" : details["native_country"], "speciality" : details["speciality"], "marital_status" : details["marital_status"], "edno" : details["edno"], "fnlwgt" : details["edno"], "workclass" : details["workclass"], "country" : details["country"], "capital_gain" : details["capital_gain"]})
    cursor.execute("""select * from PERSON """)
    response = (cursor.fetchall())
    connection.commit()
    connection.close()
    return {"response" : response}


