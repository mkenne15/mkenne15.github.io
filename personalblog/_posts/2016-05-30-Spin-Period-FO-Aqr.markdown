---
layout: post
title:  "Let's talk about the spin period of FO Aqr"
date:   2016-05-30
categories: personal
---

*The following work is based off of data taken using the Kepler telescope during its K2 mission. You can download the data and work on it yourself if you want at the* **[MAST website](https://archive.stsci.edu/k2/data_search/search.php)**

At the start of April, a collaboration of us between UCC, Notre Dame, the University of Washington, the University of Warwick and the Chinese Academy of Science published a paper about the cataclysmic variable FO Aqr (you can read the paper **[here](http://arxiv.org/abs/1604.02146)**). In it, we conclude that the spin period of the white dwarf is 1254.3401(4) seconds (that last digit in brackets is the error in our period, so the error is 0.0004 seconds).

Last week, there was another paper (available **[here](http://arxiv.org/abs/1605.08030)**) which claims, using the exact same data, and the exact same technique for periodicity (the Lomb-Scargle periodogram) that the spin period is 1254.2204(21) seconds.

Now this difference might seem small (it's only 0.12 seconds), but it's outside the errors of both of our measurements. And it has serious repercussions for the conclusions of our paper. Before our paper, the last recorded spin period of FO Aqr was 1254.284(16) seconds, which is right in between our period and the period presented by Scaringi et al. So, from our measurement, you'd have to conclude that the period of the white dwarf is longer, meaning the white dwarf has slowed down. And from Scarinig et al. you'd have to conclude that the period is shorter, and that the white dwarf has sped up! So what's going on?

Sadly, I can't say for sure. I can't be sure how Scaringi et al. are exactly doing their analysis, and what normalising and averaging they're doing. But what I can do is show you how we determined the period, and make sure that what we've done makes sense.

The following section has the code which, in sections, takes the Kepler data, removes long term trends in our light curve, and also removes the orbital variation of the object, just leaving the spin signal in the data. The code then runs a Lomb-Scargle periodogram on the data, and we select the period from that periodogram that seems to match the spin period. We then perform some least-squares fitting to make sure we're at the best period, and to get a hand on the error.

The following are the moduels I'm going to use - the normal numpy and matplotlib calls, and a module called **[astroML](http://www.astroml.org/)**, which does time series analysis.

```python
import matplotlib.pyplot as plt
import numpy as np
from astroML.time_series import lomb_scargle, lomb_scargle_BIC, lomb_scargle_bootstrap
```

Loading in 1 min cadence data, and removing data with bad flags


```python
data = np.genfromtxt("/home/mark/Data/FOAqr/kepextract_drift.txt")
data = np.delete(data,np.where(data[:,5]>0),axis=0) # data[:,5] is the data column with quality flag in it. Anything > 0 must be removed
```

The following removes long term trends for the data, and normalises it


```python
poly_fit = np.polyfit(data[:,0],data[:,3],4) #Fitting a polynomial to the data to remove long term trends. data[:,0] is time in BJD, data[:,3] is flux in PDCSAP
p = np.poly1d(poly_fit)
data[:,3] = data[:,3]/p(data[:,0])-1 # data[:,3] is our extracted flux
data[:,4] = data[:,4]/p(data[:,0]) # data[:,3] is our extracted flux
```

Now that we've normalised our data and should only have the spin signal left, let's run the Lomb Scargle periodogram on it.

```python
period = np.arange(1252./(24*60*60),1257./(24*60*60),.001/(24*60*60))   # Setting up the period search range. 
                                                                        # Here, I have it set up in seconds, then 
                                                                        # convert to days, since our data is recorded 
                                                                        # in BJD
omega = 2*np.pi/period                                                  # Converting to angular frequency

PS = lomb_scargle(data[:,0], data[:,3], data[:,4], omega, generalized=True) # Runing LSP
```
The following just makes a nice plot of our periodogram

```python
plt.figure()

plt.plot(1/((omega[:]/(2*np.pi))/(24*60*60)), PS, '-', c='green',)
plt.plot([1254.2204, 1254.2204], [0, 0.35], ':', c='black')

plt.xlabel("Period (sec)",size =20)
plt.ylabel("Relative Amplitude",size =20)
plt.xticks([1253,1254,1255,1256])
plt.xlim(1253.5,1255.5)
plt.show()
```


![png](/assets/output_6_0.png)

So, now that we have a plot of the periodogram, let's see what's going on. I've obviously highly oversampled the power spectrum (way beyond the Nyquist frequency). I've marked the period from Scarinigi et al. as a black dashed line, which shows it's just before the peak value of our LSP, but still within the width of the peak. So let's do some least squares fitting, see what happens.


```python
def lmsin(x, a, f, ph):
    return a * np.sin(2 * np.pi * f * x + 2 * np.pi *ph) # A custom sine function for least squares fitting

chi2 = []

for i in period:
    model = lmsin(data[:,0],0.137,1/i,2457012.4554/i-2457012.4554//i) # definiing our model
    chi2 = np.append(chi2,np.sum(((data[:,3]-model)**2.)/(data[:,4]**2.))) # fitting for a range of periods and 
                                                                           # and calculating the chi^2 value

plt.figure()
plt.plot(period*24*60*60,chi2)
plt.plot([1254.2204, 1254.2204], [2e9, 8e9], ':', c='black')
plt.xlim(1253.5,1255.5)
plt.xticks([1253,1254,1255,1256])
plt.xlabel("Period (sec)",size =20)
plt.ylabel(r"$\chi^{2}$",size =20)
plt.show
```

![png](/assets/output_7_1.png)

I think the least squares fitting points towards whats happened. If you fix the phase of the fitted sine wave, but vary the period, you get a strange pattern in the least squares plot, which makes falling into a local minimum quite easy. Again, plotting the period from Scarinig et al. makes it look like they've fallen into one of this minimum, and the global minimum (at least for my search space) is a longer period, at the value in our paper.

However, we could still be wrong in 2 places in the above procedure. The first: the data from K2 is not calibrated or extracted for short cadence data. You have to download it and extract it yourself. Which means our aperture for extracting the light curve of FO Aqr could be different to Scaringi et al. This could be the difference between our periodograms, if they're aperture is different to our.

The second: the use of astroML's periodogram function. This is a bit fo a black box in our code, and we're trusting that it's been coded right. I'd be very interested to know how Scraringi et al calculated the LSP. However, our least-squares fitting matches the periodogram pretty well (in terms of location of best period and width of uncertainty).

I'm not going to say we're right and the other paper is wrong. Because it could still be us who is wrong. But it's still not clear to me where the difference is coming from. 


