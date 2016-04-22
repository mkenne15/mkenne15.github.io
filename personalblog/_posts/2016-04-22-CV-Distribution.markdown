---
layout: post
title:  "The distribution of eclipses and inclination in Cataclysmic Variables"
date:   2016-04-22
categories: personal
---

So here's a little project I need to do for an appendix in my thesis, which I thought was interesting. You might not find it interesting. And if you don't, I don't know what you were expecting when reading the blog of an astrophysicist.

Anyway, here we go. The problem. There's a big list which contains lots of information about cataclysmic variables (**[the Ritter & Kolb list](http://wwwmpa.mpa-garching.mpg.de/RKcat/)**). I want to take data from this list, and make a plot which shows what the mean eclipse depth is for a system, given an orbital inclination.

My own attempt is to use python, since it's probably the language I know best. The following is the full code for it



```python
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as ndimage
from scipy import stats


data = np.genfromtxt("/home/mark/Data/j1923/eclipsecv_new.dat",delimiter='\t') #Loading the list, which I've already edited to be short

x = data[:,2] # Inclination is in the 3rd column for me 
y = data[:,1]-data[:,0] # data[:,0] is  normal magnitude, data[:,1] is eclipse magnitude

inclination = [] #Defining empty arrays
mean_mag = [] #Defining empty arrays
error_mag = [] #Defining empty arrays

for i in np.arange(10,90,5): #Nice little for loop to bin the data
    inclination = np.append(inclination,i)
    mean_mag = np.append(mean_mag,np.mean(y[(x >= i) & (x <= i+5)]))
    error_mag = np.append(error_mag,np.std(y[(x >= i) & (x <= i+5)]))

#Making a pretty plot
plt.bar(inclination,mean_mag,width=5)
plt.errorbar(inclination+2.5,mean_mag,yerr=error_mag,fmt='k.', ecolor='r')
plt.xlim(0,90)
plt.ylabel("Mean Eclipse Depth (Mag)")
plt.xlabel(r"Inclination ($\degree$)")
plt.show()
```

The above code produces the following plot, which is exactly what I wanted.

![Distriubtion of eclipse depth in CVs over inclination](/assets/cv_ritter_kolb.jpg)

The above graph is important for the paper I recently published on the object J1923 (**[ArXiv](http://arxiv.org/abs/1604.05718)**) as, early on in the paper, we claim the inclination for this system is above 70 degrees based on its eclipse depth. This claim came from producing the above plot!
