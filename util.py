import urllib
import json
import sys
import time
import base64
import random
import math
from pymongo import Connection
from gridfs import GridFS

connection = Connection('mongo2.stuycs.org')
db = connection.admin
res = db.authenticate('ml7','ml7')
db = connection['z-pd6']
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
    surv = surveys.find_one({'name': surveyname})
    allAnswers = dict(surv)
    allAnswers['useranswers'].update({user:ans})
    surveys.update(
        {'name':surveyname},
        allAnswers)
    print allAnswers
    return True

def createUser(user,password,age,realname,gender,hobbies):
    if users.find_one({"user" : user}) != None:
        return False
    tmp = base64.b64encode(password)
    newuser = {"user" : user, "pass" : tmp, "age": age, "realname":realname, "gender":gender, "hobbies": hobbies}
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

def createSurvey(name, questions):
    if surveys.find_one({"name":name}) != None:
        return False
    surveys.insert({"type": "survey", "name" : name, "questions" : questions, "useranswers": {}, "userdifferences": {}, "userpercentages": {}})
    return True

def deleteSurvey(name):
    surveys.remove({"name": name})
    return True

def findDiffs(surveyName, user):
    thisSurvey = dict(surveys.find_one({'name': surveyName}))
    allUsers = thisSurvey['useranswers']
    thisUser = allUsers[user]
    thisSurvey['userdifferences'][user] = {}

    for x in allUsers:
        if x != user:
            diffs = [math.fabs(allUsers[x][i] - thisUser[i]) for i in range(0, len(thisUser))]
            thisSurvey['userdifferences'][user].update({x:sum(diffs)})
            surveys.update(
                {'name':surveyName},
                thisSurvey)
    return True    

def findPercents(surveyName, user):
    thisSurvey = dict(surveys.find_one({'name': surveyName}))
    sumDiffs = thisSurvey['userdifferences'][user]
    thisSurvey['userpercentages'][user] = {}    

    numQs = len(thisSurvey['useranswers'][user])
    maxDiff = 4.0 * numQs
    
    for x in sumDiffs:
        percent = 100 - (sumDiffs[x] / maxDiff) * 100
        thisSurvey['userpercentages'][user].update({x:percent})
        surveys.update(
            {'name':surveyName},
            thisSurvey)
    return True

def match(surveyName, user):
    matchesData = {}
    thisSurvey = dict(surveys.find_one({'name': surveyName}))
    percents = thisSurvey['userpercentages'][user]
    
    numQs = len(thisSurvey['useranswers'][user])
    maxDiff = 4.0 * numQs
    matchesData['maxPercent'] = max(percents[x] for x in percents)
    matchesData['minPercent'] = min(percents[x] for x in percents)
    
    matchesData['best'] = [x for x in percents if percents[x] == matchesData['maxPercent']]
    matchesData['worst'] = [x for x in percents if percents[x] == matchesData['minPercent']]
    matchesData['overallBest'] = []
    
    return matchesData

def sortPercentages(surveyname):
    sorted = {}
    thisSurvey = dict(surveys.find_one({'name':surveyname}))
    unsorted = thisSurvey['userpercentages']
    
    for x in unsorted:
        sorted[x] = [[unsorted[x][y], y] for y in unsorted[x]]
    for x in sorted:
        sorted[x].sort(reverse=True)
    for x in sorted:
        sorted[x] = [y[1] for y in sorted[x]]
    return sorted
                                                

def getSurveyQs(surveyName):
    survey = dict(surveys.find_one({'name':surveyName}))
    qs = survey['questions']
    return qs

#not tested
def getSurveyNames():
    names = []
    for surv in surveys.find({"type": "survey"}):
        names.append(surv["name"])
    return names


#not tested
def getUser(userName):
    userInfo = dict(users.find_one({'user':userName}))
    result = [userInfo[x] for x in userInfo]
    return result[1:]
    
#not tested
def editUserInfo(userName, fieldChange, newValue):
    pass



#add in a list of lists (ordered) of best to worst matches. is input for bestOverall. dictionarry of lists of lists
#not done
def bestOverall(dictionaryMatches):
    #if odd numbered leave someone out
    usersMatches = {}
    matched = False 
    for person in dictionaryMatches:
        usersMatches[person] = ""
        finalMatches = []
    return matchMethod(usersMatches, dictionaryMatches, finalMatches)


#def matchMethod(userMatches, dictionaryMatches, finalMatches):
#    if dictionaryMatches.keys().length == 0:
#        return finalMatches
#    else:
#        for person in dictionaryMatches:
#            if (usersMatches[person]=="" and usersMatches[dictionaryMatches[pe#rson][0]==""):
#                usersMatches[person]== dictionaryMatches[person][0]
#                usersMatches[dictionaryMatches[person][0]] = person
#            elif (usersMatches[person] == ""):
#                notMatched = False
#                while (notMatched):
                #here need to check if the person i wanna assign is available to be assigned
#                    if usersMatches[dictionaryMatches[person]]:
                          
            
 #                   switchStuff(dictionaryMatches[person][0], dictionaryMatches)
    
#add to finalMatches
#eliminate from dictionaryMatches
#if dictionaryMatches is empty, return finalMatches
#else recurse by calling matchMethod
#base case of recursion, return finalMatches

#def switchStuff(person, dictionaryMatches):


#if __name__ == "__main__":
#    createUser("Dina", "hello")
#    print checkUserPass("Dina", "hello")
#    print checkUserPass("Dina", "he")
#    createSurvey("test", [])
#    createSurvey("test2", [])
#    print getSurveyNames()
#    takeSurvey("test", "Helen", [1, 1, 1, 1, 1])
#    takeSurvey("test", "Dina", [1, 1, 1, 1, 1])
#    takeSurvey("test", "Shreya",  [1, 1, 1, 1, 1])
#    takeSurvey("test", "David",  [2, 2, 2, 2, 2])

#    #testing algorithm
#    findDiffs('test', 'Helen')
#    findPercents('test', 'Helen')
#    match('test', 'Helen')
#    deleteSurvey("prom date")
