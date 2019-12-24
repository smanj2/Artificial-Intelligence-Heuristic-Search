# B551 Assignment 1: Searching
##### Submission by Sri Harsha Manjunath - srmanj@iu.edu; Vijayalaxmi Bhimrao Maigur - vbmaigur@iu.edu; Disha Talreja - dtalreja@iu.edu
###### Fall 2019

## Part 1: The Luddy puzzle
Here are three variants of the 15-puzzle that we studied in class:
1. Original: This is the original puzzle. The game board consists of a 4x4 grid with 15 tiles numbered
from 1 to 15. In each turn, the player can slide a tile into an adjacent empty space. Here are two
sample moves of this puzzle:

![alt text](https://github.iu.edu/cs-b551-fa2019/vbmaigur-dtalreja-srmanj-a1/blob/master/img/Annotation%202019-10-10%20113528.jpg)

2. Circular: In this variant, all of the moves of the original game are allowed but if the empty space is on the edge of the board, the tile on the opposite side of the board can be moved into the empty space (i.e., it slides on the board and "wraps around" to the other side). If an empty space is on a corner, then two possible "circular" moves are possible.

![alt text](https://github.iu.edu/cs-b551-fa2019/vbmaigur-dtalreja-srmanj-a1/blob/master/img/Annotation%202019-10-10%20113546-2.jpg)

3. Luddy: This variant honors our school's building's namesake because all moves are in the shape of a letter "L". Specifically, the empty square may be labelled with the tile that is two positions to the left or right and one position up or down, or two positions up or down and one position left or right.

![alt text](https://github.iu.edu/cs-b551-fa2019/vbmaigur-dtalreja-srmanj-a1/blob/master/img/Annotation%202019-10-10%20113606-3.jpg)

The goal of the puzzle is to find the shortest sequence of moves that restores the canonical configuration (on the left above) given an initial board configuration. We've written an initial implementation of a program to solve these puzzles and it in your github repository. You can run the program like this:
```
./solve_luddy.py [input-board-filename] [variant]
```
where input-board-filename is a text file containing a board configuration in a format like:

```
5 7 8 1
10 2 4 3
6 9 11 12
15 13 14 0
```

where 0 indicates the empty tile, and variant is one of original, circular, or luddy. We've included a few sample test boards in your repository. While the program works, the problem is that it is quite slow for complicated boards. Using this code as a starting point, implement a faster version, using A* search with a suitable heuristic function that guarantees finding a solution in is few moves as possible.
The program can output whatever you'd like, except that the last line of output should be a machine-readable
representation of the solution path you found, in this format:

```
[move-1][move-2]...[move-n]
```
where each move is encoded as a letter, indicating the direction that a tile should be moved. For Original and Circular, the possible moves are L, R, U, or D for left, right, up, or down, respectively, indicating the direction that a tile should be moved. For example, the solution to the rightmost puzzle under Original (above) would be:

```
LU
```
For Luddy, the possible moves should be indicated with letters as follows: A for moving up two and left one, B for moving up two and right one, C for moving down two and left one, D for moving down two and right
one, E for moving left two and up one, F for moving right two and up one, G for moving left two and down
one, and H for moving right two and down one. For example, the two moves illustrated above in the Luddy section would be described with: HD.

## Solution 
#### Search Abstraction
##### 1. Set of States S:
The set of States S, can be defined as all possible configurations of the board. (16! for a 4 * 4 grid).

##### 2. Successor Function
Successor function returns the swapped map with all the possible moves from the current position of "0"

Important Callout: Here, validating all the successor to see if the goal state can be reached using permutation inversion.

Original: For (0,0), [(0,1) and (1,0)] are valid moves.
Circular: For (0,0), [(0,1),(1,0),(3,0),(0,3)] are valid moves. Circular always has a 4 moves.
Luddy: For (0,0), [(1,2) and (2,1)] are valid moves.

##### 3. Initial State:
Initial state is any given map from the available set of states.

##### 4. Goal State:
Canonical configuration of the board.
```
1 2 3 4
5 6 7 8
9 10 11 12
13 14 15 0
```

##### 5. Cost:
The program uses following algorithm with the following cost function:
1. A* search: f(n)=g(n)+h(n)
where g(n) is the cost to reach from start node to the current node n
and h(n) is the cost to reach from the current node n to the goal node.
2. BFS: f(n)=h(n)
 where h(n) is the heuristic search.

The heuristics that are used are:
Misplaced Tiles: Here, the cost is equal to the number of tiles that are not in their ideal positions on the board.( misplaced according to the canonical board configuration). It is admissible because the number of tiles that are misplaced are never over-estimated.

Manhattan Distance: It is the total vertical and horizontal displacements from current position to goal position. It is admissible because it never overestimates the linear path that a tile should take to reach it's ideal position.



#### Approach:

1. Given initial map is checked to see if it can reach goal state using permutation inversion.
2. Dividing the approach into two:
    * Optimized Solution implemented using A* Search. Here, the fringe is a priority queue, where cost is the priority and has map,route traversed so far and value of g(n) in a node. The algorithm also has visited structure (dictionary) to prevent the code from looping infinite times. And, successor function returns all the possible valid map configuration (refer Successor Function section). The algorithm computes the cost function of A* search which is g(n)+f(n) (refer Cost Section) and pops the node from the fringe directing to a optimized solution.
    * Unoptimized Solution implemented using Best First Search where cost is f(n).
3. Heuristic Function: Algorithm implements two heuristic function i.e. Manhattan Distance for Original and Circular type and Misplaced Tiles for Luddy type.

The optimized implementation runs for 4 minutes and breaks out of the loop. Further, the program gives the unoptimized moves as the result.

MOVES dictionary:
1) Original : MOVES= { "R": (0, -1), "L": (0, 1), "D": (-1, 0), "U": (1,0) }
2) Circular : MOVES= { "R": (0, -1), "L": (0, 1), "D": (-1, 0), "U": (1,0) } 
    * Here, to obtain the circular movement, the code uses modulus operation clubbed with the operation used for original.
3) Luddy : MOVES= {"A" : (-1,-2),"B":(-1,2),"C":(1,-2),"D":(1,2),"E":(-2,-1),"F":(-2,1),"G":(2,-1), "H":(2,1)}

