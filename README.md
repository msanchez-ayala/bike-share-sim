# bike-share-sim
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
(in minutes), number of stations, docks, and bikes. Each station has a location
that will help calculate how long trips are between stations.
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
The project currently has no external dependencies. Simply ensure a Python3 
environment and clone this repo. You must be in the directory containing
`bike-share-sim` in order to run
```
python bike-share-sim
```
By default, a 120-minute simulation is run with 9 stations, each containing a varying
number of docks. There are a total of 120 bikes.  

## Next Steps
I would love to build the following once the base simlation is done.
1. Build a simple GUI to visualize the demonstration
2. Incorporate other bike types such as ElectricBike (and thus perhaps ElectricDock)