#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 09:55:02 2020

@author: qiuwenjie
"""

'''
cs224w homework 0
Q1 & Q2
'''
import snap as sp
import numpy as np
import matplotlib.pyplot as plt
#load graph
G = sp.LoadEdgeList(sp.PNGraph, "Wiki-Vote.txt",0,1)

#------------------------------------------------------------------------------
#Q1
GNodesNum= G.GetNodes()
print("Q1.1 The number of nodes in the network: ",GNodesNum)

SelfLoopNum = 0
for EI in G.Edges():
    if EI.GetSrcNId() == EI.GetDstNId():
        SelfLoopNum += 1
print("Q1.2 The number of nodes with a self-edge: ",SelfLoopNum)

DirecEdgeNum = 0
for EI in G.Edges():
    if EI.GetSrcNId() != EI.GetDstNId():
        DirecEdgeNum += 1
print("Q1.3 The number of directed edges in the network: ",DirecEdgeNum)

UDirecEdgeNum = 0
for EI in G.Edges():
    if EI.GetSrcNId() != EI.GetDstNId():
        if G.IsEdge(EI.GetDstNId(),EI.GetSrcNId()) == False:
            UDirecEdgeNum += 1
        else:
            UDirecEdgeNum +=0.5
print("Q1.4 The number of undirected edges in the network: ",UDirecEdgeNum)

RecEdgeNum = 0
for EI in G.Edges():
    if EI.GetSrcNId() != EI.GetDstNId():
        if G.IsEdge(EI.GetDstNId(),EI.GetSrcNId()):
            RecEdgeNum += 0.5
print("Q1.5 The number of reciprocated edges in the network: ",RecEdgeNum)

ZOutNum = 0
for NI in G.Nodes():
    if NI.GetOutDeg() == 0:
        ZOutNum +=1
print("Q1.6 The number of nodes of zero-out edge: ",ZOutNum)

ZInNum = 0
for NI in G.Nodes():
    if NI.GetInDeg() == 0:
        ZInNum +=1
print("Q1.7 The number of nodes of zero-in edge: ",ZInNum)

OutG10Num = 0
for NI in G.Nodes():
    if NI.GetOutDeg() > 10:
        OutG10Num +=1
print("Q1.8 The number of nodes with more than 10 outgoing edge: ",OutG10Num)

InF10Num = 0
for NI in G.Nodes():
    if NI.GetInDeg() < 10:
        InF10Num +=1
print("Q1.9 The number of nodes with fewer than 10 incoming edge: ",InF10Num)
#Q1 end
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
#Q2
OutDegDict = {}
for NI in G.Nodes():
    OutDeg = NI.GetOutDeg() 
    if OutDeg > 0:
        if OutDeg in OutDegDict.keys():
            OutDegDict[OutDeg] += 1
        else:
            OutDegDict[OutDeg] = 1
OutDegArr = np.array(sorted(OutDegDict))
OutDegArrNum = np.zeros(OutDegArr.shape[0])
for i in range(len(OutDegArrNum)):
    OutDegArrNum[i] = OutDegDict[OutDegArr[i]]
print('Q2')
ax = plt.gca()
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_adjustable("datalim")
ax.set_xlabel('Out-Degree')
ax.set_ylabel('Count')
ax.set_title('The distribution of out-degrees of nodes in the network')
plt.plot(OutDegArr, OutDegArrNum,'-',label='Out-Degree Distribution')
LogOutDegArr = np.log10(OutDegArr)
LogOutDegArrNum = np.log10(OutDegArrNum)
reg=np.polyfit(LogOutDegArr,LogOutDegArrNum,1)
LogOutDegArrNumEst=np.power(10,reg[1])*np.power(OutDegArr,reg[0])
plt.plot(OutDegArr,LogOutDegArrNumEst,'-',label='Least-Square Regression')
ax.set_xlim(OutDegArr[0], OutDegArr[-1])
#ax.set_ylim(min(OutDegArrNum), max(OutDegArrNum))
ax.grid()
plt.legend()


