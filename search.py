# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    Start: (5, 5)
    Is the start a goal? False
    Start's successors: [((5, 4), 'South', 1), ((4, 5), 'West', 1)]
    """
    "*** YOUR CODE HERE ***"
    root = problem.getStartState()
    stack = util.Stack()
    # Node Data Structure:
        # Parent: Contains the parent node.
        # Action: Contains the action the node can take i.e. 'South, West, North, South'
        # State: Contains a tuple (x, y) coordinate of where pacman is. 
    node = {}
    node["parent"] = None
    node["action"] = None
    node["state"] = root

    discovered = dict()

    stack.push(node)

    # While the stack is not empty we still have more nodes to visit.
    while not stack.isEmpty():
        node = stack.pop() # Pop the top state.
        state = node["state"] # Grab the state from the node.
        if discovered.has_key(hash(state)): # Storing the state 
            continue
        discovered[hash(state)] = True
        if problem.isGoalState(state) == True:
            break

        for child in problem.getSuccessors(state):
            state = hash(child[0])
            if not discovered.has_key(state):
                sub_node = {}
                sub_node["parent"] = node
                sub_node["action"] = child[1]
                sub_node["state"] = child[0]
                stack.push(sub_node)

        actions = []
        while node["action"] != None:
            actions.insert(0, node["action"])
            node = node["parent"]
        return actions 

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    root = problem.getStartState()
    queue = util.Queue() 
    
    # Node Data Structure:
        # Parent: Contains the parent node.
        # Action: Contains the action the node can take i.e. 'South, West, North, South'
        # State: Contains a tuple (x, y) coordinate of where pacman is. 
    node = {}
    node["parent"] = None
    node["action"] = None 
    node["state"] = root

    discovered = dict() # holds a easily searchable data structure to store visited nodes. 

    queue.push(node)

    while not queue.isEmpty():
        node = queue.pop()
        state = node["state"] # (x, y)
        if discovered.has_key(hash(state)):
            continue
        discovered[hash(state)] = True
        # found the end 
        if problem.isGoalState(state) == True:
            break

        for child in problem.getSuccessors(state):
            state = hash(child[0])
            if not discovered.has_key(state):
                child_node = {}
                child_node["parent"] = node # (parent, action, cost)
                child_node["action"] = child[1]
                child_node["state"] = child[0]
                queue.push(child_node)
    actions = []
    while node["action"] != None: # return the path up the tree recursively following the parent. 
        actions.insert(0, node["action"])
        node = node["parent"]
    return actions 

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    root = problem.getStartState()

    discovered = dict()
    pq = util.PriorityQueue()

    node = {} 
    node["parent"] = None
    node["action"] = None
    node["totalCost"] = 0
    node["state"] = root

    pq.push(node, node["totalCost"])

    while not pq.isEmpty():
        node = pq.pop()
        state = node["state"]
        if discovered.has_key(hash(state)):
            continue
        discovered[hash(state)] = True
        if problem.isGoalState(state) == True:
            break
        for child in problem.getSuccessors(state):
            state = child[0]
            if not discovered.has_key(hash(state)):
                child_node = {}
                child_node["parent"] = node
                child_node["action"] = child[1]
                child_node["state"] = child[0]
                child_node["totalCost"] = node["totalCost"] + child[2]
                pq.push(child_node, child_node["totalCost"])
    actions = []
    while node["action"] != None:
        actions.insert(0, node["action"])
        node = node["parent"]
    return actions




def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    PQ = util.PriorityQueue()
    discovered = dict()
    node = {}
    node["parent"] = None
    node["action"] = None
    node["state"] = problem.getStartState()
    node["gn"] = 0
    node["hn"] = heuristic(node["state"], problem)
    node["fn"] = node["gn"] + node["hn"]
    PQ.push(node, node["fn"])
    while not PQ.isEmpty():
        path = PQ.pop()
        if discovered.has_key(path["state"]):
            continue
        discovered[path["state"]] = True
        if problem.isGoalState(path["state"]) == True:
            break
        for successor in problem.getSuccessors(path["state"]):
            if not discovered.has_key(successor[0]):
                new_path = {}
                new_path["parent"] = path
                new_path["state"] = successor[0]
                new_path["action"] = successor[1]
                new_path["gn"] = successor[2] + path["gn"]
                new_path["hn"] = heuristic(new_path["state"], problem)
                new_path["fn"] = new_path["gn"] + new_path["hn"]
                PQ.push(new_path, new_path["fn"]) 
    actions = []
    while path["action"] != None:
        actions.insert(0, path["action"])
        path = path["parent"]
    return actions

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
