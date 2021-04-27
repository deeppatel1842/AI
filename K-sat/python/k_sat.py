# -*- coding: utf-8 -*-
"""k-SAT.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WyOghlg1sDFp56XK37dQSIh7cjafLx5v
"""

from string import ascii_lowercase
import random
from itertools import combinations

print("Enter the number of clauses ")
m = int(input())
print("Enter the accept values K ")
k = int(input())
print("Enter number of variables ")
n = int(input())

def Problemgenerated(m, k, n):
    #lower Case +ve
    positive_var = (list(ascii_lowercase))[:n]
    negative_var = [c.upper() for c in positive_var]
    variables = positive_var + negative_var
    repe = 1 #how many problem you are genrerated
    problems = []
     
     
    i = 0

    while i<repe:
        c = random.sample(allCombination, m)
        if c not in problems:
            i += 1
            problems.append(list(c))
            
    problems_new = []
    for c in problems:
        temp = []
        for sub in c:
            temp.append(list(sub))
        problems_new.append(temp)
    return problems

problems = Problemgenerated(m, k, n)

for i in range(len(problems)):
    print(problems[i])