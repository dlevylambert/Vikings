import urllib
import json
import sys
import time
import base64
import random
import math
from pymongo import Connection

Conn = Connection('ds041367.mongolab.com',41367)
db = Conn['stuycs_sideprojects']
res = db.authenticate('stuycs','stuycs')
users = db.VikingsUsers
surveys = db.VikingsSurveys


"""
Function: takeSurvey(string user, string survey, int[] ans)
Purpose: save the user's answers for the survey
Return: Boolean

Last Edited: 4/21/13 at 16:06 by Helen Nie
Tested: yes
"""
def takeSurvey(user, survey, ans):
    users = surveys.find_one({"name" : survey})["users"]
    users[user] = ans
    return True


def createUser(user,password):
    if users.find_one({"user" : user}) != None:
        return False
    tmp = base64.b64encode(password)
    newuser = {"user" : user, "pass" : tmp}
    users.insert(newuser)
    return True

def createSurvey(password,name):
    if surveys.find_one({"name":name}) != None:
        return False
    newsurvey = {"name" : name, "questions" : [], "users": {}}
    surveys.insert(newsurvey)
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


#if __name__ == "__main__":
#    createUser("Dina", "hello")
#    print checkUserPass("Dina", "hello")
#    print checkUserPass("Dina", "he")
#    createSurvey("hello", "test")
#    takeSurvey("Dina", "test", [1, 1, 1, 1, 1])
