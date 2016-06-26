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
    upvotes.append(int(post.get("value")))

obdv = objects.find({"_key": {"$regex": r'uid:[0-9]+:downvote'}})
downvotes = []
for post in obdv:
    downvotes.append(int(post.get("value")))

obfav = objects.find({"_key": {"$regex": r'uid:[0-9]+:favourite'}})
favourites = []
for post in obfav:
    favourites.append(int(post.get("value")))

print "Getting NodeBB era posts"
obf = objects.find({"$and": [  {"relativeTime": {"$exists": False}}, {"pid": {"$exists": True}}, {"content": {"$exists": True}} ]   })

#Getting number of times cited, faved, etc...:
#mentions = [0]*len(userlist)
#nposts = [0]*len(userlist)
postn = 0
postlimit = 10 #no limit = 0

UserRanking = Counter()
UserPosts = Counter()
UserFavs = Counter()
UserUpVotes = Counter()
UserDownVotes = Counter()
UserMentions = Counter()
            
print "Number of posts: " + str(obf.count())
for post in obf:
    if post.get("tid") in floodlist:
        continue
    content = post.get("content")
    author = post.get("uid")
    pid = post.get("pid")
    usern = 0
    for user, uid in userlist:
        try:
            if uid == author:
                #nposts[usern] += 1
                UserPosts[user] += 1
                nuv = upvotes.count(pid)
                ndv = -downvotes.count(pid)
                nfavs = favourites.count(pid)
                UserRanking[user] += nuv + ndv + nfavs
                UserFavs[user] += nfavs
                UserUpVotes[user] += nuv
                UserDownVotes[user] += ndv
            elif user in content:
                #mentions[usern] += 1
                UserRanking[user] += 1
                UserMentions[user] += +1
            
        except TypeError:
            print "TypeError"
            print "uid:"
            print uid
            print "username:"
            print user
            print "content:"
            print content
        usern += 1
    postn += 1

    if postlimit > 0 and postn > postlimit:
        break

for i in range(0, len(userlist)):
    userlist[i].append(UserRanking[userlist[i][0]])
    userlist[i].append(UserPosts[userlist[i][0]])
    userlist[i].append(UserFavs[userlist[i][0]])
    userlist[i].append(UserUpVotes[userlist[i][0]])
    userlist[i].append(UserDownVotes[userlist[i][0]])
    userlist[i].append(UserMentions[userlist[i][0]])
    
userlist1 = sorted(userlist, key=lambda userlist: userlist[2], reverse=True) #sort by mentions+favs+upvotes-downvotes
userlist2 = sorted(userlist, key=lambda userlist: userlist[3], reverse=True) #sort by posts
userlist3 = sorted(userlist, key=lambda userlist: userlist[4], reverse=True) #sort by favs
userlist4 = sorted(userlist, key=lambda userlist: userlist[5], reverse=True) #sort by upvotes
userlist5 = sorted(userlist, key=lambda userlist: userlist[6], reverse=True) #sort by downvotes
userlist6 = sorted(userlist, key=lambda userlist: userlist[7], reverse=True) #sort by mentions

with open("UserRanking.pickle", "w") as sf:
    pickle.dump([userlist1, userlist2, userlist3, userlist4, userlist5, userlist6], sf)

print "End"

timeend = time.time()
print "Time elapsed:"
print timeend - timestart
