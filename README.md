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
Clone this repo and ensure a Python3 environment with the required packages.  You must be in the directory containing
`bike-share-sim` in order to run
```
python bike-share-sim
```
By default, a 120-minute simulation is run with 9 stations, each containing a varying
number of docks. There are a total of 120 bikes.  

## Challenges
Perhaps the most difficult thing was figuring out how to simulate customers checking out bikes. I knew there
was some probability that needed to be calculated using a Poisson process. The tricky part was figuring out how to 
decide how many people each minute would consider checking out a bike and simulating whether or not they would 
actually check it out.

Knowing that I had to use the equation for Poisson distribution to calculate the probability of K number of people checking
out a bike at any given minute, I had to decide two things: 1) the average rate at which people check out bikes, and 2)
how many people could attempt to check out a bike that minute. 

### 1) Average rate
I did a little online research to find that the DC bikeshare in Q1 2012 saw on average 4 rides/minute. Although that system was larger
than mine, I simply adopted those numbers to account for the passing of times and potentially greater interest in bikes now in 2020 than
2012.

### 2) Number of people
I decided that the upper half of a normal distribution with mu = 1 and st dev = 1 would be appropriate to model the number of people
considering rending a bike at any given minute of the day for a system with 120 bikes. It seemed reasonable to me that every minute, 
generally speaking there is a chance that 1 or maybe 2 people could possibly try to check out a bike (although possible
3 or even 4 people could check one out). I say half the distribution because I only take the distribution for K >= 1 so I avoid 
calculating the probability that 0 or a negative amount of people check out bikes.

Thus, every minute of the simulation I randomly pick a K from the distribution of people described above. Then I plug K into 
the Poisson probability function to calculate the probability (as a percentage) that K people will actually check out a bike that minute. Lastly,
I pick a random number from 1-100 every minute. If random_int <= P(K), then at minute t, K people attempt to check out bikes from the system.

I say "attempt" because there is the possiblity that all bikes are currently in use, but that almost never happens. 





## Next Steps
I would love to build the following once the base simlation is done.
1. Build a simple GUI to visualize the demonstration
2. Incorporate other bike types such as ElectricBike (and thus perhaps ElectricDock)
