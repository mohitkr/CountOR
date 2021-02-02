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


def readCSV(fileName):
    with open(fileName, "rU") as csvFile:
        reader = csv.reader(csvFile, delimiter=",")
        data = list(reader)
        data = np.asarray(data)
        return data

def cleanData(data):
   variables = []
   rows, cols = data.shape
   blankRows = 0
   while not data[blankRows, 0]:
       blankRows += 1
   blankCols = 0
   while not data[0, blankCols]:
       blankCols += 1
   for i in range(blankRows):
       variables.append(list(OrderedDict.fromkeys(data[i, blankCols:])))
   for i in range(blankCols):
       variables.append(list(OrderedDict.fromkeys(data[blankRows:, i])))
   variables_mat = np.matrix(variables)

   lengths = []
   for i in range(variables_mat.shape[1]):
       lengths.append(len(variables_mat[0, i]))
   dataTensor = np.zeros(lengths)

   for i in range(blankRows, rows):
       for j in range(blankCols, cols):
           if int(data[i, j]) == 1:
               index = ()
               for k in range(blankRows):
                   index = index + (variables[k].index(data[k, j]),)
               for k in range(blankCols):
                   index = index + (variables[blankRows + k].index(data[i, k]),)
               dataTensor[index] = 1
   return dataTensor, variables


def getConstraintsForAll(dataTensor, variables, orderingNotImp):
    repeatDim = ()
    r = set([v for v in range(len(variables)) if v not in repeatDim])

    constraints = {}
    for l, (m, s) in enumerate(cf.split(r, (), repeatDim)):
        newset = m + s

        # this value will be used to filter max constraints
        maxPossible = 1
        for i in range(len(s)):
            maxPossible *= len(variables[s[i]])
        idTensor = cf.tensorIndicator(dataTensor, newset, variables)
        sumSet = range(len(m), len(newset))

        sumTensor_max, sumTensor_min = cf.tensorSum(
            idTensor, sumSet, np.array(variables)[list(newset)], 0
        )

        if len(set(s)) == 1 and len(set(orderingNotImp) & set(s)) == 0:
            minConsZero, maxConsZero, minConsNonZero, maxConsNonZero = cf.tensorConsZero(
                idTensor, sumSet, np.array(variables)[list(newset)]
            )
        else:
            minConsZero, maxConsZero, minConsNonZero, maxConsNonZero = (
                None,
                None,
                None,
                None,
            )
        row = {}
        row["minSum"] = sumTensor_min
        row["maxSum"] = sumTensor_max
        row["minConsZero"] = minConsZero
        row["minConsNonZero"] = minConsNonZero
        row["maxConsZero"] = maxConsZero
        row["maxConsNonZero"] = maxConsNonZero

        constraints[(m, s)] = row

    return constraints


def learnConstraints(dataTensor, dim):
    variables = []
    for d in dim:
        variables.append(list(range(d)))
    lenVar = []
    for i in range(len(variables)):
        lenVar.append(len(variables[i]))
    orderingNotImp = [2]
    return getConstraintsForAll(dataTensor, variables, orderingNotImp)


def learnConstraintsFromCSV(csvFile):
    data = readCSV(csvFile)
    dataTensor, variables = cleanData(data)
    lenVar = []
    for i in range(len(variables)):
        lenVar.append(len(variables[i]))
    orderingNotImp = [2]
    constraints = getConstraintsForAll(dataTensor, variables, orderingNotImp)
    return constraints
