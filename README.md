# Step-Counter
#### A simple step counting Android App
The application is built using python and kivy. It is packaged for android using the buildozer toolset:
https://github.com/kivy/buildozer

A bit of the front end comes form some of the plyer examples, check them out here:

https://github.com/kivy/plyer

#### Algorithmic Approach
Accelerometer data is smoothed using median smoothing with a sliding window of 50 samples (15 sample overlap)
From there, peak detection determines steps. The red bar on the graph here indicates each time someone is stepping. 

![alt text](https://cloud.githubusercontent.com/assets/8022792/25584152/d7a34ebc-2e62-11e7-9147-35e3eb6c3c49.png)
