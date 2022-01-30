# -*- coding: utf-8 -*-
"""SeqeunceAlignment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OJQCKzvmrWj1E7A0zuX8oaS4amdmyiNU
"""

pip install biopython

from Bio.Align import substitution_matrices
def sigma(c1, c2): #implement subs matrix here
  m = substitution_matrices.load("BLOSUM62")
  return m[c1.upper(), c2.upper()]

def needleman_wunsch(seq1, seq2):
  lingap = 2 
  T = arr = [[0 for j in range(len(seq1)+1)] for i in range(len(seq2)+1)] # seq1 is cols and seq2 is rows, so j(seq1) is for cols and i(seq2) is for rows

  T[0][0] = (0, (0 , 0))#, (0, 0)) 

  for i in  range(1, len(seq2)+1): #filling all the col 0
    temp = T[i-1][0][0]
    T[i][0] = (temp - lingap, (i - 1, 0))#, (i, 0))

  for j in range(1, len(seq1)+1): # filling all of row 0
    temp = T[0][j - 1][0]
    T[0][j] = (temp - lingap, (0, j - 1))#, (0, j))

  for j in range(1, len(seq1)+1): #cols
    for i in range(1, len(seq2)+1): #rows
      x1 = T[i-1][j-1][0] + sigma(seq2[i-1], seq1[j-1])
      x2 = T[i-1][j][0] - lingap
      x3 = T[i][j-1][0] - lingap
      maxval = max(x1, x2, x3)
      if maxval == x1:
        temp = (i-1,j-1)
      elif maxval == x2:
        temp = (i-1, j)
      else:
        temp = (i, j-1)

      T[i][j] = (maxval, temp)

  i = len(seq2) #row
  j = len(seq1) #col

  aseq1 = ""
  aseq2 = ""
  
  while i > 0 and j > 0:
    t1 = T[i][j][1][0]
    t2 = T[i][j][1][1]

    if i - 1 == t1 and j - 1 == t2:
      aseq2 = aseq2 + seq2[i - 1]
      aseq1 = aseq1 + seq1[j - 1]
      i = t1 
      j = t2 
    elif i == t1 and j - 1 == t2:
      aseq2 = aseq2 + "-"
      aseq1 = aseq1 + seq1[j - 1]
      j = t2
    elif i - 1 == t1 and j == t2:
      aseq2 = aseq2 + seq2[i - 1]
      aseq1 = aseq1 + "-"
      i = t1
      
  if i > 0:
    temp = seq2[0:i]
    aseq2 = aseq2 + temp[::-1]
    while (i > 0):
      aseq1 = aseq1 + "-"
      i = i - 1
  elif j > 0:
    temp = seq1[0:j]
    aseq1 = aseq1 + temp[::-1]
    while (j > 0):
      aseq2 = aseq2 + "-"
      j = j - 1

  return (T[len(seq2)][len(seq1)][0], aseq1[::-1], aseq2[::-1])

import numpy as np
from Bio.Align import substitution_matrices

def sigma3(c1, c2): #implement subs matrix here
  m = substitution_matrices.load("BLOSUM62")
  return m[c1.upper(), c2.upper()]

def smith_waterman_helper(seq1, seq2):
  lingap = 2 
  T = np.zeros((len(seq2)+1, len(seq1)+1))
  T[0,0] = 0 

  for i in  range(1, len(seq2)+1): #filling all the col 0
    temp = T[i-1,0]
    if (temp - lingap) < 0:
      T[i,0] = 0 
    else:
      T[i,0] = temp - lingap 

  for j in range(1, len(seq1)+1): 
    temp = T[0,j - 1]
    if (temp - lingap) < 0:
      T[0,j] = 0 
    else:
      T[0,j] = temp - lingap 

  for j in range(1, len(seq1)+1): #cols
    for i in range(1, len(seq2)+1): #rows
      x1 = T[i-1,j-1] + sigma3(seq2[i-1], seq1[j-1])
      x2 = T[i-1,j] - lingap
      x3 = T[i,j-1] - lingap
      maxval = max(x1, x2, x3)
     
      if (maxval < 0):
        T[i,j] = 0 
      else:
        T[i,j] = maxval 
 
  return T

def smith_waterman(T, seq1, seq2):
  res = np.where(T == np.amax(T))
  i = res[0][0]
  j = res[1][0]
  a1 = ""
  a2 = ""
  while T[i, j] != 0:
    a1 = a1 + seq2[i-1]
    a2 = a2 + seq1[j-1]
    i = i - 1
    j = j - 1
  
  return (a1[::-1], a2[::-1])

from Bio.Align import substitution_matrices

def sigma2(c1, c2): #implement substitution matrix here
  m = substitution_matrices.load("BLOSUM62")
  return m[c1.upper(), c2.upper()]

