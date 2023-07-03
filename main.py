import pandas as pd 
import numpy as np
from collections import Counter
import copy
import math
import json
import sys
from associationRule import generateAssociationRules
from largeItemSet import generateLargeItemSet

def main(fileName,minSup,minConf,outputFile = "output.txt"):
    minSup = float(minSup)
    minConf = float(minConf)
    df = pd.read_csv(fileName,dtype=str) # reading the csv file and converting it into a dataFrame for efficeint processing
    n = len(df)
    
    df = df.apply(lambda x: pd.Series(x,dtype=str).drop_duplicates(), axis=1) # Removing Duplicate values from the Row and replacing the duplicates with Nan

    largeItemSet,counter = generateLargeItemSet(df, minSup) # generating Large Item Sets on basis of min Support from the df
    
    f = open(outputFile, 'w') # opening the output 

    
    largeItemSet.sort(key = lambda x : counter[x],reverse = True) # Sorting the large itemsets in decreasing order of support
    
    
    f.write("==Frequent itemsets (min_sup="+ str(minSup*100) + "%) \n") # Printing the Large ItemSets
    for itemSet in largeItemSet:
        json.dump(list(itemSet),f)
        f.write("," + str((counter[itemSet]/n)*100) + "% \n" )
    
    rules = generateAssociationRules(largeItemSet,counter,minConf) # Generating the Assoction Rules with Confidence >= min_confidence
    
    rules.sort(key = lambda x: (x[2],x[3]) , reverse = True) # Sorting the assoication Rules based on 

    f.write("==High-confidence association rules (min_conf="+ str(minConf*100) + "%) \n")
    for rule in rules:
        json.dump(list(rule[0]),f)
        f.write(" => ")
        json.dump(list(rule[1]),f)
        f.write(" (Conf: " + str(rule[2]*100) + "%, Supp: " + str((rule[3]/n)*100) + "%) \n")    

        
data=sys.argv[1:]
print(data)
main(*data)