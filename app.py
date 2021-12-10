from flask import Flask
from flask import request
import json

app = Flask(__name__)

@app.route("/")
def hello_world():
    return ({"hello" : "world"})

@app.route("/access/<string:utype>/<string:operation>/<string:name>/<string:password>")
def login(utype, operation, name, password):
    print(utype, operation, name, password)
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
    app.run()