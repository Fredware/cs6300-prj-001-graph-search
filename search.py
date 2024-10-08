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

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))

    # Initialize the explored set to be empty
    explored_set = set()
    # Initialize the frontier as a Stack
    frontier = util.Stack()
    # Add initial state to frontier
    start_node = {"state": problem.getStartState(), "parent": None, "action": None}
    frontier.push(start_node)
    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoalState(node["state"]):
            action_list = []
            while node["parent"] is not None:
                action_list.append(node["action"])
                node = node["parent"]
            action_list.reverse()
            return action_list
        explored_set.add(node["state"])
        successors = problem.getSuccessors(node["state"])
        for child in successors:
            child_node = {"state": child[0], "parent": node, "action": child[1]}
            if child_node["state"] not in explored_set:
                frontier.push(child_node)
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # Initialize the explored set to be empty
    explored_set = set()
    frontier_set = set()
    # Initialize the frontier as a Stack
    frontier = util.Queue()
    # Add initial state to frontier
    start_node = {"state": problem.getStartState(), "parent": None, "action": None}
    frontier.push(start_node)
    frontier_set.add(start_node["state"])
    while not frontier.isEmpty():
        node = frontier.pop()
        frontier_set.remove(node["state"])
        if problem.isGoalState(node["state"]):
            action_list = []
            while node["parent"] is not None:
                action_list.append(node["action"])
                node = node["parent"]
            action_list.reverse()
            return action_list
        explored_set.add(node["state"])
        successors = problem.getSuccessors(node["state"])
        for child in successors:
            child_node = {"state": child[0], "parent": node, "action": child[1]}
            if not (child_node["state"] in explored_set or child_node["state"] in frontier_set):
                frontier.push(child_node)
                frontier_set.add(child_node["state"])
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # Initialize the explored set to be empty
    explored_set = set()
    frontier_set = set()
    # Initialize the frontier as a Stack
    frontier = util.PriorityQueue()
    # Add initial state to frontier
    start_node = {"state": problem.getStartState(), "parent": None, "action": None, "cost": 0}
    frontier.push(start_node, start_node["cost"])
    frontier_set.add(start_node["state"])
    while not frontier.isEmpty():
        node = frontier.pop()
        frontier_set.remove(node["state"])
        if problem.isGoalState(node["state"]):
            action_list = []
            while node["parent"] is not None:
                action_list.append(node["action"])
                node = node["parent"]
            action_list.reverse()
            return action_list
        explored_set.add(node["state"])
        successors = problem.getSuccessors(node["state"])
        for child in successors:
            child_node = {"state": child[0], "parent": node, "action": child[1], "cost": child[2] + node["cost"]}
            if not (child_node["state"] in explored_set or child_node["state"] in frontier_set):
                frontier.push(child_node, child_node["cost"])
                frontier_set.add(child_node["state"])
            elif child_node["state"] in frontier_set:
                frontier_temp = util.PriorityQueue()
                while not frontier.isEmpty():
                    search_node = frontier.pop()
                    if search_node["state"] == child_node["state"]:
                        if search_node["cost"] > child_node["cost"]:
                            search_node = child_node
                    frontier_temp.push(search_node, search_node["cost"])
                frontier = frontier_temp
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # Initialize the explored set to be empty
    explored_set = set()
    frontier_set = set()
    # Initialize the frontier as a Stack
    frontier = util.PriorityQueue()
    # Add initial state to frontier
    start_node = {"state": problem.getStartState(), "parent": None, "action": None, "cost": 0, "heur": heuristic(problem.getStartState(), problem)}
    frontier.push(start_node, start_node["cost"])
    frontier_set.add(start_node["state"])
    while not frontier.isEmpty():
        node = frontier.pop()
        frontier_set.remove(node["state"])
        if problem.isGoalState(node["state"]):
            action_list = []
            while node["parent"] is not None:
                action_list.append(node["action"])
                node = node["parent"]
            action_list.reverse()
            return action_list
        explored_set.add(node["state"])
        successors = problem.getSuccessors(node["state"])
        for child in successors:
            child_node = {"state": child[0], "parent": node, "action": child[1], "cost": child[2] + node["cost"], "heur": heuristic(child[0], problem)}
            if not (child_node["state"] in explored_set or child_node["state"] in frontier_set):
                frontier.push(child_node, child_node["cost"] + child_node["heur"])
                frontier_set.add(child_node["state"])
            elif child_node["state"] in frontier_set:
                frontier_temp = util.PriorityQueue()
                while not frontier.isEmpty():
                    search_node = frontier.pop()
                    if search_node["state"] == child_node["state"]:
                        if (search_node["cost"] + search_node["heur"]) > (child_node["cost"] + child_node["heur"]):
                            search_node = child_node
                    frontier_temp.push(search_node, search_node["cost"] + search_node["heur"])
                frontier = frontier_temp
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
