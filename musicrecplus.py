# A very simple music recommender system.
'''
Created on 11/8
@author:   GaYoung Park, Roger Shagawat, 10446882, 10441828
Pledge:    I pledge my honor that I have abided by the stevens honor system
CS115 - Hw 10
'''
PREF_FILE = "musicrec-store.txt"

def loadUsers(fileName):
    ''' Reads in a file of stored users' preferences
        stored in the file 'fileName'.
        Returns a dictionary containing a mapping
        of user names to a list preferred artists
    '''
    file = open('musicrecplus.txt', 'r')
    userDict = {}
    for line in file:
        # Read and parse a single line
        [userName, bands] = line.strip().split(":")
        bandList = bands.split(",")
        bandList.sort()
        userDict[userName] = bandList
    file.close()
    return userDict

def getPreferences(userName, userMap):
    ''' Returns a list of the uesr's preferred artists.
        If the s
        ystem already knows about the user,
        it gets the preferences out of the userMap
        dictionary and then asks the user if she has
        additional preferences.  If the user is new,
        it simply asks the user for her preferences. '''
    newPref = ""
    if userName in userMap:
        prefs = userMap[userName]
        print("I see that you have used the system before.")
        print("Your music preferences include:")
        for artist in prefs:
            print(artist)
        print("Enter an artist that you like")
        newPref = input("(Enter to finish): ")
    else:
        prefs = []
        print("I see that you are a new user.")
        print("Enter an artist that you like")
        newPref = input("(Enter to finish): " )
        
    while newPref != "":
        prefs.append(newPref.strip().title())
        print("Enter an artist that you like ")
        newPref = input("(Enter to finish): ")
        
    # Always keep the lists in sorted order for ease of
    # comparison
    prefs.sort()
    saveUserPreferences(userName, prefs, userMap, 'musicrecplus.txt')
    return prefs

def getRecommendations(currUser, prefs, userMap):
    ''' Gets recommendations for a user (currUser) based
        on the users in userMap (a dictionary)
        and the user's preferences in pref (a list).
        Returns a list of recommended artists.  '''
    bestUser = findBestUser(currUser, prefs, userMap)
    recommendations = drop(prefs, userMap[bestUser])
    return recommendations

def findBestUser(currUser, prefs, userMap):
    ''' Find the user whose tastes are closest to the current
        user.  Return the best user's name (a string) '''
    users = userMap.keys()
    bestUser = None
    bestScore = -1
    for user in users:
        score = numMatches(prefs, userMap[user])
        if score > bestScore and currUser != user:
            bestScore = score
            bestUser = user
    return bestUser

def drop(list1, list2):
    ''' Return a new list that contains only the elements in
        list2 that were NOT in list1. '''
    list3 = []
    i = 0
    j = 0
    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            i += 1
            j += 1
        elif list1[i] < list2[j]:
            i += 1
        else:
            list3.append(list2[j])
            j += 1
    return list3

def numMatches( list1, list2 ):
    ''' return the number of elements that match between
        two sorted lists '''
    matches = 0
    i = 0
    j = 0
    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            matches += 1
            i += 1
            j += 1
        elif list1[i] < list2[j]:
            i += 1
        else:
            j += 1
    return matches

def saveUserPreferences(userName, prefs, userMap, fileName):
    ''' Writes all of the user preferences to the file.
        Returns nothing. '''
    userMap[userName] = prefs
    file = open(fileName, "w")
    for user in userMap:
        toSave = str(user) + ":" + ",".join(userMap[user]) + \
                    "\n"
        file.write(toSave)
    file.close()
    
def getNonPrivUsers():
    L = []
    dic = loadUsers('musicrecplus.txt')
    users = list(dic)
    artists = list(dic.values())
    for i in range(len(users)):
        if "$" in users[i]:
            users.remove(users[i])
        else:
            users = users
    return users

def getNonPrivArtists():
    L = []
    dic = loadUsers('musicrecplus.txt')
    users = list(dic)
    artists = list(dic.values())
    for i in range(len(users)):
        if "$" in users[i]:
            users.remove(users[i])
            artists.remove(artists[i])
        else:
            users = users
            artists = artists
    for x in range(len(artists)):
            L += artists[x]
    artists = L
    return artists


dic = {}
def mostPopularArtists():
    '''print the artist that is liked by the most users;
    if tie, print all artists'''
    artists = getNonPrivArtists()
    if artists == []:
        return "Sorry, no artists found."
    else:
        for x in range(len(artists)):
            dic[artists[x]] = artists.count(artists[x])
    keys = list(dic)
    values = list(dic.values())
    i = values.index(max(values))
    return keys[i]
      
def mostLikes():
    '''print which user has the most likes, print full names
    of the users who likes the most artists'''
    dic = loadUsers('musicrecplus.txt')
    dic = dic.keys()
    if dic == []:
        print ("Sorry, no user found.")

def howMostPopular():
    '''print the number of likes the most popular artists
    received'''
    artists = getNonPrivArtists()
    if artists == []:
        return "Sorry, no artists found."
    else:
        for x in range(len(artists)):
            dic[artists[x]] = artists.count(artists[x])
    keys = list(dic)
    values = list(dic.values())
    return max(values)


def menu(userName, userMap):
    option = input("Enter a letter to choose an option:\
    \ne - Enter preferences\
    \nr - Get recommendations\
    \np - Show most popular artists\
    \nh - How popular is the most popular\
    \nm - Which user has the most likes\
    \nq - Save and quit\n")
    swicher = {
        'e' : getPreferences(userName, userMap),\
        'r' : getRecommendations(currUser, prefs, userMap),\
        'p' : mostPopularArtists(),\
        'h' : howMostPopular(),\
        'm' : mostLikes(),\
        'q' : saveUserPreferences(),\
    }
    return switcher[option]

