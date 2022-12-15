# save this as app.py
import json
from flask import Flask, render_template, request
from flask_table import Table, Col


app = Flask(__name__)
Admin = {
    "admin@gmail.com": "1234admin",
    }

User = {
    "aa@gmail.com": ["aa@gmail.com","aa"],
    "bb@gmail.com": ["bb@gmail.com","bb"],
    "cc@gmail.com": ["cc@gmail.com","cc"],
    }
TempUserId= []
TempUser= {}
Apps = ["a1","a2","a3","a4","a5","a6","a7","a8","a9","a10"]

UserAllow = {
    "aa@gmail.com":["aa@gmail.com",'a1','a10'],
    "bb@gmail.com":["bb@gmail.com",'a2','a3','a10'],
    "cc@gmail.com":["cc@gmail.com",'a4','a5','a10']
}
UserDeny = {
    "aa@gmail.com":["aa@gmail.com","a2","a3","a4","a5","a6","a7","a8","a9"],
    "bb@gmail.com":["bb@gmail.com","a1","a4","a5","a6","a7","a8","a9"],
    "cc@gmail.com":["cc@gmail.com","a1","a2","a3","a6","a7","a8","a9"]
}
Requests = []
print(Requests)




@app.route("/")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/user", methods=["POST"])
def user():
    id = request.form.get("mail")
    if id not in User:
        return render_template('Admin.html', request=Requests, user=User, app=Apps, tempuser=TempUserId, Error = "Error: **User Not Exist**")
    Req = []
    for user in Requests:
        if user[0] == id:
            Req.append(user[1])
    return render_template('admin1.html', allow=UserAllow[id], deny=UserDeny[id], req = Req)

@app.route("/logging", methods=["POST"])
def logging():
    profile = request.form.get("profile")
    id = request.form.get("email")
    pwd = request.form.get("pswd")
    if profile == "Admin":
        if id not in Admin:
            return render_template("login.html", Error = "Email Not Registered!")
        if pwd == Admin[id]:
            return render_template('Admin.html', request=Requests, user=User, app=Apps, tempuser=TempUserId)
        else:
            return render_template("login.html", Error = "Password Incorrect!")
    if profile == "User":
        if id in TempUserId:
            return render_template("login.html", Error = "Approval Pending!")
        if id not in User:
            return render_template("login.html", Error = "Email Not Registered!")
        if pwd == User[id][1]:
            Req = []
            for user in Requests:
                if user[0] == id:
                    Req.append(user[1])
            return render_template('home.html', allow=UserAllow[id], deny=UserDeny[id], req = Req)
        else:
            return render_template("login.html", Error = "Password Incorrect!")

@app.route("/registering", methods=["POST"])
def registering():
    id = request.form.get("email")
    pwd = request.form.get("pswd")
    cnfm = request.form.get("cnfm")
    if pwd != cnfm:
        return render_template("register.html", Error = "Password didn't match!")
    if id in TempUserId:
        return render_template("register.html", Error = "Approval Pending!")
    if id not in User:
        TempUser[id] = pwd
        TempUserId.append(id)
        print(TempUser)
        return render_template("register.html", Error = "Sent for approval!")
    return render_template("register.html", Error = "Email Already Exists!")

def access(id, app, allowed):
    UserData[id][app] = allowed

def remove(id):
    del UserData[id]

@app.route('/test', methods=['POST'])
def test():
    output = request.get_json()
    result = json.loads(output)
    id = result['id']
    app = result['app']
    for req in Requests:
        if req[0] == id:
            if req[1] == app:
                return output
    #for i in range(0,len(Requests),1):
    #    if Requests[i][0]==id and Requests[i][1]==app:
    #        return output*/
    Requests.append([id,app])
    UserDeny[id].remove(app)
    print(Requests)
    return output

@app.route('/cancel', methods=['POST'])
def cancel():
    output = request.get_json()
    result = json.loads(output)
    id = result['id']
    app = result['app']
    for req in Requests:
        if req[0] == id:
            if req[1] == app:
                Requests.remove([id,app])
                UserDeny[id].append(app)
    print(Requests)
    return output

@app.route('/update', methods=['POST'])
def update():
    output = request.get_json()
    result = json.loads(output)
    id = result['id']
    app = result['app']
    print(UserAllow[id])
    print(UserDeny[id])
    if app not in UserAllow[id]:
        UserAllow[id].append(app)
    print(UserAllow[id])
    print(UserDeny[id])
    Requests.remove([id,app])
    return Requests

@app.route('/revoke', methods=['POST'])
def revoke():
    output = request.get_json()
    result = json.loads(output)
    id = result['id']
    app = result['app']
    print(UserAllow[id])
    print(UserDeny[id])
    UserDeny[id].append(app)
    UserAllow[id].remove(app)
    print(UserAllow[id])
    print(UserDeny[id])
    return output

@app.route('/temp', methods=['POST'])
def temp():
    output = request.get_json()
    result = json.loads(output)
    id = result['id']
    pwd = TempUser[id]
    TempUser.pop(id)
    if id in User:
        return output
    if id in TempUserId:
        TempUserId.remove(id)
    User[id] = [id,pwd]
    UserAllow[id] = [id]
    UserDeny[id] = [id,"a1","a2","a3","a4","a5","a6","a7","a8","a10"]
    return output


@app.route('/urm', methods=['POST'])
def urm():
    output = request.get_json()
    result = json.loads(output)
    id = result['id']
    print(User)
    if id not in User:
        return output
    User.pop(id)
    UserAllow.pop(id)
    UserDeny.pop(id)
    print(User)
    return output

@app.route('/rmapp', methods=['POST'])
def rmapp():
    output = request.get_json()
    result = json.loads(output)
    id = result['id']
    print(Apps)
    print(UserDeny)
    print(UserAllow)
    if id in Apps:
        Apps.remove(id)
    for user in UserDeny.values():
        if id in user:
            user.remove(id)
    for user in UserAllow.values():
        if id in user:
            user.remove(id)
    print(Apps)
    print(UserDeny)
    print(UserAllow)
    return output