def affine_gaps(seq1, seq2):
  neginf = float('-inf')

  gapopen = -10
  gapext = -1

  T = [[{"M":[neginf, (0,0), ((0,0), "")], "Ix":[neginf, (0,0), ((0,0), "")], "Iy":[neginf, (0,0), ((0,0), "")]} for j in range(len(seq1)+1)] for i in range(len(seq2)+1)]

  T[0][0]["M"][0] = 0

  for i in range(0, len(seq2)+1):
    T[i][0]["Ix"][0] = gapopen + gapext * i
    T[i][0]["Ix"][1] = (i, 0)
    if i == 0:
      continue
    else:
      T[i][0]["Ix"][2] = ((i - 1, 0), "Ix")

  for j in range(0, len(seq1)+1):
    T[0][j]["Iy"][0] = gapopen + gapext * j
    T[0][j]["Iy"][1] = (0, j)
    if j == 0:
      continue
    else:
      T[0][j]["Iy"][2] = ((0, j - 1), "Iy")

  for i in range(1, len(seq2)+1):
    for j in range(1, len(seq1)+1):
      m1 = T[i-1][j-1]["M"][0] + sigma2(seq1[j - 1], seq2[i - 1])
      m2 = T[i-1][j-1]["Ix"][0] + sigma2(seq1[j - 1], seq2[i - 1])

      m3 = T[i-1][j-1]["Iy"][0] + sigma2(seq1[j - 1], seq2[i - 1])

      ix1 = T[i-1][j]["M"][0] + gapopen 
      ix2 = T[i-1][j]["Ix"][0] + gapext

      iy1 = T[i][j-1]["M"][0] + gapopen 
      iy2 = T[i][j-1]["Iy"][0] + gapext

      m_max = max(m1, m2, m3)

      if m_max == m1:
        T[i][j]["M"][0] = m_max
        T[i][j]["M"][1] = (i, j)
        T[i][j]["M"][2] = ((i - 1, j - 1), "M")
      elif m_max == m2:
        T[i][j]["M"][0] = m_max
        T[i][j]["M"][1] = (i, j)
        T[i][j]["M"][2] = ((i - 1, j - 1), "Ix")
      else:
        T[i][j]["M"][0] = m_max
        T[i][j]["M"][1] = (i, j)
        T[i][j]["M"][2] = ((i - 1, j - 1), "Iy")
      
      ix_max = max(ix1, ix2)

      if ix_max == ix1:
        T[i][j]["Ix"][0] = ix_max
        T[i][j]["Ix"][1] = (i, j)
        T[i][j]["Ix"][2] = ((i - 1, j), "M")
      else:
        T[i][j]["Ix"][0] = ix_max
        T[i][j]["Ix"][1] = (i, j)
        T[i][j]["Ix"][2] = ((i - 1, j), "Ix")

      iy_max = max(iy1, iy2)

      if iy_max == iy1:
        T[i][j]["Iy"][0] = iy_max
        T[i][j]["Iy"][1] = (i, j)
        T[i][j]["Iy"][2] = ((i, j - 1), "M")
      else:
        T[i][j]["Iy"][0] = iy_max
        T[i][j]["Iy"][1] = (i, j)
        T[i][j]["Iy"][2] = ((i, j - 1), "Iy")

  i = len(seq2) #row
  j = len(seq1) #col
  c = 1
  aseq1 = ""
  aseq2 = ""

  while i > 0 and j > 0:
    t1 = T[i][j]["M"][0]
    t2 = T[i][j]["Ix"][0]
    t3 = T[i][j]["Iy"][0]

    t_max = max(t1, t2, t3)

    if c == 1:
      score = t_max
      c = 0


    if t_max == T[i][j]["M"][0]:
      c1 = T[i][j]["M"][2][0][0]
      c2 = T[i][j]["M"][2][0][1]
      aseq1 = aseq1 + seq1[j - 1]
      aseq2 = aseq2 + seq2[i - 1]
    elif t_max == T[i][j]["Ix"][0]:
      c1 = T[i][j]["Ix"][2][0][0]
      c2 = T[i][j]["Ix"][2][0][1]
      aseq1 = aseq1 + "-"
      aseq2 = aseq2 + seq2[i - 1]
    else:
      c1 = T[i][j]["Iy"][2][0][0]
      c2 = T[i][j]["Iy"][2][0][1]
      aseq1 = aseq1 + seq1[j - 1]
      aseq2 = aseq2 + "-"

    i = c1
    j = c2

  if i > 0:
    temp = seq2[0:i]
    aseq2 = aseq2 + temp[::-1]
    while (i > 0):
      aseq1 = aseq1 + "-"
      i = i - 1
  elif j > 0:
    temp = seq1[0:j]
    aseq1 = aseq1 + temp[::-1]
    while (j > 0):
      aseq2 = aseq2 + "-"
      j = j - 1

  return (score, aseq1[::-1], aseq2[::-1])