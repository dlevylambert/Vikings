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
            return redirect(url_for("myprofile"))
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
    print surveyname, username
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
            return redirect(url_for("myprofile"))
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
            return redirect(url_for("myprofile"))
        if request.form.has_key("tabsurvey"):
            return redirect(url_for("survey"))
        if request.form.has_key("tabresults"):
            return redirect(url_for("results"))

@app.route("/getUserInfo")
def getUserInfo():
    username = session["user"]
    print util.getUser(username)
    return json.dumps(util.getUser(username))

@app.route("/getOtherInfo")
def getOtherInfo():
    otherUser = request.args.get("otherUser", "").strip()
    print otherUser #to make sure we're looking for the right other user
    return json.dumps(util.getUser(otherUser))

@app.route("/signup",methods=["POST","GET"])
def signup():
    if request.method=="GET":
        return render_template("signup.html")
    else:
        # adding some testing functions for signing up users
        # DK: UPDATE, 12:35 PM 4/30. Saving profiles works. For some reason, my dkurk account saved every field as 'dkurk' and I was worried but it looks like this was fixed along the way!
        if request.form.has_key("submitsignup"):
            user = str(request.form["Username"])
            #print user
            password = str(request.form["Password"])
            #print password
            age = str(request.form["Age"])
            #print age
            realname = str(request.form["RealName"])
            #print realname
            gender = str(request.form["Gender"])
            #print gender
            hobbies = str(request.form["Hobbies"])
            #print hobbies
            youtube = str(request.form["Youtube"])
            print youtube
            reached = False
            i = 0
            youtubeID=""
            index = youtube.find('=')
            #print index
            if (index):
                youtubeID= youtube[index + 1:len(youtube)]
            #for letter in youtube:
                #if (reached):
                    #youtubeID=youtubeID + letter
                    #if (letter == "=")
                    #reached = True
                    #if (reached == False):
                    #youtubeID="9ZEURntrQOg"
                    #print youtubeID
                    #validate = util.createUser(user,password,age,realname,gender,hobbies)
            validate = util.createUser(user,password,age,realname,gender,hobbies,youtubeID)
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
            return redirect(url_for("myprofile"))
        if request.form.has_key("tabsurvey"):
            return redirect(url_for("survey"))
        if request.form.has_key("tabresults"):
            return redirect(url_for("results"))

@app.route("/myprofile",methods=["POST","GET"])
def myprofile():
    if request.method=="GET":
        if 'user' not in session:
            return redirect(url_for("login"))
        #return render_template("profile.html", user=session['user'])
        return render_template("myprofile.html")
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
            return redirect(url_for("myprofile"))
        if request.form.has_key("tabsurvey"):
            return redirect(url_for("survey"))
        if request.form.has_key("tabresults"):
            return redirect(url_for("results"))

@app.route("/getsong")
def getsong():
    username = session["user"]
    print "username: " + username
    return json.dumps(util.getSong(username))

@app.route("/getsongother")
def getsongother():
    otherUser = request.args.get("otherUser", "").strip()
    return json.dumps(util.getSong(otherUser))

@app.route("/profile/<user>",methods=["POST","GET"])
def profile(user=None):
    if request.method=="GET":
        if 'user' not in session:
            return redirect(url_for("login"))
        #return render_template("profile.html", user=session['user'])
        return render_template("profile.html", user=user)
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
            return redirect(url_for("myprofile"))
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
        if request.form.has_key("tablogin"):
            return redirect(url_for("login"))
        if request.form.has_key("tabhome"):
            return redirect(url_for("home"))
        if request.form.has_key("tabsignup"):
            return redirect(url_for("signup"))
        if request.form.has_key("tabcreate"):
            return redirect(url_for("create"))
        if request.form.has_key("tabprofile"):
            return redirect(url_for("myprofile"))
        if request.form.has_key("tabsurvey"):
            return redirect(url_for("survey"))
        if request.form.has_key("tabresults"):
            return redirect(url_for("results"))
        if request.form.has_key("submitSurvey"):
            sname = request.form['sname']
            username = session['user']
            ans = []
            #change to correct question number
            for i in range (0, 5):
                ans.append(request.form[str(i)])
            print sname, username, ans    
            util.takeSurvey(sname, username, ans)
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
            return redirect(url_for("myprofile"))
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
    util.createSurvey('roommate', [['How much of a night owl are you?', 'number'],['On a scale of 1 to 5, how quiet do you want your room to be?', 'number'],['How much to you agree with the following statement: I will spend most of my free time in my room.', 'word'],['How much to you agree with the following statement: "I  always have friends over.', 'word'],['How much do you agree with the following statement: I need my room to be clean and organized.', 'word']])
    app.run(debug=True, port=6565)
