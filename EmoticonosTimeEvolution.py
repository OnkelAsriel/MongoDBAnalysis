from ClientSetUp import *
#Using ROOT to make histograms for now
from ROOT import TCanvas, TH1F, TTree, TFile, std, TLegend, gStyle, THStack
from unidecode import unidecode
import string
import time
import pickle

timestart = time.time()
print "Starting"

with open("emojilist.pickle") as sf:
    emojilist = pickle.load(sf)

print "Making [FLOOD] exclude list" #exclude official FLOOD topics
floodlist = []
for ob in objects.find({"title":{"$regex":r'\[FLOOD]'}}):
    floodlist.append(ob.get("tid"))

#Start of NodeBB time: 1430147642074.0 ms, Mon, 27 Apr 2015 17:06:35 GMT
t0 = 1430147642074.0
tf = 1447280914107.0 #Store here the highest post timestamp found

histos = [] #store emoji use time
#to be substituted by a more python-friendly histogram class
hAllPosts = TH1F("hAllPosts", "AllPosts", 7, 0, tf - t0)
binlabels = ["Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre"]
for emoji, ntimes in emojilist:
    if 2*ntimes >= emojilist[0][1]:
        histos.append(TH1F("h"+emoji, emoji, 7, 0, tf - t0))
    
print "Getting NodeBB era posts"
obf = objects.find({"$and": [  {"relativeTime": {"$exists": False}}, {"pid": {"$exists": True}}, {"content": {"$exists": True}} ]   })

postn = 0
postlimit = 0 #no limit
print "Number of posts: " + str(obf.count())
for post in obf:
    if post.get("tid") in floodlist:
        continue
    content = post.get("content")
    timestamp = post.get("timestamp")
    if timestamp > tf:
        tf = timestamp
    timestamp -= t0
    for i in range(0, len(histos)):
        hAllPosts.Fill(timestamp)
        if emojilist[i][0] in content:
            histos[i].Fill(timestamp)
    postn += 1
    if postlimit > 0 and postn > postlimit:
        break

cAll = TCanvas("cAllPosts", "All Posts", 600, 600)
hAllPosts.Draw("histo")

cEmojis = TCanvas("cEmojis", "Emojis Relative", 600, 600)

colour = 1

leg = TLegend(0.6, 0.7, 0.9, 0.9)
leg.SetHeader("Emoticonos: uso relativo")
gStyle.SetFillStyle(0)
gStyle.SetLineWidth(0)
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

hs = THStack("hs", "")

for h in histos:
    h.Divide(hAllPosts)
    h.SetLineColor(1)
    h.SetFillColor(colour)
    h.SetLineWidth(1)
    for binn in range(1, 8):
        h.GetXaxis().SetBinLabel(binn, binlabels[binn-1])
    leg.AddEntry(h, h.GetTitle(), "f")
    hs.Add(h)
    colour += 1

hs.Draw()
leg.Draw()
