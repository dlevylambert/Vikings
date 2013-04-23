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
        if request.form.has_key("tabsignup"):
            return redirect(url_for("signup"))
        if request.form.has_key("tabcreate"):
            return redirect(url_for("create"))
        if request.form.has_key("tabprofile"):
            return redirect(url_for("profile"))
        if request.form.has_key("tabsurvey"):
            return redirect(url_for("survey"))
        if request.form.has_key("tabresults"):
            return redirect(url_for("results"))
            
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
        if request.form.has_key("tabsignup"):
            return redirect(url_for("signup"))
        if request.form.has_key("tabcreate"):
            return redirect(url_for("create"))
        if request.form.has_key("tabprofile"):
            return redirect(url_for("profile"))
        if request.form.has_key("tabsurvey"):
            return redirect(url_for("survey"))
        if request.form.has_key("tabresults"):
            return redirect(url_for("results"))

@app.route("/results", methods=["POST", "GET"])
def results():
    if request.method=="GET":
        return render_template("results.html")
    else:
        if request.form.has_key("tablogin"):
            return redirect(url_for("login"))
        if request.form.has_key("tabhome"):
            return redirect(url_for("home"))
        if request.form.has_key("tabsignup"):
            return redirect(url_for("signup"))
        if request.form.has_key("tabcreate"):
            return redirect(url_for("create"))
        if request.form.has_key("tabprofile"):
            return redirect(url_for("profile"))
        if request.form.has_key("tabsurvey"):
            return redirect(url_for("survey"))
        if request.form.has_key("tabresults"):
            return redirect(url_for("results"))


@app.route("/signup",methods=["POST","GET"])
def signup():
    if request.method=="GET":
        return render_template("signup.html")
    else:
        if request.form.has_key("submitsignup"):
            user = str(request.form["Username"])
            password = str(request.form["Password"])
            validate = util.createUser(user,password)
            if validate == 0:
                print "no"
                return render_template("signup.html", failure = True)
            if validate == True:
                session['user'] = user
                print "worked"
                return redirect(url_for("home"))
            if validate == False:
                print "no"
                return render_template("signup.html", failure = True)
        if request.form.has_key("tablogin"):
            return redirect(url_for("login"))
        if request.form.has_key("tabhome"):
            return redirect(url_for("home"))
        if request.form.has_key("tabsignup"):
            return redirect(url_for("signup"))
        if request.form.has_key("tabcreate"):
            return redirect(url_for("create"))
        if request.form.has_key("tabprofile"):
            return redirect(url_for("profile"))
        if request.form.has_key("tabsurvey"):
            return redirect(url_for("survey"))
        if request.form.has_key("tabresults"):
            return redirect(url_for("results"))

@app.route("/profile",methods=["POST","GET"])
def profile():
    if request.method=="GET":
        return render_template("profile.html")
    else:
        if request.form.has_key("tablogin"):
            return redirect(url_for("login"))
        if request.form.has_key("tabhome"):
            return redirect(url_for("home"))
        if request.form.has_key("tabsignup"):
            return redirect(url_for("signup"))
        if request.form.has_key("tabcreate"):
            return redirect(url_for("create"))
        if request.form.has_key("tabprofile"):
            return redirect(url_for("profile"))
        if request.form.has_key("tabsurvey"):
            return redirect(url_for("survey"))
        if request.form.has_key("tabresults"):
            return redirect(url_for("results"))

@app.route("/survey",methods=["POST","GET"])
def survey():
    if request.method=="GET":
        return render_template("survey.html")
    else:
        if request.form.has_key("tablogin"):
            return redirect(url_for("login"))
        if request.form.has_key("tabhome"):
            return redirect(url_for("home"))
        if request.form.has_key("tabsignup"):
            return redirect(url_for("signup"))
        if request.form.has_key("tabcreate"):
            return redirect(url_for("create"))
        if request.form.has_key("tabprofile"):
            return redirect(url_for("profile"))
        if request.form.has_key("tabsurvey"):
            return redirect(url_for("survey"))
        if request.form.has_key("tabresults"):
            return redirect(url_for("results"))

@app.route("/create",methods=["POST","GET"])
def create():
    if request.method=="GET":
        return render_template("create.html")
    else:
        if request.form.has_key("tablogin"):
            return redirect(url_for("login"))
        if request.form.has_key("tabhome"):
            return redirect(url_for("home"))
        if request.form.has_key("tabsignup"):
            return redirect(url_for("signup"))
        if request.form.has_key("tabcreate"):
            return redirect(url_for("create"))
        if request.form.has_key("tabprofile"):
            return redirect(url_for("profile"))
        if request.form.has_key("tabsurvey"):
            return redirect(url_for("survey"))
        if request.form.has_key("tabresults"):
            return redirect(url_for("results"))

if __name__ == "__main__":
    app.run(debug=True)
