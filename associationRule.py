import pandas as pd 
import numpy as np
from collections import Counter
import copy
import math
import json
def generateAssociationRules(largeItemSet,counter,minConf):
    # All the items in largeItemSet have sufficent support we need to find assoication rules from large itemsets such that they have good confidence
    associationRule = [] # tuples (LHS,RHS,confidence,support)
    for itemSet in largeItemSet:
        
        n = len(itemSet)
        support = counter[itemSet]
        
        for i in range(1,n):
            LHS = itemSet[:i]
            RHS = itemSet[i:]
            
            # For rule LHS -> RHS
            conf1 = counter[itemSet]/counter[LHS]
            if conf1 >= minConf:
                associationRule.append((LHS,RHS,conf1,support))
            
            # For rule RHS -> LHS
            conf2  = counter[itemSet]/counter[RHS]
                    
            if conf2 >= minConf:
                associationRule.append((RHS,LHS,conf2,support))
    
    return associationRule