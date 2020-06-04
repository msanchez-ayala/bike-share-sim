# bike-share-sim

[![Build Status](https://travis-ci.com/msanchez-ayala/bike-share-sim.svg?branch=master)](https://travis-ci.com/msanchez-ayala/bike-share-sim)


A Python simulation of a bike share such as Citibike. The goal is to practice
my OOP skills by creating a simple bike share simulation. There are only a 
handful of objects in this project.

## Classes
1. Bike
2. Dock
3. Station
4. Simulation

## How the Simulation Works
1. Bike share system is initialized with a predetermined simulation run time 
(in minutes) that can be changed in `__main__.py`, 9 stations, 135 docks, and 
80 bikes. Each station is located in a 3x3 grid that will help calculate how 
long trips are between stations.
2. Every minute of the simulation, the probability of customers renting a bike 
is simulated as a Poisson process, and anywhere from about 0-4 (possible although 
very unlikely 4 people will check out) people can potentially check out a bike.
3. When a customer does check out a bike, they do so from a randomly chosen station.
That customer then travels **directly** to another randomly chosen station in the system. 
When they arrive, they can check in the bike if there are any available docks. 
If not, they have to travel to another station and try there. By "directly" I mean that
there are no joy rides that for instance could result in someone starting and ending
at the same dock. Furthermore, this simplifies the calculation of travel time, as it is assumed
that any trip between two locations is purely a function of distance and speed which can be predetermined.
4. When a customer checks a bike in or out, the time is recorded along with the 
station id number.
5. At the end of the simulation, a full log of all activity is printed for review.

## How to run
Clone this repo and ensure a Python3 environment with the required packages.  You must be in the directory containing
`bike-share-sim` in order to run
```
python bike-share-sim
```
A summarized log of activity each minute will be printed out, as well as some
statistics about the entire simulation at the end.

## Next Steps
I would love to build the following once the base simlation is done.
1. Include command line inputs for the size of the simulation.
2. Build a simple GUI to visualize the demonstration
3. Incorporate other bike types such as ElectricBike (and thus perhaps ElectricDock)