## Part 2: Road trip!
Besides baseball, McDonald's, and reality TV, few things are as canonically American as hopping in the car for an old-fashioned road trip. We've prepared a dataset of major highway segments of the United States
(and parts of southern Canada and northern Mexico), including highway names, distances, and speed limits;
you can visualize this as a graph with nodes as towns and highway segments as edges. We've also prepared
a dataset of cities and towns with corresponding latitude-longitude positions.
between pairs of cities given by the user. Your program should be run on the command line like this:
```
./route.py [start-city] [end-city] [cost-function]
```
where:
* start-city and end-city are the cities we need a route between.
* cost-function is one of:
  * **segments** tries to find a route with the fewest number of "turns" (i.e. edges of the graph)
  * **distance** tries to find a route with the shortest total distance
  * **time** tries to find the fastest route, for a car that always travels at the speed limit
  * **mpg** tries to find the most economical route, for a car that always travels at the speed limit and
whose mileage per gallon (MPG) is a function of its velocity (in miles per hour), as follows:
MPG(v) = 400 v/150 (1 - v/150)4

The output of your program should be a nicely-formatted, human-readable list of directions, including travel times, distances, intermediate cities, and highway names, similar to what Google Maps or another site might produce. In addition, the last line of output should have the following machine-readable output about the route your code found:
```
[total-segments] [total-miles] [total-hours] [total-gas-gallons] [start-city] [city-1] [city-2] ... [end-city]
```

Please be careful to follow these interface requirements so that we can test your code properly. For instance, the last line of output might be:
```
3 51 1.0795 1.9552 Bloomington,_Indiana Martinsville,_Indiana Jct_I-465_&_IN_37_S,_Indiana Indianapolis,_Indiana
```
Like any real-world dataset, our road network has mistakes and inconsistencies; in the example above, for example, the third city visited is a highway intersection instead of the name of a town. Some of these "towns" will not have latitude-longitude coordinates in the cities dataset; you should design your code to still work well in the face of these problems.

## Solution 
#### Search Abstraction
##### 1. Set of States S
The set of states S, can be defined as all cities in the road-segments.txt that has interconnected neighbors, such that one can visit a city using one of its neighbors

##### 2. Successor Function
The successor function used in this problem returns every adjacent neighbor for a given city along with the following metrics for each neighbor
* distance
* speed limit
* Highway name
* Time to reach
* mpg achieved by travelling

##### 3. Initial State
The start city specified by the user

##### 4. Goal State:
To find the optimal route between a start and destination city, based on the optimization metric specifed by the user. If no solution is found, then to return `Inf`

##### 4. Cost:
The cost will depend on the metric chosen for optimization
* Segments - Number of edges in the path
* Distance - Total miles in the path
* Time - Total time taken to travel
* MPG - Total Miles per Gallon associated with the path

#### Approach
The implementation follows a greedy approach for most of the metrics, where it chooses the least expensive neighbor at every step. Although greedy algorithms are not always optimal, or even complete, the nature of this problem allows us to find solutions pretty quickly most of the times, since the algorithm mimics choices made in the real world.

Most often than not, we choose the least expensive path when driving between 2 cities

The implementation also uses a visited structure to record the cities that have been encountered in the path to avoid going in loops

For optimizing on segments, the implementation follows a breadth first search method.

