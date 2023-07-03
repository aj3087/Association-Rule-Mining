import pandas as pd 
import numpy as np
from collections import Counter
import copy
import math
import json

def generateFirstPassCandidate(df, minsup):
    '''
    Generates the candidate elements for set withh a single element. Returns a counter of all the elements and the candidate Set in sorted order
    '''
    
    n = len(df)
    ctr = {}
    for i in range(n):
        row =  list(df.values[i])
        for entry in row:
            if entry != '' and entry!= None and entry!="nan" and not pd.isna(entry): # Filter out unneeded entries
                ctr[tuple([entry])] = ctr.get(tuple([entry]),0) + 1
    
    candidateSet = [] 
    for key in ctr:
        if (ctr[key]/n) >= minsup:
            candidateSet.append(key) # only add those candidate key that have support greater than the min support provided
            
    return sorted(candidateSet),ctr 

def pruneCandidateSet(candidateSets, lprev):
    # prunning set to remove such sets from candidate sets which posses a k-1 length subset that is not part of lprev
    prunnedCandidateSet = []
    
    for candidateSet in candidateSets:
        # generating all the subset os candidateSet with k-1 length
        allSubset = [] # all subsets of k-1 length
        n = len(candidateSet)
        
        for i in range(n):
            allSubset.append(candidateSet[:i]+candidateSet[i+1:])
        
        # if any one of the k-1 length subset is missing we don't included the candidateSet
        
        include = True
        for subset in allSubset:
            if subset not in lprev:
                include = False
                break
        if include:
            prunnedCandidateSet.append(candidateSet)
        
        
    
    return prunnedCandidateSet

def generateCandidateSet(lprev):
    # lprev is a set of len k-1 
    candidateSet = []
    
    n = len(lprev)
    
    for i in range(n):
        for j in range(i+1,n):
            if lprev[i][:-1] == lprev[j][:-1] and lprev[i][-1] < lprev[j][-1]: #  Expands the largeItemSets such that first k-2 items are smae andd only differ in kth item
                candidateSet.append(lprev[i]+tuple([lprev[j][-1]]))
    
    candidateSet = pruneCandidateSet(candidateSet,lprev) # Prune the candidate Set to exclude such sets that have atleast onee subset not part of k-1 largeItemset since that would  violate Apriori Property
    
    return candidateSet

def generateLargeItemSet(df, minSup):
    largeItemSet = []   
    
    dataSet = df.values
    
    n = len(dataSet)
    
    # Add an optimization to reduce the df size each time, no need to do a complete scan
    
    lprev,counter = generateFirstPassCandidate(df, minSup) # Generate the candidateSet for first pass
    largeItemSet = largeItemSet + lprev
    
    while lprev:
        candidateSet = generateCandidateSet(lprev) # Generate candidate set of length k+1
        lnext = []
        
        for entry in candidateSet:
            tempDf = df.isin(list(entry)) 
            
            resPerRow = (tempDf.values+0).sum(1)
            n1 = len(entry)
            count = sum(i >= n1 for i in resPerRow)
            
            counter[entry] = count
            
            if count/n >= minSup:
                lnext.append(entry) # Generating largeItemSet of length K+1 
        
        if lnext:
            largeItemSet = largeItemSet + lnext
        lprev = copy.copy(lnext)
    
    return largeItemSet,counter