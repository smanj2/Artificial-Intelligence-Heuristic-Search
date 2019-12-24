#!/usr/local/bin/python3
# choose_team.py : Choosing a Team
#
# Code by: [Sri Harsha Manjunath - srmanj; Vijaylakshmi Maigur - vbmaigur; Disha Talreja - dtalreja]
#
#
#

import sys

def load_people(filename):
    people={}
    with open(filename, "r") as file:
        for line in file:
            l = line.split()
            temp = (l[1:])
            people[l[0]] = [ float(temp[0]),float(temp[1]),float(temp[1])/float(temp[0])]
    return people

### --- The class definition for defining the following fringe structure has been taken from the following links --- ###
### --- http://www.mathcs.emory.edu/~cheung/Courses/323/Syllabus/BranchBound/Docs/branch+bound01.pdf --- ###
### --- https://stackoverflow.com/questions/7448141/implementing-branch-and-bound-for-knapsack --- ###
### --- Beginning of code from the above link --- ###
class fringe(object):
    def __init__(self, depth, skill, cost, state):
        self.depth = depth
        self.skill = skill
        self.cost = cost
        self.state = state
        #When initializing a node at a certain depth d, make every node after that as 1
        #Indicating it needs to be evaluated
        self.pointer = self.state[:self.depth]+[1]*(len(robot_skill)-depth)
        #Compute the upper bound for the given fringe state
        self.ub = self.compute_cost()
### --- End of code from the above link --- ###

    def compute_cost(self):
        ub = 0
        total_cost = 0
        for i in range(len(robot_cost)):
            if robot_cost[i] * self.pointer[i] <= budget - total_cost:
                if self.pointer[i] != 0:
                    total_cost += robot_cost[i]
                    ub += robot_skill[i]
            else:
                if self.pointer[i] != 0:
                    ub += (budget - total_cost) * ratio[i]
                    #After computing the cost; Do not further consider remaining robots
                break
        return ub

    def successor(self):
        #This function generates (Include) or (Exclude) child nodes and returns them
        depth = self.depth + 1
        #Child 0 will the return inputs as a fringe object, since nothing has changed
        child0 = fringe(depth, self.skill, self.cost, self.state)
        include = False
        if self.cost + robot_cost[self.depth] <= budget: #iIf within budget, compute include(1) child
            #Modify states accordingly
            state1 = self.state[:self.depth]+[1]+self.state[self.depth+1:]
            cost1 = self.cost + robot_cost[self.depth]
            skill1 = self.skill + robot_skill[self.depth]
            child1 = fringe(depth, skill1, cost1, state1)
            include = True #Set Flag = True denoting there exists a child with 1
        if include == True:
            return [child1,child0]
        else:
            return [child0]

if __name__ == "__main__":
    if(len(sys.argv) != 3):
        raise Exception('Error: expected 2 command line arguments')

    #Define Constants
    budget = float(sys.argv[2])
    robot_name = []
    robot_cost = []
    robot_skill = []
    ratio = []

    #Data Preprocessing -
    people = load_people(sys.argv[1])

    # Create a list of tuples sorted by index the ratio of cost and skill
    tuples = sorted(people.items() ,  key=lambda x: x[1][2])

    # Iterate over the sorted sequence
    for elem in tuples :
        robot_name.append(elem[0])
        robot_cost.append(elem[1][1])
        robot_skill.append(elem[1][0])
        ratio.append(elem[1][2])

    explorer = fringe(0, 0, 0, [0]*len(robot_skill)) #start with nothing
    visited = [] #list of States waiting to be explored

    while explorer.depth < len(robot_skill):
        visited.extend(explorer.successor())
        visited.sort(key=lambda x: x.ub) #sort the waiting list based on their upperbound
        explorer = visited.pop() #explore the one with largest upperbound
        final = explorer

    best_robots = []
    for i in range(len(final.state)):
        if (final.state[i] == 1):
            best_robots.append(robot_name[i])

    if final.cost == 0:
        print ("Inf")
    else:
        print ("Found a group with 4 people costing ",final.cost," with total skill ",final.skill)
        for i in best_robots:
            print(i," 1.0")