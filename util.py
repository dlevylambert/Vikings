import urllib
import json
import sys
import time
import base64
import random
import math
from pymongo import Connection
from gridfs import GridFS

Conn = Connection('ds041367.mongolab.com',41367)
db = Conn['stuycs_sideprojects']
res = db.authenticate('stuycs','stuycs')
users = db.VikingsUsers
surveys = db.VikingsSurveys
#pics = db.VikingsPics
#fs = GridFS(db, 'pics')

"""
Function: takeSurvey(string user, string survey, int[] ans)
Purpose: save the user's answers for the survey
Return: Boolean

Last Edited: 4/21/13 at 16:06 by Helen Nie
Tested: yes
"""
def takeSurvey(surveyname, user, ans):
    surv = surveys.find_one({"name": surveyname})
    surv["useranswers"][user] = ans
    return true

def createUser(user,password):
    if users.find_one({"user" : user}) != None:
        return False
    tmp = base64.b64encode(password)
    newuser = {"user" : user, "pass" : tmp}
    users.insert(newuser)
    return True

def checkUserPass(user,password):
    encpass = base64.b64encode(password)
    tmp = users.find_one({"user" : user})
    if tmp == None:
        return 0
    if encpass == tmp["pass"]:
        return True
    else:
        return False

def createSurvey(password,name):
    if surveys.find_one({"name":name}) != None:
        return False
    newsurvey = {"name" : name, "questions" : [], "useranswers": {}, "userdifferences": {}, "userpercentage": {}} 
    surveys.insert(newsurvey)
    return True

def findDiffs(surveyname, user):
    surv = surveys.find_one({"name": surveyname})
    difference = 0
    useranswers =[]
    for answer in surv["useranswers"][user]:
        useranswers.append(answer)
    for person in surv["useranswers"]:
        if person == user:
            pass
        else:
            for answer in person:
                difference += math.fabs(answer - useranswers.pop(0))
            #store in survey database

#if __name__ == "__main__":
#    createUser("Dina", "hello")
#    print checkUserPass("Dina", "hello")
#    print checkUserPass("Dina", "he")
#    createSurvey("hello", "test")
#    takeSurvey("Dina", "test", [1, 1, 1, 1, 1])
