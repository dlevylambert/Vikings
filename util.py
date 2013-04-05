import urllib
import json
import sys
import time
import base64
import random
import gamesystem
import math
from pymongo import Connection

Conn = Connection('ds041367.mongolab.com',41367)
db = Conn['stuycs_sideprojects']
res = db.authenticate('stuycs','stuycs')
users = db.VikingsUsers
surveys = db.VikingsSurveys

def createUser(user,password):
    if users.find_one({"user" : user}) != None:
        return False
    tmp = base64.b64encode(password)
    newuser = {"user" : user, "pass" : tmp, "game" : 0, "wins" : 0, "loses" : 0,"friends" : []}
    users.insert(newuser)
    return True

def createSurvey(password,name):
    if surveys.find_one({"name":name}) != None:
        return False
    newsurvey = {"name" : name, "questions" : []}
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

