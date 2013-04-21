import math
import util


"""
Function: findMatches(dict users, string user)
Purpose: to find the best, worst, and overall best match for the user
Return: a dictionary with keys 'best, 'worst', and 'overall'. Each key points to a list of tuples of the form (name, match percentage)

Last Edited: 4/21/13 at 15:27 by Helen Nie
Tested:yes
"""
def findMatches(users, user):
    matches = {}
    vectors = vectorize(users)
    diff = sortByDiff(vectors, user)

    matches['best'] = percent(bestMatch(diff))
    matches['worst'] = percent(worstMatch(diff))
    matches['overall'] = percent(overallBestMatch(diff))
    print matches
    return matches


"""
Function: bestMatch(tuple[] diff)
Purpose: to find the best match
Return: a list of tuples of the form (name, vector difference)

Last Edited: 4/21/13 at 15:27 by Helen Nie
Tested:yes
"""
def bestMatch(diff):
    best = [tup for tup in diff if tup[0] == diff[0][0]]
    return best


"""
Function: worstMatch(tuple[] diff)
Purpose: to find the worst match
Return: a list of tuples of the form (name, vector difference)

Last Edited: 4/21/13 at 15:27 by Helen Nie
Tested:yes
"""
def worstMatch(diff):
    diff.sort(reverse=True)
    worst = [tup for tup in diff if tup[0] == diff[0][0]]
    return worst


"""
Function: bestMatch(tuple[] diff)
Purpose: find the overall best match
Return: a list of tuples of the form (name, vector difference)

Last Edited: 4/21/13 at 15:27 by Helen Nie
Tested:yes
"""
def overallBestMatch(diff):
    return []


"""
Function: vectorize(dict users)
Purpose: use answer values in users to assign a vector to each user
Return: a dictionary of the form {name: vector}

Last Edited: 4/21/13 at 15:27 by Helen Nie
Tested:yes
"""
def vectorize(users):
    vectors = {}
    tupleVec = [(sum([x * x for x in users[user]]), user) for user in users]
    for (a, b) in tupleVec:
        vectors[b] = a
    return vectors


"""
Function: sortByDiff(dict vectors, string user)
Purpose: to find the difference between each user's vector value and that of the current user
Return: a list of tuples of the form (difference, name)

Last Edited: 4/21/13 at 15:27 by Helen Nie
Tested:yes
"""
def sortByDiff(vectors, user):
    goal = vectors[user]
    diff = [(math.fabs(vectors[vec] - goal), vec) for vec in vectors if vec != user]
    diff.sort()
    return diff


"""
Function: percent(tuple[] matches)
Purpose: to convert difference values to percentages by comparing them to the largest possible difference, 120.0
Return: a list of tuples of the form (percentage, name)

Last Edited: 4/21/13 at 15:27 by Helen Nie
Tested:yes
"""
def percent(matches):
    largest = 120.0
    percents = [((100 - match[0] / largest * 100), match[1]) for match in matches]
    return percents


#testing
users = {'shreya': [1, 1, 2, 2, 2], 'Dina': [4, 4, 4, 4, 4], 'helen': [2, 2, 2, 2, 2], 'david': [5, 5, 5, 5, 5]}

findMatches(users, 'helen')
