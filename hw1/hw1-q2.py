#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 13:49:36 2020

@author: q
"""

import snap
import numpy as np
import matplotlib.pyplot as plt
#load graph
FIn = snap.TFIn("hw1-q2.graph")
G = snap.TUNGraph.Load(FIn)

#Q2.1
def GetNodeFea(G,NodeID):
    Node = G.GetNI(NodeID)
    NodeFea = []
    Deg = Node.GetDeg()
    if Deg == 0:
        return np.zeros(3)
    NodeFea.append(Deg)
    EgonetID = [NodeID]
    EdgeNum = 0
    for i in range(Deg):
        EgonetID.append(Node.GetNbrNId(i))

    for id1 in EgonetID:
        for id2 in EgonetID:
            if (id1!=id2) & G.IsEdge(id1,id2):
                EdgeNum += 0.5
    NodeFea.append(EdgeNum)
    EnterLeaveNum = 0
    for ID in EgonetID[1:]:
        node = G.GetNI(ID)
        deg = node.GetDeg()
        for i in range(deg):
            nbr_id = node.GetNbrNId(i)
            if nbr_id not in EgonetID:
                EnterLeaveNum +=1
    NodeFea.append(EnterLeaveNum)
    NodeFea = np.array(NodeFea)
    return NodeFea

def CalSimilarity(Fea1,Fea2):
    Norm1 = np.linalg.norm(Fea1)
    Norm2 = np.linalg.norm(Fea2)
    if Norm1 ==0 or Norm2==0:
        return 0
    else:
        return np.dot(Fea1,Fea2)/np.linalg.norm(Fea1)/np.linalg.norm(Fea2)

def GetTopSimilarityNodes(G,NodeId,NodeFea,TopK=5,RecursiveNum=1):
    GNodesNum = G.GetNodes()
    SimilarityArr = np.zeros(GNodesNum)
    for NI in G.Nodes():
        NID = NI.GetId()
        if NID != NodeID:
            NIFea = GetNodeRecursiveFea(G,NID,RecursiveNum)
            SimilarityArr[NID] = CalSimilarity(NodeFea,NIFea)

    NodesID = np.argsort(-SimilarityArr)        # '-' minus for ascending order
    NodesID = NodesID[:TopK]
    
    return NodesID

#Q2.2
def GetFea(FeaList,flag = 'mean'):
    fea = FeaList[0]
    for fea0 in FeaList[1:]:
        fea = fea+fea0
    if flag == 'mean':
        return fea/len(FeaList)
    elif flag == 'sum':
        return fea
    else:
        print("undefined: ",flag)

#recursive method
def GetNodeRecursiveFea(G,NodeID,RecursiveNum=3):
    Node = G.GetNI(NodeID)
    Deg = Node.GetDeg()
    if RecursiveNum == 1:
        return GetNodeFea(G,NodeID)
    else:
        NbrFeaList = []
        NodeFea = GetNodeRecursiveFea(G,NodeID,RecursiveNum-1)
        if Deg ==0:
            return np.concatenate((NodeFea,np.zeros(3**(RecursiveNum-1)),np.zeros(3**(RecursiveNum-1))))
        else:
            for i in range(Deg):
                NbrID = Node.GetNbrNId(i)
                NbrFea = GetNodeRecursiveFea(G,NbrID,RecursiveNum-1)
                NbrFeaList.append(NbrFea)
                NbrFeaMean = GetFea(NbrFeaList,'mean')
                NbrFeaSum = GetFea(NbrFeaList,'sum')
            return np.concatenate((NodeFea,NbrFeaMean,NbrFeaSum))
        
#Q2.1 main
NodeID = 9
NodeFea = GetNodeFea(G,NodeID)
NodesID = GetTopSimilarityNodes(G,NodeID,NodeFea,)
print("Q2.1.1 Basic feature vector for Node with ID 9: ",NodeFea)
print("Q2.1.2 Top 5 nodes that are most similar to node 9: ",NodesID)



#Q2.2 main
NodeRecursiveFea = GetNodeRecursiveFea(G,NodeID,RecursiveNum=3)
NodesID2 = GetTopSimilarityNodes(G,NodeID,NodeRecursiveFea,RecursiveNum=3)
print("Q2.2 Top 5 nodes that are most similar to node 9 in terms of recursive feature: ",NodesID2)

#2.3
def GetSimilarityArr(G,NodeId,NodeFea,RecursiveNum=1):
    GNodesNum = G.GetNodes()
    SimilarityArr = np.zeros(GNodesNum)
    for NI in G.Nodes():
        NID = NI.GetId()
        if NID != NodeID:
            NIFea = GetNodeRecursiveFea(G,NID,RecursiveNum)
            SimilarityArr[NID] = CalSimilarity(NodeFea,NIFea)
    return SimilarityArr

def GetRandomNodeID(SimilarityArr,interval):
    indices = (SimilarityArr>interval[0])*1*((SimilarityArr<interval[1])*1)
    index = np.nonzero(indices)[0]
    return int(np.random.choice(index))

def PlotSubGraph(G,NodeID,path="./graph/"):
    Node = G.GetNI(NodeID)
    NIdV = snap.TIntV()         #subgraph nodes ID
    NIdV.Add(NodeID)
    Deg = Node.GetDeg()
    NidName = snap.TIntStrH()
    NidName[NodeID] = str(NodeID)
    for i in range(Deg):
        NbrID = Node.GetNbrNId(i)
        NIdV.Add(NbrID)
        NidName[NbrID] = str(NbrID)
        SubGraph = snap.GetSubGraph(G, NIdV)
    snap.DrawGViz(SubGraph,snap.gvlDot,path+"subgraph"+str(NodeID)+".png","SubGraph of "+str(NodeID),NidName)    
    return 0
#Q2.3 main
#plot histogram
SimilarityArr = GetSimilarityArr(G,NodeID,NodeRecursiveFea,RecursiveNum=3)
plt.hist(SimilarityArr,bins = 20)

#plot subgraph
PlotSubGraph(G,9)
RandomNodeID1 = GetRandomNodeID(SimilarityArr,[0.6,0.65])
RandomNodeID2 = GetRandomNodeID(SimilarityArr,[0.85,0.9])
RandomNodeID3 = GetRandomNodeID(SimilarityArr,[0.9,0.95])
PlotSubGraph(G,RandomNodeID1)
PlotSubGraph(G,RandomNodeID2)
PlotSubGraph(G,RandomNodeID3)
print("Q2.3.1 Basic feature vector for Node with ID %d: "%(RandomNodeID1),GetNodeFea(G,RandomNodeID1))
print("Q2.3.2 Basic feature vector for Node with ID %d: "%(RandomNodeID2),GetNodeFea(G,RandomNodeID2))
print("Q2.3.3 Basic feature vector for Node with ID %d: "%(RandomNodeID3),GetNodeFea(G,RandomNodeID3))