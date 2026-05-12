#!/usr/bin/env python
# coding: utf-8

# In[4]:


import collections
import random
import time

# Configuration and Goal State
# The problem wants clockwise in ascending order
#Clockwise Goal
#1 2 3
#8 0 4
#7 6 5
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
    # Represents a state in the search tree
    def __init__(self, state, parent=None, action=None, depth=0):
        self.state = state #board configuration (tuple)
        self.parent = parent #parent node
        self.action = action #move that got us where we are, like Up or Down
        self.depth = depth #Depth in tree
    def getBlankIndex(self):
        return self.state.index(0)

    def getChildren(self):
        #Generates all valid children states from the current state.
        children = []
        blankIDX = self.getBlankIndex()
        #Calculate row and column of the blank space
        row, col = divmod(blankIDX, 3)
        for moveName, moveDelta in moves.items():
            #Boundary checking
            if moveName == 'Up' and row == 0: continue
            if moveName == 'Down' and row == 2: continue
            if moveName == 'Left' and col == 0: continue
            if moveName == 'Right' and col == 2: continue
            #Create a new state by swapping the blank state with the target state
            targetIDX = blankIDX + moveDelta
            newStateList = list(self.state)
            #Swapping
            newStateList[blankIDX], newStateList[targetIDX] = \
                    newStateList[targetIDX], newStateList[blankIDX]
            newState = tuple(newStateList)
            #Create a new node
            children.append(Node(newState, self, moveName, self.depth+1))
        return children

    def getPath(self):
        #Backtracks from this node to the root to reconstruct the path.
        path = []
        current = self
        while current:
            path.append(current)
            current = current.parent
        return path[::-1] #Returning reversed (Start -> Goal)

#Helper Functions

def printBoard(state):
    #prints the 3x3 board
    for i in range(0,9,3):
        print(f"{state[i]} | {state[i+1]} | {state[i+2]}")
    print("-" * 9)

def getRandomStart(steps=15):
    #Generates a random solvable state by starting at the goal and shuffling backwards 'steps' times. This will ensure the puzzle is solvable
    currentState = goalState
    #A simple loop to make random moves
    for _ in range(steps):
        #Temporarily create a node just to use getChildren logic
        tempNode = Node(currentState)
        children = tempNode.getChildren()
        randomChild = random.choice(children)
        currentState = randomChild.state
    return currentState

# The Algorithms

def BFS(initialState):
    #Breadth First Search (BFS)
    #Uses a Queue (FIFO). Will guarantee the shortest path.
    print("\n--- Starting BFS ---")
    startTime = time.time()
    startNode = Node(initialState)
    if startNode.state == goalState:
        return startNode
    queue = collections.deque([startNode])
    visited = set()
    visited.add(initialState)
    nodesExpanded = 0
    while queue:
        currentNode = queue.popleft()
        nodesExpanded +=1
        if currentNode.state == goalState:
            print(f"BFS Found Goal! Nodes expanded: {nodesExpanded}")
            print(f"Time taken: {time.time() - startTime:.4f} seconds")
            return currentNode
        for child in currentNode.getChildren():
            if child.state not in visited:
                visited.add(child.state)
                queue.append(child)
    return None

def IDFS(initialState, maxDepth=50):
    #Iterative-Deepening Depth-First Search (IDFS)
    #Repeatedly calls DLS (Depth Limited Search) with increasing depth limits.
    print("\n--- Starting IDFS ---")
    startTime = time.time()
    #Loop to increase depth limit
    for limit in range(maxDepth):
        #Pass a new visited set for each depth,
        #or check the current path for cycles as per DFS rules.
        #Do not re-add any of the parents which are already in the tree branch.
        result = DLS(Node(initialState),limit)
        if result:
            print(f"IDFS Found Goal at depth limit: {limit}")
            print(f"Time taken: {time.time() - startTime:.4f} seconds")
            return result
    print("IDFS reached max depth without finding solution.")
    return None

def DLS(node, limit):
    #Depth-Limited Search (Recursive DFS)

    #Check if goal
    if node.state == goalState:
        return node
    #check depth limit
    if node.depth >= limit:
        return None

    for child in node.getChildren():
        #Cycle prevention:
        #"Make sure that you do not re-add any of the parents which are already in the tree branch."
        if not isInBranch(node,child.state):
            result = DLS(child,limit)
            if result:
                return result
    return None

def isInBranch(currentNode,stateToCheck):
    #Checks if stateToCheck exists within the current path (ancestors).
    curr = currentNode
    while curr:
        if curr.state == stateToCheck:
            return True
        curr = curr.parent
    return False

#Main

if __name__ == "__main__":
    #1. Generate random start
    #Using a small shuffle number for IDFS to finish quickly in demo.
    randomStartState = getRandomStart(steps=15)

    print("Initial State:")
    printBoard(randomStartState)
    print("\nGoal State:")
    printBoard(goalState)

    #2. Run BFS
    bfsSolution = BFS(randomStartState)
    if bfsSolution:
        path = bfsSolution.getPath()
        print(f"\nBFS Solution Path Length: {len(path) -1} moves")
        print("Moves to solve:")
        for node in path:
            if node.action:
                print(f"Move {node.action} ->")
            printBoard(node.state)
    else:
        print("BFS failed to find a solution.")

    #3. Run IDFS
    idfsSolution = IDFS(randomStartState, maxDepth=50)
    if idfsSolution:
        path = idfsSolution.getPath()
        print(f"\nIDFS Solution Path Length: {len(path) -1} moves")
        #Print path for IDFS
        for node in path:
            if node.action:
                print(f"Move {node.action} ->")
            printBoard(node.state)
    else:
        print("IDFS failed to find a solution")

