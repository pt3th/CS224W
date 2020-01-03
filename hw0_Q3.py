#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 14:32:01 2020

@author: qiuwenjie
"""

'''
cs224w homework 0
Q3
'''

import snap as sp
import numpy as np
#load graph
G = sp.LoadEdgeList(sp.PNGraph, "stackoverflow-Java.txt",0,1)
Components = sp.TCnComV()
sp.GetWccs(G,Components)
WccsNum = len(Components)
print("Q3.1 The number of weakly connected components in the network: ",WccsNum)

MxWcc = sp.GetMxWcc(G)
MxWccNodeNum = MxWcc.GetNodes()
MxWccEdgesNum = MxWcc.GetEdges()
print("Q3.2 %d edges and %d nodes in the largest weakly connected component."\
      %(MxWccEdgesNum,MxWccNodeNum))

PRankH = sp.TIntFltH()
sp.GetPageRank(G, PRankH)
PRankHKey = []
PRankHVal = []
for item in PRankH:
    PRankHKey.append(item)
    PRankHVal.append(PRankH[item])
PRankHVal = np.array(PRankHVal)
SortedIdx = np.argsort(-PRankHVal)
Top3PRId = []
for i in range(3):
    Top3PRId.append(PRankHKey[SortedIdx[i]])
print("Q3.3 IDs of the top 3 most central nodes in the network by PagePank scores: ",Top3PRId)

NIdHubH = sp.TIntFltH()
NIdAuthH = sp.TIntFltH()
sp.GetHits(G, NIdHubH, NIdAuthH)
NIdHubHKey = []
NIdHubHVal = []
for item in NIdHubH:
    NIdHubHKey.append(item)
    NIdHubHVal.append(NIdHubH[item])
NIdHubHVal = np.array(NIdHubHVal)
SortedIdx1 = np.argsort(-NIdHubHVal)
#Auth
NIdAuthHKey = []
NIdAuthHVal = []
for item in NIdAuthH:
    NIdAuthHKey.append(item)
    NIdAuthHVal.append(NIdAuthH[item])
NIdAuthHVal = np.array(NIdAuthHVal)
SortedIdx2 = np.argsort(-NIdAuthHVal)
Top3HubId = []
Top3AuthId = []
for i in range(3):
    Top3HubId.append(NIdHubHKey[SortedIdx1[i]])
    Top3AuthId.append(NIdAuthHKey[SortedIdx2[i]])

print("Q3.4.1 IDs of the top 3 hubs in the network by HITS scores. ",Top3HubId)
print("Q3.4.2 IDs of the top 3 authorities in the network by HITS scores. ",Top3AuthId)

