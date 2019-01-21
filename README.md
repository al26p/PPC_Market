# PPC_Market
Project for PPC 3TC - Modeling of an energetic market

### Collaborators
- @al26p
- @AeredrenInsa

### Setup
install required requirements : 

`pip3 install -r requirements.txt`

(Tkinter is needed too. should be installed by default. Otherwise, google it ;) )

### How to launch the simulation
The main.py script launch all the process of the simulation. Just type 

`python3 main.py`

To stop, press enter ('STOP' should appears, multiples press can be mandatory)

Parameter are hard coded, if you want to change the number of houses, their politics or the clock for the different process change them at the creation in the main.
The probabilities for external event can be change in External.py

### Real data :
Meteorological data from Reykjavik, monthly, from 1949 to 2018

kW/h price in France : 0.1469€

average consumption in kW/h in France : 4760 kW/h per Year -> ~300 kW/h per month

### Simulation info :
Each tick of the weather Clock represent 1 month.
