import util, json
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

@app.route("/getquestions")
def getquestions():
    surveyname = request.args.get('surveyname', '') #write JS method for this
    return json.dumps(util.getSurveyQs(surveyname)) #this too

@app.route("/getnames")
def getnames():
    return json.dumps(util.getSurveyNames())

@app.route("/matchfind")
def matchfind():
    surveyname = request.args.get('surveyname', '') #write JS method for this
    username = session['user']
    return json.dumps(util.match(surveyname, username))

@app.route("/submitSurvey")
def submitSurvey():
    surveyname = request.args.get('surveyname', '')
    ans = request.args.get('ans', '').split(",")
    username = session['user']
    print surveyname, ans, username
    return util.takeSurvey(surveyname, username, ans)


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
        if 'user' not in session:
            return redirect(url_for("login"))
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
            age = str(request.form["Username"])
            realname = str(request.form["Username"])
            gender = str(request.form["Username"])
            hobbies = str(request.form["Username"])
            validate = util.createUser(user,password,age,realname,gender,hobbies)
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
        if 'user' not in session:
            return redirect(url_for("login"))
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
        if 'user' not in session:
            return redirect(url_for("login"))
        return render_template("survey.html", surveynames = util.getSurveyNames())
    else:
        button = request.form['button']
        if button == "Submit":
            return redirect(url_for("survey"))
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
        if 'user' not in session:
            return redirect(url_for("login"))
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
        if request.form.has_key("submitcreate"):
            surveyname = str(request.form['surveyname'])
            questions = []
            for i in range(1, 6):
                questions.append([str(request.form['q'+str(i)]), str(request.form['q'+str(i)+'type'])])
            print surveyname, questions
            util.createSurvey(surveyname, questions)
            return redirect(url_for('create'))

if __name__ == "__main__":
    #for each question, list format is [question, question type: either number or word]
    app.run(debug=True, port=6565)
    util.createSurvey('roommate', [['How much of a night owl are you?', 'number'],['On a scale of 1 to 5, how quiet do you want your room to be?', 'number'],['How much to you agree with the following statement: I will spend most of my free time in my room.', 'word'],['How much to you agree with the following statement: " always have friends over.', 'word'],['How much do you agree with the following statement: I need my room to be clean and organized.', 'word']])
