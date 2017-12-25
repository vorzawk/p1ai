''' A* search '''
from stateSpaceGraph import node
from heapq import heappush, heappop

def greedyBestFirstSearch(initNode):
    heapNodes = []
    setExplored = set()
    currNode = initNode
    heuristicCurrNode = currNode.heuristicValue()
#   Search the statespace for a node with heuristic value of 0 a.k.a the goal node
    numGoalTests = 0
    maxQueueSize = 0
    while heuristicCurrNode != 0:
        numGoalTests = numGoalTests + 1
        listChildNodes = currNode.computeChildren()
        for node in listChildNodes:
            heuristicNode = node.heuristicValue()
            heappush(heapNodes, (heuristicNode, node))
            queueSize = len(heapNodes)
            if queueSize > maxQueueSize:
                maxQueueSize = queueSize
        setExplored.add(currNode)
# Find the node with the least heuristic value i.e the node which is closest to the goal node. A loop is required since
# the priority queue does not provide a change_priority method (too expensive). So, instead of doing an O(n) search to
# find the priority value for the node, simply add the node to the heap. The better value for the node will have
# higher priority and is guarranteed to be explored earlier if it exists. A check is required to see if the node popped
# out of the heap is already explored, so that it is not processed again.
        while currNode in setExplored:
            if len(heapNodes) == 0:
                return None
            tupleCurrNode = heappop(heapNodes)
            currNode = tupleCurrNode[1]
            heuristicCurrNode = tupleCurrNode[0]
    print("Number of goal tests : {}".format(numGoalTests))
    print("Maximum queue size : {}".format(maxQueueSize))
    return currNode

def aStarSearch(initNode):
    heapNodes = []
    setExplored = set()
    currNode = initNode
    heuristicCurrNode = currNode.heuristicValue()
#   Search the statespace for a node with heuristic value of 0 a.k.a the goal node
    numGoalTests = 0
    maxQueueSize = 0
    while heuristicCurrNode != 0:
        numGoalTests = numGoalTests + 1
        listChildNodes = currNode.computeChildren()
        for node in listChildNodes:
            heuristicNode = node.heuristicValue()
            heappush(heapNodes, (heuristicNode + node.pathcost, node))
            queueSize = len(heapNodes)
            if queueSize > maxQueueSize:
                maxQueueSize = queueSize
        setExplored.add(currNode)
# Find the node with the least heuristic value i.e the node which is closest to the goal node. A loop is required since
# the priority queue does not provide a change_priority method (too expensive). So, instead of doing an O(n) search to
# find the priority value for the node, simply add the node to the heap. The better value for the node will have
# higher priority and is guarranteed to be explored earlier if it exists. A check is required to see if the node popped
# out of the heap is already explored, so that it is not processed again.
        while currNode in setExplored:
            if len(heapNodes) == 0:
                return None
            tupleCurrNode = heappop(heapNodes)
            currNode = tupleCurrNode[1]
            heuristicCurrNode = tupleCurrNode[0] - currNode.pathcost
    print("Number of goal tests : {}".format(numGoalTests))
    print("Maximum queue size : {}".format(maxQueueSize))
    return currNode

def backTrace(currNode):
    if currNode.parent:
        backTrace(currNode.parent)
    for stack in currNode.state:
        print("|", end = ' ')
        for block in stack:
            print(block, end = ' ')
        print()
    print()
