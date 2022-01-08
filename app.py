from flask import Flask, jsonify, send_file
from flask import request
import sqlite3
from generate_data import integrate
from multi import multilevel_generalise
import json
import csv
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
#@crossdomain(origin='*',headers=['access-control-allow-origin','Content-Type'])
def hello_world():
    return "<p>Hello world</p>"


@app.route("/multi/<int:sz>/<int:k>")
#@crossdomain(origin='*',headers=['access-control-allow-origin','Content-Type'])
def get_multi_table(sz, k):
    multilevel_generalise(sz, k)
    mlevel = convert_csv_to_arr("result.csv")
    return {"multi_level" : mlevel}



@app.route("/table/<int:sz>/<int:k>/<int:doblvl>/<int:wclasslvl>")
#@crossdomain(origin='*',headers=['access-control-allow-origin','Content-Type'])
def get_table(sz, k, doblvl, wclasslvl):
    integrate(sz, k, doblvl, wclasslvl)
    with_suppression = convert_csv_to_arr("with_suppression.csv")
    without_suppression = convert_csv_to_arr("without_suppression.csv")
    private_table = convert_csv_to_arr("sample.csv")
    return {"with_suppression" : with_suppression, "without_suppression" : without_suppression, "private_table" : private_table}


@app.route("/image/<int:sz>/<int:k>")
#@crossdomain(origin='*',headers=['access-control-allow-origin','Content-Type'])
def get_plot(sz, k):
    return send_file("plot.png", mimetype='image/png')
    return "<p>Return plot</p>"
    
def convert_csv_to_arr(path):
    rows = []
    with open(path, 'r') as file:
        csvreader = csv.reader(file)
        # header = next(csvreader)
        for row in csvreader:
            rows.append(row) 
        return rows
    return []

@app.route("/test")
#@crossdomain(origin='*',headers=['access-control-allow-origin','Content-Type'])
def table():
    return "<p>Testing</p>"

@app.route("/access/<string:utype>/<string:operation>/<string:name>/<string:password>")
#@crossdomain(origin='*',headers=['access-control-allow-origin','Content-Type'])
def login(utype, operation, name, password):
    with open('login.json') as fobj:
        data = json.load(fobj)
        admin = data['admin']
        guest = data['guest']
        if utype == "admin":
            for k, v in admin.items():
                if v['name'] == name and v['password'] == password:
                    return ({"status" : 1, "msg" : "admin login success"})
            else:
                return {"status" : 0, "msg" : "admin login failure"}

        if utype == "guest":
            if operation == "login":
                for k, v in guest.items():
                    if v['name'] == name and v['password'] == password:
                        print("login success ful")
                        return ({"status" : 1, "msg" : "guest login success"})
                else:
                    return ({"status" : 0, "msg" : "guest login failure"})
            if operation == "signup":
                try:
                    guest[str(len(guest))] = {'name' : name, 'password' : password}
                    details = dict()
                    details["admin"] = admin 
                    details["guest"] = guest
                    file = open("login.json", "r+")
                    file.truncate(0)
                    json.dump(details, file, indent = 4)
                    file.close()
                    return {"status" : 1,  "msg" : "guest signup success"}
                except:
                     return {"status" : 0,  "msg" : "guest signup failure"}

    return ({"status" : 0, "msg" : "no operation", "place" : [utype, operation, name, password]})


@app.route("/", methods=["POST"])
def post_test():
    connection = sqlite3.connect("databases/thirdparty.db")
    print(request.get_json())
    details = request.get_json()
    cursor = connection.cursor()
    print("contents")
    
    #cursor.execute("""INSERT INTO WORK VALUES (:f, :l, :p)""", {"f" : det['f'], "l" : det['l'], "p" : det['p']})
    cursor.execute("""INSERT INTO THIRDPARTY VALUES (:org, :domain, :purpose, :country)""", {"org" : details['org'], 
        "domain" : details['domain'], "purpose" : details['purpose'], 
        "country" : details['country']})   

    cursor.execute("""select * from THIRDPARTY""")
    print(cursor.fetchall())
    connection.commit()
   
    connection.close()

    print(request.method)
    
    return {"fname" : "d"}


@app.route("/<string:orgname>", methods=["DELETE"])
def del_test(orgname):
    connection = sqlite3.connect("databases/thirdparty.db")
    print(request.get_json())
    details = request.get_json()
    cursor = connection.cursor()
    print("contents")
    
    #cursor.execute("""INSERT INTO WORK VALUES (:f, :l, :p)""", {"f" : det['f'], "l" : det['l'], "p" : det['p']})
    cursor.execute("""delete from THIRDPARTY where orgname = :org""", {"org" : orgname})   

    cursor.execute("""select * from THIRDPARTY""")
    print(cursor.fetchall())
    connection.commit()
    connection.close()
    print(request.method)
    return {"fname" : "d"}


#person related queries
@app.route("/person", methods=["GET"])
def get_person():
    connection = sqlite3.connect("databases/person.db")
    cursor = connection.cursor()
    cursor.execute("""
        select * from PERSON
    """)
    p = (cursor.fetchall())
    connection.commit()
    connection.close()
    return {"response" : p}


@app.route("/person/age/<int:lage>/<int:hage>", methods=["GET"])
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

@app.route("/person/workclass/<string:wclass>", methods=["GET"])
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

#census collector
@app.route("/census/", methods=["POST"])
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
    print(cursor.fetchall())
    connection.commit()
    connection.close()
    return {"response" : []}

@app.route("/census/<string:empid>", methods=["DELETE"])
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

    print(cursor.fetchall())
    connection.commit()
    connection.close()
    return {"response" : []}


if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=7542) 
    app.run()