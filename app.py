from flask import Flask, jsonify, send_file
from flask import request
import sqlite3
from person import *
from jurisdiction import *
import random
import time
from thirdparty import *
from generate_data import integrate
from multi import multilevel_generalise
import json
from sac import sac_algorithm
from census import *
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

# implements the sac algorithm
@app.route("/custom/<int:records>/<int:k>")
#@crossdomain(origin='*',headers=['access-control-allow-origin','Content-Type'])
def get_sac(records, k):
    sac_algorithm(records, k)
    sac = convert_csv_to_arr("sac_result.csv")
    return {"sac" : sac}

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

#person related queries
@app.route("/person", methods=["GET"])
def getperson():
    return get_person()

@app.route("/person/age/<int:lage>/<int:hage>", methods=["GET"])
def getpersonage(lage, hage):
    return get_person_age(lage, hage)

@app.route("/person/workclass/<string:wclass>", methods=["GET"])
def getpersonworkclass(wclass):
    return get_person_workclass(wclass)

@app.route("/person", methods=["POST"])
def insertperson():
    return insert_person()
    

#census collector
@app.route("/census/", methods=["POST"])
def insertcensuscollector():
    return insert_census_collector()

@app.route("/census/<string:empid>", methods=["DELETE"])
def deletecensuscollector(empid):
    return delete_census_collector(empid)
   
@app.route("/census", methods=["GET"])
def getcensuscollector():
    return get_census_collector()


#jurisdiction
@app.route("/jurisdiction", methods=["GET"])
def getjurisdiction():
    return get_jurisdiction()

@app.route("/jurisdiction/<string:jurisdiction>", methods=["GET"])
def getjurisdictionbyid(jurisdiction):
    return get_jurisdiction_by_id(jurisdiction)

@app.route("/jurisdiction", methods=["POST"])
def insertjurisdiction():
    return insert_jurisdiction()
    

#third party
@app.route("/thirdparty", methods=["GET"])
def getthirdparty():
    return get_third_party()

@app.route("/thirdparty", methods=["POST"])
def insertthirdparty():
    return insert_third_party()

@app.route("/thirdparty/<string:orgname>", methods=["DELETE"])
def delthirdparty(orgname):
    return del_third_party(orgname)

@app.route("/thirdparty", methods=["PUT"])
def updatepurpose():
    return update_purpose()



@app.errorhandler(404)
def page_not_found(error):
    return {"status" : 0 , "message" : "Route not found, try another route"}

if __name__ == "__main__":
    app.run(debug=True, port=33507)
    #app.run(host="0.0.0.0", port=7542) 
    #app.run(use_reloader=True, debug=True)
