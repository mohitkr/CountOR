#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 17:02:20 2019

@author: mohit
"""

import csv
import numpy as np
from collections import OrderedDict
from . import constraintFormulation as cf
import os.path

def readCSV(fileName):
    with open(fileName, 'rU') as csvFile:
        reader = csv.reader(csvFile, delimiter=',')
        data = list(reader)
        data = np.asarray(data)
        return data

def cleanData(data):
    variables=[]
    rows, cols = data.shape
#     finding number of variables
    blankRows=0
    while(not data[blankRows,0]):
        blankRows+=1
    blankCols=0
    while(not data[0,blankCols]):
        blankCols+=1
    for i in range(blankRows):
        variables.append(list(OrderedDict.fromkeys(data[i,blankCols:])))
    for i in range(blankCols):
        variables.append(list(OrderedDict.fromkeys(data[blankRows:,i])))
    variables_mat=np.matrix(variables)

    lengths = []
    for i in range(variables_mat.shape[1]):
        lengths.append(len(variables_mat[0,i]))
    dataTensor=np.zeros(lengths)

    for i in range(blankRows, rows):
        for j in range(blankCols, cols):
            if data[i,j].astype(int)==1:
                index=()
                for k in range(blankRows):
                    index=index+(variables[k].index(data[k,j]),)
                for k in range(blankCols):
                    index=index+(variables[blankRows+k].index(data[i,k]),)
                dataTensor[index]=1
    return dataTensor,variables

def saveConstraintsForAll(dataTensor,variables,orderingNotImp):
    repeatDim=()
    r=set([v for v in range(len(variables)) if v not in repeatDim])
    subsets=cf.split(r,(),repeatDim)
    constraints=[]
    for l in range(len(subsets)):
        subset=subsets[l]
        newset=subset[0]+subset[1]
        # this value will be used to filter max constraints
        maxPossible=1
        for i in range(len(subset[1])):
            maxPossible*=len(variables[subset[1][i]])
        idTensor=cf.tensorIndicator(dataTensor,newset, variables)
        sumSet = range(len(subset[0]),len(newset))

        sumTensor_max,sumTensor_min=cf.tensorSum(idTensor,sumSet, np.array(variables)[list(newset)],0)

        constraints_row = [sumTensor_min, sumTensor_max]
        if len(set(subset[1]))==1 and len(set(orderingNotImp) & set(subset[1]))==0:
            minConsZero,maxConsZero,minConsNonZero,maxConsNonZero = cf.tensorConsZero(idTensor,sumSet, np.array(variables)[list(newset)])
            constraints_row.extend([minConsZero, maxConsZero, minConsNonZero, maxConsNonZero])
        else:
            constraints_row.extend([None]*4)
        constraints.append(constraints_row)

    return constraints


def learnConstraints(dataTensor,dim):
    variables = []
    for d in dim:
        variables.append(list(range(d)))
    lenVar=[]
    for i in range(len(variables)):
        lenVar.append(len(variables[i]))
    orderingNotImp=[2]
    constraints=saveConstraintsForAll(dataTensor,variables,orderingNotImp)
    return constraints
#    saveConstraintsForAll(dataTensor,variables,orderingNotImp,1,num_nurses,directory,tag+str(0))


def learnConstraintsFromCSV(csvFile):
    data = readCSV(csvFile)
    dataTensor,variables=cleanData(data)
    lenVar=[]
    for i in range(len(variables)):
        lenVar.append(len(variables[i]))
    orderingNotImp=[2]
    constraints=saveConstraintsForAll(dataTensor,variables,orderingNotImp)
    return constraints
