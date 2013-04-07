import util
from flask import request,Flask,render_template, url_for,redirect,request,session

app = Flask(__name__)
app.secret_key = "vikingsrock"

@app.route("/", methods = ["GET", "POST"])
def hello():
    if request.method == "GET":
        return redirect(url_for("home"))

@app.route("/home", methods = ["GET", "POST"])
def home():
    if request.method=="GET":
        return render_template("home.html")
    else:
        if request.form.has_key("tablogin"):
            return redirect(url_for("login"))
        if request.form.has_key("tabhome"):
            return redirect(url_for("home"))
            
@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=="GET":
        return render_template("login.html")	
    else:
        if request.form.has_key("submitlogin"):
            user = str(request.form["Username"])
            password = str(request.form["Password"])
            validate = util.checkUserPass(user,password)
            if validate == 0:
                print "no"
                return render_template("login.html")
            if validate == True:
                session['user'] = user
                print "worked"
                return redirect(url_for("home"))
            if validate == False:
                print "no"
                return render_template("login.html")
        if request.form.has_key("tablogin"):
            return redirect(url_for("login"))
        if request.form.has_key("tabhome"):
            return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
