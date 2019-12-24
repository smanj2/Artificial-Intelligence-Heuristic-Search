#!/usr/local/bin/python3
# solve_luddy.py : Sliding tile puzzle solver
#
# Code by: [PLEASE PUT YOUR NAMES AND USER IDS HERE]
#
# Based on skeleton code by D. Crandall, September 2019
#
from queue import PriorityQueue
import sys
import numpy as np
import time

# Computes index value in a list given row and col
def rowcol2ind(row, col):
    return row*4 + col

# Computes row,col given index in a list
def ind2rowcol(ind):
    return (int(ind/4), ind % 4)

def valid_index(row, col):
    return 0 <= row <= 3 and 0 <= col <= 3
	
def swap_ind(list, ind1, ind2):
    return list[0:ind1] + (list[ind2],) + list[ind1+1:ind2] + (list[ind1],) + list[ind2+1:]

def swap_tiles(state, row1, col1, row2, col2):
    return swap_ind(state, *(sorted((rowcol2ind(row1,col1), rowcol2ind(row2,col2)))))

def printable_board(row):
    return [ '%3d %3d %3d %3d'  % (row[j:(j+4)]) for j in range(0, 16, 4) ]

# checks if we've reached the goal
def is_goal(state):
    return sorted(state[:-1]) == list(state[:-1]) and state[-1]==0

# checks if solution exists for any given state by computing permutation inversion
# return True if solution exists and false if it doesnt.

def solnexist(m):
    lenofmap=int(np.sqrt(len(m)))
    pi=[]
    for (ind,val) in enumerate(m):
        (r,c)=ind2rowcol(ind)
        possible_pi_pos=m[ind+1:]
        if val==0:
            pi.append(r+1)
        else:
            pi.append(len([m for m in possible_pi_pos if m<val and m!=0]))
    return sum(pi)%2==0

# Implements approach using A* search and runs for 4 minutes

def solve_optimised(initial_board,type_sol):
    fringe = PriorityQueue()
    fringe.put((0,initial_board,"",0)) #Cost, State, Route, g(x)
    visited={}
    a=time.time()
    b=0
    while not fringe.empty():
        #Pop the smallest cost entry in the fringe
        cost,state, route_so_far,g = fringe.get()
        # Append visited dictionary
        visited[state]="yes"
        for (succ, move) in successors(tuple(state),type_sol):
            if succ not in visited:
                #Check 1: If Successor is the goal
                if is_goal(succ):
                    return (route_so_far + move )    
                #Compute Heuristic + cost_to_root
                h = heuristic(succ,type_sol)
                g = g+1
                #Check 2: If time has exceeds 4 min
                if b-a<240:
                    fringe.put((h+g, succ ,route_so_far + move ,g))
                else:
                    return solve_unoptimised(initial_board,type_sol)
                    break
        if fringe.qsize()==0:
            return None
        b=time.time()

# unoptimized solution uses Best First Search
def solve_unoptimised(initial_board,type_sol):
    fringe = PriorityQueue()
    fringe.put((0,initial_board,"",0)) #Cost, State, Route, g(x)
    visited={}
    while not fringe.empty():
        #Pop the smallest cost entry in the fringe
        cost,state, route_so_far,g = fringe.get()
        visited[state]="yes"
        for (succ, move) in successors(tuple(state),type_sol):
            #print(succ)
            if succ not in visited:
                #Check 1: If Successor is the goal
                if is_goal(succ):
                    return (route_so_far + move )    
                #Compute Heuristic + cost_to_root
                h = heuristic(succ,type_sol)
                g = g+1
                fringe.put((h, succ ,route_so_far + move ,g))
        if fringe.qsize()==0:
            return None
		
def heuristic(board,type_sol):
    #Function to return h(x)
    ideal_list= [i for i in range(1,len(board))]#; ideal_list.pop(0); ideal_list.append(0) #Defining the solved list
    ideal_list.append(0)
    if type_sol in ("original","circular"):
        heur = 0
        for i in range(0,len(board)):
            if board.index(i) == ideal_list[i]:
                pass
            else:
                x1,y1 = ind2rowcol(ideal_list[i]) #Returns where the current misplaced tile is
                x2,y2= ind2rowcol(board[i]) #Returns where it is suppose to be
                heur = heur + (abs(x1-x2) + abs(y1-y2))
    else:
        # calculates the number of misplaced tiles.
        heur=0
        for i in range(len(board)):
            if board[i]!=ideal_list[i]:
                heur+=1
        
    return heur

def successors(state,type_sol):
    (empty_row, empty_col) = ind2rowcol(state.index(0))
    maplen=np.sqrt(len(state))
    succ=[]
    for (c,(i,j)) in MOVES.items():
        if valid_index((empty_row+i), (empty_col+j)) and (type_sol in ("original", "luddy")):
            map_swap=(swap_tiles(state, empty_row, empty_col, (empty_row+i), (empty_col+j)))
            if solnexist(map_swap): # checks if solution exists for the curr state
                succ.append((map_swap, c))
        # for circular the index values are calculated by finding the modulus of the above implementation
        elif valid_index(int((empty_row+i)%maplen), int((empty_col+j)%maplen)) and (type_sol in ("circular")):
            map_swap=(swap_tiles(state, empty_row, empty_col, int((empty_row+i)%maplen), int((empty_col+j)%maplen)))
            if solnexist(map_swap): # checks if solution exists for the curr state
                succ.append((map_swap,c))
        else:
            pass
    return succ

# test cases
if __name__ == "__main__":
    global MOVES
    if(len(sys.argv) != 3):
        raise(Exception("Error: expected 2 arguments"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != 16:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    if(sys.argv[2] == "original" or sys.argv[2] == "circular"):
        MOVES= { "R": (0, -1), "L": (0, 1), "D": (-1, 0), "U": (1,0) }
    else:
        MOVES= {"A" : (-1,-2),"B":(-1,2),"C":(1,-2),"D":(1,2),"E":(-2,-1),"F":(-2,1),"G":(2,-1), "H":(2,1)}
    #checks if solution exists or not.
    if solnexist(start_state):
        route = solve_optimised(tuple(start_state),sys.argv[2])
        if route==None:
            print("Inf")
        else:
            print("Solution found in " + str(len(route)) + " moves:" + "\n" + route)
    else:	
        print("Inf")
