# -*- coding: utf-8 -*-
"""AI lab 9.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qRk5KLjOZipRjEJuLCBT37T9A-NLTvUu
"""

import random
# --- Bandit ---
class Bandit(object):
  def __init__(self, N):
    # N = number of arms
    self.N = N
  def actions(self):
    result = []
    for i in range(0,self.N):
      result.append(i)
    return result
  def rewardA(self, action):
    p =[.1, .2]
    rand=random.random()
    if rand < p[action]:
      return 1
    else:
      return 0
  def rewardB(self, action):
    p =[.8, .9]
    rand=random.random()
    if rand < p[action]:
      return 1
    else:
      return 0

myBandit = Bandit(N=2)

myBandit.actions()

def eGreedy(myBandit, epsilon, max_iteration):
  # Initialization 
  Q = [0]*myBandit.N 
  count = [0]*myBandit.N
  epsilon = epsilon
  r = 0
  R = []
  R_avg = [0]*1
  max_iter = max_iteration
  # Incremental Implementation
  for iter in range(1,max_iter):
    if random.random() > epsilon:
      action = Q.index(max(Q)) # Exploit/ Greed
    else:
      action = random.choice(myBandit.actions()) # Explore
    r = myBandit.rewardB(action)
    R.append(r)
    count[action] = count[action]+1
    Q[action] = Q[action]+(r - Q[action])/count[action]
    R_avg.append(R_avg[iter-1] + (r-R_avg[iter-1])/iter)

  return Q, R_avg, R

Q,R_avg,R = eGreedy(myBandit, 0.1, 1000)

Q

import matplotlib.pyplot as plt
plt.plot(R_avg)