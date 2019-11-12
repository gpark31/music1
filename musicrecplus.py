# A very simple music recommender system.
'''
Created on 11/8
@author:   GaYoung Park, Roger Shagawat, 10446882, 10441828
Pledge:    I pledge my honor that I have abided by the stevens honor system

CS115 - Hw 10
'''
PREF_FILE = "musicrec-store.txt"

def loadUsers(filename):
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

        If the system already knows about the user,
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

def menu():
    option = input("Enter a letter to choose an option:\
    \ne - Enter preferences\
    \nr - Get recommendations\
    \np - Show most popular artists\
    \nh - How popular is the most popular\
    \nm - Which user has the most likes\
    \nq - Save and quit")
    swicher = {
        'e': enter_preferences()
        'r': get_recommendations()
        'p': most_popular_artists()
        'h': how_most_popular()
        'm': most_likes()
        'q': save_and_quit()
    }
    return switcher(option)

def main():
    ''' The main recommendation function '''
    userMap = loadUsers(PREF_FILE)
    print("Welcome to the music recommender system!")

    userName = input("Enter your name (put a $ symbol after your name if you wish your preferences to remain private)")
    print ("Welcome,", userName)

    prefs = getPreferences(userName, userMap)
    recs = getRecommendations(userName, prefs, userMap)

    # Print the user's recommendations
    if len(recs) == 0:
        print("I'm sorry but I have no recommendations")
        print("for you right now.")
    else:
        print(userName, "based on the users I currently")
        print("know about, I believe you might like:")
        for artist in recs:
            print(artist)

        print("I hope you enjoy them! I will save your")
        print("preferred artists and have new")
        print(" recommendations for you in the future")

    saveUserPreferences(userName, prefs, userMap, PREF_FILE)
    

if __name__ == "__main__": main()
