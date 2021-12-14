from flask import Flask, jsonify, send_file
from flask import request
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

if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=7542) 
    app.run()