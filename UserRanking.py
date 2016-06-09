from ClientSetUp import *
from unidecode import unidecode
import time
import pickle
from collections import Counter

timestart = time.time()
print "Starting"

print "Making [FLOOD] exclude list" #exclude official FLOOD topics
floodlist = []
for ob in objects.find({"title":{"$regex":r'\[FLOOD]'}}):
    floodlist.append(ob.get("tid"))

print "Getting the list of users"
userlist = []
for ob in objects.find({"$and" : [{"username" : {"$exists" : 1}}]}):
    if ob.get("postcount") < 100:
        continue
    username = ob.get("username")
    username = username.replace(u' ', u'-')
    username = u'@' + username
    uid = ob.get("uid")
    userlist.append([username, uid])
print str(len(userlist)) + " users found."

print "Listing posts with upvotes, downvotes and favourites:"
obuv = objects.find({"_key": {"$regex": r'uid:[0-9]+:upvote'}})
upvotes = []
for post in obuv:
    upvotes.append(post.get("value"))

obdv = objects.find({"_key": {"$regex": r'uid:[0-9]+:downvote'}})
downvotes = []
for post in obdv:
    downvotes.append(post.get("value"))

obfav = objects.find({"_key": {"$regex": r'uid:[0-9]+:favourite'}})
favourites = []
for post in obfav:
    favourites.append(post.get("value"))

print "Getting NodeBB era posts"
obf = objects.find({"$and": [  {"relativeTime": {"$exists": False}}, {"pid": {"$exists": True}}, {"content": {"$exists": True}} ]   })

#Getting number of times cited, faved, etc...:
#mentions = [0]*len(userlist)
#nposts = [0]*len(userlist)
postn = 0
postlimit = 0 #no limit = 0

UserRanking = Counter()
UserPosts = Counter()
print "Number of posts: " + str(obf.count())
for post in obf:
    if post.get("tid") in floodlist:
        continue
    content = post.get("content")
    author = post.get("uid")
    pid = post.get("pid")
    usern = 0
    for user, uid in userlist:
        if uid == author:
            #nposts[usern] += 1
            UserPosts[user] += 1
            nuv = upvotes.count(pid)
            ndv = -downvotes.count(pid)
            nfavs = favourites.count(pid)
            UserRanking[user] += nuv + ndv + nfavs
        elif user in content:
            #mentions[usern] += 1
            UserRanking[user] += 1
            
        usern += 1
    postn += 1
    if postlimit > 0 and postn > postlimit:
        break

for i in range(0, len(userlist)):
    userlist[i].append(UserRanking[userlist[i][0]])
    userlist[i].append(UserPosts[userlist[i][0]])
    userlist[i].append(UserRanking[userlist[i][0]]-UserPosts[userlist[i][0]])
    if UserPosts[userlist[i][0]] > 0:
        userlist[i].append(float(UserRanking[userlist[i][0]])/float(UserPosts[userlist[i][0]]))
    else:
        userlist[i].append(0)

userlist1 = sorted(userlist, key=lambda userlist: userlist[2], reverse=True) #sort by nentions+favs+upvotes-downvotes
userlist2 = sorted(userlist, key=lambda userlist: userlist[3], reverse=True) #sort by posts
userlist3 = sorted(userlist, key=lambda userlist: userlist[4], reverse=True) #sort by #1-#2
userlist4 = sorted(userlist, key=lambda userlist: userlist[5], reverse=True) #sort by #1/#2

with open("UserRanking.pickle", "w") as sf:
    pickle.dump([userlist1, userlist2, userlist3, userlist4], sf)

print "End"

timeend = time.time()
print "Time elapsed:"
print timeend - timestart