#### Alternative approaches considered
Since we had the GPS coordinates available from the `city-gps.txt` we initially tried the A* algorithm with a straight line heuristic.
* Where the straight line distance between 2 cities was derived using the haversine function.
* This distance in turn formed the heuristic for the A* algorithm
* For cases where a city did not have a GPS coordinate, we used the next neighboring city that had a GPS co-ordinate. Since straight line distance just need to give a rough intuition (heuristic) as to in which direction a city lied, we felt this was appropriate

This implementation was abandoned since the other method provided satisfactory, if not better, results

##### Assumptions
* **Important callout**  - 'mpg' implementation as instructed by the pdf, says to `"Find the most economical route, for a car that always travels at the speed limit and
whose mileage per gallon (MPG) is a function of its velocity."`
  * We assume "most economical" means the cheapest (in terms of fuel), and hence the least amount of gallons consumed. Entity optimized here being gallons
  * We have not considered the maximum `mpg` for each city
* The difference between the two being, "More bang for your buck" v/s "Number of bucks" and we choose to have fewer "number of bucks" go towards fuel rather than "most bang for your buck."



## Part 3: Choosing a team
In the dystopian future, AI will have taken over most labor and leadership positions. As a student in B551,
you will assemble teams of robots to do the assignments for you. SICE will have a set of available robots for you to choose from. Each robot i will have an hourly rate Pi and a skill level Si. You'll want to choose a team of robots that has the greatest possible skill (i.e., the sum of the skill levels is as high as possible),
but you have a fixed budget of just B Intergalactic EuroYuanDollars (EYDs). The robot names, skills, and rates will be given in a le format like this:
```
David 34 100.5
Sam 25 30
Ed 12 50
Glenda 50 101
Nora 1 5
Edna 45 80
```
We've prepared an initial solution for you, but it has a big problem. It is guaranteed to assemble the best
possible team but only if you are allowed to hire fractions of robots:
```
[<>djcran@tank part3]$ ./choose_team.py people-small 200
Found a group with 4 people costing 200.000000 with total skill 69.029703
Nora 1.000000
Ed 1.000000
David 1.000000
Glenda 0.440594
```
As you can see, the program found a 4 person team that cost exactly the budget, but it hired only a portion
(about 0.44) of Glenda's time. Your job is to write a program that assembles as skilled a team as possible
but using only whole robots, and whose total cost is less than or equal to the budget. Please follow the same
output format as above.

## Solution 
#### Search Abstraction
##### 1. Set of States S
The set of states S can be defined as all possible combinations of robots (R1, R2,...,Rn) given, such that sum of cost of robots is less than the specified budget

##### 2. Successor Function
A robot Ri such that the cost (R1 + R2 + ... + Ri) <= budget

##### 3. Goal State:
Set of robots (R1, R2,...,Rn) such that cost(R1 + R2 + ... + Rn)<=budget and Max(Skill(R1 + R2 +  ... + Rn))

##### 4. Cost:
The cost at each stage is the amount of EuroYuanDollars paid for a robot.
Tha cost in this implementation also encompasses the consideration of the upper-bound which we try to maximize while minimizing the cost

#### Approach
This problem can be modeled using a 0/1 Knapsack with Least Cost Branch & Bound algorithm to search and subsequently prune a set of states generated at any given depth.

* The given list of [robots-skill-cost] file is sorted based on the ratio of cost/skill
* The algorithm computes an upper bound for every successor, this value helps it determine the feasibility/optimality of that successor
  * Any successor that does not improve the upper-bound is de-prioritized and one with the highest upper-bound is evaluated
* With every successor that is accepted as part of the solution, its corresponding weight is deducted from the budget
* Further successors are explored until the budget is not exhausted
  * When we reach the successor that exceeds the budget, we backtrack and consider the next successor (next node in the tree)
* This process continues until the number of robots is exhausted


#### Alternative approaches considered
 **1. Brute-force Approach**
 * A set of all possible combinations of robots were drawn and its associated metrics were populated
 * Manual pruning was done to a certain extent to exclude items that exceeded the budget
  * The implementation was abandoned due the sheer amount of states that the program would have to iterate through (n!)


 **2. Knapsack 0/1 Problem with Dynamic Programming**
 * The default 0/1 Knapsack algorithm did not make it easy for us to make use of the non-integer costs associated with each robot
 * This shifted our focus towards other approaches that allow us to have a fractional cost associated with each item in a knapsack


**References** - </br>
[1] - https://www.geeksforgeeks.org/implementation-of-0-1-knapsack-using-branch-and-bound/ </br>
[2] - https://rosettacode.org/wiki/Knapsack_problem/0-1#Python</br>
[3] - https://www.youtube.com/watch?v=yV1d-b_NeK8 </br>
[4] - https://www.kancloud.cn/leavor/cplusplus/630548 </br>
[5] - https://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/</br>
[6] - http://www.mathcs.emory.edu/~cheung/Courses/323/Syllabus/BranchBound/Docs/branch+bound01.pdf</br>
[7] - https://stackoverflow.com/questions/7448141/implementing-branch-and-bound-for-knapsack</br>
