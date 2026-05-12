#!/usr/bin/env python
# coding: utf-8

# In[15]:


import heapq
import random
import time

#Configuration and Goal State
#Represented as flat tuple: (1,2,3,8,0,4,7,6,5)
goalState = (1, 2, 3, 8, 0, 4, 7, 6, 5)

#Directions for moving the blank space: Up, Down, Left, Right
moves = {
    'Up': -3,
    'Down': 3,
    'Left': -1,
    'Right': 1
}

class Node:
    #Represents a state in the search tree
    def __init__(self, state, parent=None, action=None, g=0):
        self.state = state     #board configuration (tuple)
        self.parent = parent   #parent node
        self.action = action   #move that got us where we are
        self.g = g             #Cost to reach this node (from the start)
        self.h = self.calculateManhattan() #Estimated cost to goal
        self.f = self.g + self.h #Total cost f(n) = g(n) + h(n)

    def calculateManhattan(self):
        #Calculates the Manhattan Distance of each tile from its proper position
        distance = 0
        for idx, val in enumerate(self.state):
            if val != 0: #Don't calculate distance for the blank space
                #Find current 2D coordinates (row, col) from the 1D index
                currRow, currCol = divmod(idx, 3)
                #Find target 2D coordinates (row, col) in the goal state
                targetRow, targetCol = divmod(goalState.index(val), 3)

                distance += abs(currRow - targetRow) + abs(currCol - targetCol)
        return distance

    def __lt__(self, other):
        #Allows the priority queue to sort nodes based on the lowest f(n) value.
        return self.f < other.f

    def getBlankIndex(self):
        return self.state.index(0)

    def getChildren(self):
        #Generates all valid children states from the current state.
        children = []
        blankIDX = self.getBlankIndex()
        #Calculate row and column of the blank space
        row, col = divmod(blankIDX, 3)

        for moveName, moveDelta in moves.items():
            # Boundary checking
            if moveName == 'Up' and row == 0: continue
            if moveName == 'Down' and row == 2: continue
            if moveName == 'Left' and col == 0: continue
            if moveName == 'Right' and col == 2: continue

            #Create a new state by swapping the blank state with the target tile
            targetIDX = blankIDX + moveDelta
            newStateList = list(self.state)
            #Swapping
            newStateList[blankIDX], newStateList[targetIDX] = newStateList[targetIDX], newStateList[blankIDX]
            newState = tuple(newStateList)

            #Create a new node. g(n) increases by 1 for each step
            children.append(Node(newState, self, moveName, self.g + 1))
        return children

    def getPath(self):
        #Backtracks from this node to the root to reconstruct the path.
        path = []
        current = self
        while current:
            path.append(current)
            current = current.parent
        return path[::-1] # Returning reversed (Start -> Goal)

#Helper Functions

def printBoard(state):
    #prints the 3x3 board
    for i in range(0,9,3):
        print(f"{state[i]} | {state[i+1]} | {state[i+2]}")
    print("-" * 9)

def getRandomStart(steps=25):
    #Generates a random solvable state by starting at the goal and shuffling backwards.
    currentState = goalState
    for _ in range(steps):
        tempNode = Node(currentState)
        children = tempNode.getChildren()
        randomChild = random.choice(children)
        currentState = randomChild.state
    return currentState

#The Algorithm

def aStarSearch(initialState):
    # Executes the A* search algorithm
    print("\n--- Starting A* Search ---")
    startTime = time.time()
    startNode = Node(initialState)

    openList = []
    heapq.heappush(openList, startNode)
    visited = set() #Keeps track of visited states to prevent infinite loops

    nodesExpanded = 0

    while openList:
        currentNode = heapq.heappop(openList) #Get node with lowest f(n)

        #Skip if we've already evaluated this exact state
        if currentNode.state in visited:
            continue

        visited.add(currentNode.state)
        nodesExpanded += 1

        #Check if we reached the goal
        if currentNode.state == goalState:
            print(f"A* Found Goal! Nodes expanded: {nodesExpanded}")
            print(f"Time taken: {time.time() - startTime:.4f} seconds")
            return currentNode

        #Generate and add successors to the open list
        for child in currentNode.getChildren():
            if child.state not in visited:
                heapq.heappush(openList, child)

    return None #returns None if no solution is found

#Main

if __name__ == "__main__":
    print("Generating a random initial state...")
    initialState = getRandomStart(steps=25)

    print("Initial State:")
    printBoard(initialState)
    print("\nGoal State:")
    printBoard(goalState)

    solutionNode = aStarSearch(initialState)

    if solutionNode:
        path = solutionNode.getPath()
        print(f"\nGoal found in {len(path) - 1} moves!\n")
        print("--- Intermediate States ---")
        for step, node in enumerate(path):
            if node.action:
                print(f"Step {step}: Move blank {node.action}")
            else:
                print("Start:")
            printBoard(node.state)
    else:
        print("No solution found.")

