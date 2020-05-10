# bike-share-sim
A Python simulation of a bike share such as Citibike. The goal is to practice
my OOP skills by creating a simple bike share simulation. There are only a 
handful of objects in this project.

### Classes
1. Bike -> ClassicBike, ElectricBike (not yet implemented)
2. Dock
3. Station
4. Simulation

### How to run
The project currently has no external dependencies. Simply ensure a Python3 
environment and clone this repo. Then navigate into bike-share-sim. Lastly,
run
```
python sim
```
It currently doesn't do much other than instantiate two Stations, each with one
Dock. One of those two docks is filled with a ClassicBike that will travel 
back and forth between the two stations as such:
![basic_sim](/images/basic_sim.png)

### Next Steps
Once the basic simulation above is configured correctly, I'll expand one at
a time for the following:
1. Adding more stations
2. Adding more docks/bikes to stations
3. Add ability to export all stations' bike logs to a PostgreSQL db to then
visualize bike ride statistics.