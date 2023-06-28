#!/usr/bin/env python
# coding: utf-8

# # 2021-0802 Zach Gardner
# 
# Prepared by Nick Machairas
# 
# Updated on Aug 18 2021
# 
# Assumptions:
# - Layers are always encountered in the order presented (columns left to right)
# 

# In[1]:


import os
import numpy as np
import pandas as pd


# In[2]:


df = pd.read_excel(
    os.path.join('files', '2021-0813-HAI-BWH-SummaryTable.xlsx'),
    usecols='B,D,E,I,K,N,Q,T,W,Z,AC',
    skiprows=[0,1,2,3,5,6,7],
    na_values=['NE', 'ne'],
)


# In[3]:


df.info()


# In[4]:


df


# Main script:

# In[5]:


with open(os.path.join('files', '2021-0813 - Field Geological Descriptions.csv'), 'w') as f:
    f.write('Location ID,Depth Top,Depth Base,Geology Code,Location Code\n')
    for i in df.index:
        bor = df.iloc[i]
        if pd.notna(bor['TEST BORING']):
            bor = bor.dropna()
            layers = list(bor[3:].items())
            if layers:
                for k, l in zip(layers[:-1], layers[1:]):
                    f.write(f"{bor['TEST BORING']},{k[1]},{l[1]},{k[0]},{bor['SOURCE FILE NAME']}\n")
                f.write(f"{bor['TEST BORING']},{layers[-1][1]},{bor['DEPTH OF']},{layers[-1][0]},{bor['SOURCE FILE NAME']}\n")


# In[ ]:




