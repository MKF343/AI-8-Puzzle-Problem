# 8-Puzzle Solver: AI Search Optimization

## Overview
This repository contains a modular Python-based solver for the classic 8-puzzle sliding tile problem. The project was developed to explore and compare the efficiency, memory utilization, and computational overhead of different Artificial Intelligence search algorithms. 

By implementing both uninformed and informed search strategies, this project demonstrates state-space exploration, heuristic design, and algorithmic optimization. The algorithms attempt to reach the target clockwise goal state:

```text
1 | 2 | 3
8 | 0 | 4
7 | 6 | 5
```

## Algorithms Implemented

The solver tackles the puzzle using three distinct search strategies:

* **Breadth-First Search (BFS):** An uninformed search method utilizing a FIFO queue. While it guarantees the shortest possible path to the goal, it demonstrates the high memory complexity associated with exploring all possible states level by level.
* **Iterative-Deepening Depth-First Search (IDFS):** An uninformed search that repeatedly applies Depth-Limited Search (DLS) with an increasing depth limit. This strategy balances the path-optimality of BFS with the strict memory efficiency of DFS, featuring built-in cycle prevention.
* **A-Star Search:** An informed, best-first search algorithm utilizing a custom **Manhattan Distance** heuristic. By calculating the total estimated cost utilizing the formula f(n) = g(n) + h(n), the algorithm intelligently prioritizes which nodes to expand. This results in a drastic reduction in computational overhead and nodes explored compared to the uninformed methods.

## Repository Structure

* `Kirtland.py`: Contains the implementation for the uninformed search algorithms (**BFS** and **IDFS**). Includes a random state generator that walks backward from the goal state to ensure the generated puzzles are always solvable.
* `Kirtland1.py`: Contains the implementation for the informed **A* Search** algorithm. Utilizes Python's `heapq` library to maintain a highly efficient priority queue based on the calculated costs.

## Technical Highlights

* **Object-Oriented Design:** Utilizes a custom `Node` class to encapsulate board states, track parent nodes for path reconstruction, record move actions, and calculate heuristic costs.
* **Algorithmic Efficiency:** Showcases the stark contrast in performance and node expansion between blind exploration and heuristic-driven logic.
* **Data Structures:** Leverages `collections.deque` for optimal O(1) queue operations in BFS, sets for O(1) visited-state lookups, and `heapq` for priority queue management in A*.

## How to Run

Ensure you have Python 3.x installed. No external libraries are required.

To run the Uninformed Search (BFS & IDFS) solver:
```bash
python Kirtland.py
```

To run the Informed Search (A*) solver:
```bash
python Kirtland1.py
```

Upon execution, the scripts will generate a random, solvable starting board, execute the respective algorithms, and output the step-by-step path required to reach the goal state, along with the total nodes expanded and execution time.

---
**Author:** Michael Kirtland  
**Academic Focus:** Computer Science | Data Structures & Algorithms | Database Architecture
