import math
import util

def findMatches(users, user):
    matches = {}
    vectors = vectorize(users)
    diff = sortByDiff(vectors, user)

    matches['best'] = percent(bestMatch(diff))
    matches['worst'] = percent(worstMatch(diff))
    matches['overall'] = percent(overallBestMatch(diff))
    print matches
    return matches

def bestMatch(diff):
    best = [tup for tup in diff if tup[0] == diff[0][0]]
    return best

def worstMatch(diff):
    diff.sort(reverse=True)
    worst = [tup for tup in diff if tup[0] == diff[0][0]]
    return worst

def overallBestMatch(diff):
    return []

def vectorize(users):
    vectors = {}
    tupleVec = [(sum([x * x for x in users[user]]), user) for user in users]
    for (a, b) in tupleVec:
        vectors[b] = a
    return vectors

def sortByDiff(vectors, user):
    goal = vectors[user]
    diff = [(math.fabs(vectors[vec] - goal), vec) for vec in vectors if vec != user]
    diff.sort()
    return diff

def percent(matches):
    largest = float(5 * 5 * 5 - 5 * 1 * 1)
    percents = [((100 - match[0] / largest * 100), match[1]) for match in matches]
    return percents

#testing
users = {'shreya': [1, 1, 2, 2, 2], 'Dina': [4, 4, 4, 4, 4], 'helen': [2, 2, 2, 2, 2], 'david': [5, 5, 5, 5, 5]}

findMatches(users, 'helen')
