#!/usr/bin/env python3

import sys
import string
from random import choice as randChoice, randint
from searchAlgo import node, aStarSearch, greedyBestFirstSearch, backTrace

if len(sys.argv) != 3:
    print("{}: Missing required arguments".format(sys.argv[0]))
    print("Usage: {} numBlocks numStacks".format(sys.argv[0]))
    print("Eg: {} 5 3 for initial state with 5 blocks and 3 stacks".format(sys.argv[0]))
    sys.exit()

numBlocks = int(sys.argv[1])
numStacks = int(sys.argv[2])
goalState = list(string.ascii_lowercase[0:numBlocks])
initState = [[] for _ in range(numStacks)]
# For sequences(lists, tuples, strings), empty sequences are False
while goalState:
    stackNo = randint(0,numStacks-1)
    block = randChoice(goalState)
    initState[stackNo].append(block)
    goalState.remove(block)

initNode = node(initState, 0, None)
goal = aStarSearch(initNode)
print("Solution Path:")
backTrace(goal)
print("Total steps taken : {}".format(goal.pathcost))


