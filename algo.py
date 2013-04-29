#add in a list of lists (ordered) of best to worst matches. is input for bestOverall. dictionarry of lists of lists

def bestOverall(dictionaryMatches):
    #if odd numbered leave someone out
    usersMatches = {}
    matched = False 
    for each person in dictionaryMatches:
        usersMatches[person] = ""
    finalMatches = []
    return matchMethod(userMatches, dictionaryMatches, finalMatches)

def matchMethod(userMatches, dictionaryMatches, finalMatches):
    #add to finalMatches
    #eliminate from dictionaryMatches
    #if dictionaryMatches is empty, return finalMatches
    #else recurse by calling matchMethod
    #base case of recursion, return finalMatches
