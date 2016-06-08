from ClientSetUp import *
#from ROOT import TCanvas, TH1F, TTree, TFile, std
from unidecode import unidecode
import string
import time

timestart = time.time()
print "Starting"

from Emojilist import *
emojilist = emojilist_short

print "Making [FLOOD] exclude list" #exclude official FLOOD topics
floodlist = []
for ob in objects.find({"title":{"$regex":r'\[FLOOD]'}}):
    floodlist.append(ob.get("tid"))

print "Getting NodeBB era posts"
obf = objects.find({"$and": [  {"relativeTime": {"$exists": False}}, {"pid": {"$exists": True}}, {"content": {"$exists": True}} ]   })

#Store number of times emoji is found in a message:
messagecount = [0]*len(emojilist)

postn = 0
postlimit = 0 #no limit
print "Number of posts: " + str(obf.count())
for post in obf:
    tid = post.get("tid")
    if tid in floodlist:
        continue
    content = post.get("content")
    emojin = 0 #I could have done a dic, I chose to do this instead
    for emoji in emojilist:
        if emoji[0] in content:
            messagecount[emojin] += 1
        emojin += 1
    postn += 1
    if postlimit > 0 and postn > postlimit:
        break

for i in range(0, len(emojilist)):
    emojilist[i].append(messagecount[i])

emojilist = sorted(emojilist, key=lambda emojilist: emojilist[1], reverse=True)

print "End"

timeend = time.time()
print "Time elapsed:"
print timeend - timestart
