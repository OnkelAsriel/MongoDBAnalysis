from ClientSetUp import *

userlist = []
for ob in objects.find({"$and" : [{"username" : {"$exists" : 1}}]}):#({"$and" : [{"_key" : {"$regex" : "user:[0-9]+"}}, {"username" : {"$exists" : 1}}]}):
    username = ob.get("username")
    username = username.replace(u' ', u'-')
    username = u'@' + username
    uid = ob.get("uid")
    userlist.append(uid)
    
print "User list created."
print str(len(userlist)) + " users found."

#Find posts not older than...
obf = objects.find({"$and" : [{"_key" : {"$regex" : "post:[0-9]+"}}, {"timestamp" : {"$gt" : 1477958400000}}] }) #1 Nov 2016:1477958400000  #1 Nov 2015: 1446336000000 #ms

f = open("PostNullUser.txt", "w")

#If a post has an author not in the user list, save the pid
for post in obf:
    author = post.get("uid")
    if author not in userlist:
        f.write(str(post.get("pid"))+"\n")
f.close()
