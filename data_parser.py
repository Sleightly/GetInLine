import pandas as pd 
import numpy as np 

df = pd.read_csv('data/data_line2.csv')

vel = []
y = []
counter = 0
for i in range(len(df['magnitude'])):
	vel.append(abs(int(df['magnitude'][i])))
	y.append(counter)
	counter += 0.3

print(vel)
#print(y)

estimatedw = []
for i in range(len(df['magnitude'])):
	div = vel[i]
	if (vel[i] < 1):
		div = 1
	estimatedw.append(1920/div/60)
print(estimatedw)

print(list(df['people']))
