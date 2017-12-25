''' This module defines the node class and the heuristic functions. The node class has a member heuristicValue of the type function. The required heuristic function can be selected by assigning it to this variable. Its default value is h5 which is the final version which gives the best performance '''
import copy
import string

class node:
    def __init__(self, state, pathcost, parentNode):
        self.state = state
        self.pathcost = pathcost
        self.parent = parentNode
        self.heuristicValue = self.h5

    def __lt__(self, otherNode):
        return self.state[0] < otherNode.state[0]

    def __eq__(self, otherNode):
        return self.state[0] == otherNode.state[0]

    def __hash__(self):
        # A tuple of tuple is hashable, this is necessary so that the node can be added to the hashset of explored nodes in
        # the A* search algorithm
        tuple_of_tuples = tuple(tuple(stack) for stack in self.state)
        return hash(tuple_of_tuples)

    def computeChildren(self) :
        listChildren = []
        for stack in self.state:
            if len(stack) > 0:
                for otherStack in self.state:
                    if otherStack != stack:
                        otherStack.append(stack.pop())
#                       Deep copy is required here otherwise the new node generated will still refer to the parent, the
#                       idea is to modify the parent, store the node and revert the change to get back the parent node
                        childNode = node(copy.deepcopy(self.state), self.pathcost + 1, self)
                        listChildren.append(childNode)
#                       Restore the parent node
                        stack.append(otherStack.pop())
        return listChildren

    def h1(self):
        # count the number of blocks not on the first stack, then for every pair of
        # blocks on the first stack which are not in order, at least 3 moves
        # are needed to set them right.

        h = 0
        for stack in self.state[1:]:
            h = h + len(stack)
        # check if the blocks in the first stack are in order
        firstStack = self.state[0]
        for i in range(0, len(firstStack)-1):
            if (firstStack[i] > firstStack[i+1]):
                h = h + 3
        return h

    def h2(self):
        ''' This heuristic tries to mimic the "human" method of placing the blocks, first locate 'a', get it to its position,
        then 'b' and so on '''
        numBlocks = 0
        for stack in self.state:
            numBlocks = numBlocks + len(stack)
#       Initialize the heuristic assuming that none of the blocks are in place, then the minimum possible value for h is
#       numBlocks
        h = 4*numBlocks

        goalState = list(string.ascii_lowercase[0:numBlocks])
        if self.state[0] == goalState:
            return 0
#       This is definitely not the goal state, so compute the heuristic value by comparing the current state with the
#       goal state
        for blkIdx, block in enumerate(goalState):
            flgNxtBlk = False
#       Search for "block" in the stacks starting from 'a', find the first block which is out of place and compute the
#       heuristic
            for stackNo, stack in enumerate(self.state):
                for idx, letter in enumerate(stack):
                    if letter == block:
#                       Check if "letter" is already in its correct position.
                        if stackNo == 0 and idx < len(stack):
                            if stack[idx] == goalState[idx]:
#                               I can't right away switch to the next block, for eg: initially the heuristic value is
#                               determined by the position of block 'a', if this is the first node with block 'a' in the right
#                               position then there is a discontinuity in the heuristic function resulting in a higher
#                               heuristic value being assigned if it is suddenly decided by the position of 'b'. This can result 
#                               in this state not being chosen even if it is the best possible choice. The solution I use is to 
#                               check if this is the case and incentivize choosing this state. In case the parent doesn't have 
#                               the block in the right position, then there is no need to go further, this is the way to go.
                                h = h - 4
                                if stack[idx] not in self.parent.state[0]:
                                    return h
                                else:
#                                   This block is already in its correct position, go to the next one
                                    flgNxtBlk = True
                                    break
#                       We found the first block that is out of place and not already in its correct position, this is the one 
#                       that decides the heuristic value.
                        if stackNo != 0:
#                           If the block is not on the first stack, all the blocks on top of it must be moved first
                            h = h + len(stack[idx+1:])
#                       Irrespective of where the block is, all the out of place blocks on the first stack must be
#                       removed. Since the blocks are checked in order, block represents the index of the first block
#                       that is out of place on stack 0. An additional step is needed to actually get the block into
#                       place.
                        h = h + len(self.state[0][blkIdx:]) + 1
                        return h
                if flgNxtBlk:
                    break
        return

    def h4(self):
        ''' This heuristic tries to mimic the "human" method of placing the blocks, first locate 'a', get it to its position,
        then 'b' and so on '''
        numBlocks = 0
        for stack in self.state:
            numBlocks = numBlocks + len(stack)
#       Initialize the heuristic assuming that none of the blocks are in place, then the minimum possible value for h is
#       numBlocks
        h = 4*numBlocks

        goalState = list(string.ascii_lowercase[0:numBlocks])
        if self.state[0] == goalState:
            return 0
#       This is definitely not the goal state, so compute the heuristic value by comparing the current state with the
#       goal state
        for blkIdx, block in enumerate(goalState):
            flgNxtBlk = False
#       Search for "block" in the stacks, starting from 'a', find the first block which is out of place and compute the
#       heuristic
            for stackNo, stack in enumerate(self.state):
                for idx, letter in enumerate(stack):
                    if letter == block:
                        if stackNo == 0 and idx < len(stack):
                            if stack[idx] == goalState[idx]:
#                               I can't right away switch to the next block, for eg: initially the heuristic value is
#                               determined by the position of block 'a', if this is the first node with block 'a' in the right
#                               position then there is a discontinuity in the heuristic function resulting in a higher
#                               heuristic value being assigned if it is decided by the position of 'b'. This can be
#                               prevented by checking the parent to see if this is the case.
                                h = h - 4
                                if stack[idx] not in self.parent.state[0]:
                                    return h
                                else:
#                                   This block is in its correct position, go to the next one
                                    flgNxtBlk = True
                                    break
#                       We found the first block that is out of place, this is the one that decides the heuristic value.
                        if stackNo != 0:
#                           If the block is not on the first stack, all the blocks on top of it must be moved first
                            h = h + len(stack[idx+1:])
#                       Irrespective of where the block is, all the out of place blocks on the first stack must be
#                       removed. Since the blocks are checked in order, block represents the index of the first block
#                       that is out of place on stack 0. An additional step is needed to actually get the block into
#                       place.
                        h = h + len(self.state[0][blkIdx:]) + 1
#                       Right now the heuristic only considers the cost of getting the next block into place and this is
#                       a very short-sighted approach. It is possible that the algorithm picks up a 'd' which is on top
#                       of an 'a' and places it on top of the 'b' which is needed next!
#                       The solution is to check if the blocks needed sooner don't get buried underneath as a result of
#                       our move. In particular, I can check if the top block is needed earlier than the ones at the
#                       bottom for each of the stacks other than 0.
                        for stack in self.state[1:]:
                            for elem in stack:
                                if stack[-1] > elem:
#                               In this case, it is necessary that the top block is moved to another stack to make
#                               progress.
                                    h = h + 1
                        return h
                if flgNxtBlk:
                    break
        return

    def h5(self):
        ''' This heuristic tries to mimic the "human" method of placing the blocks, first locate 'a', get it to its position,
        then 'b' and so on '''
        numBlocks = 0
        for stack in self.state:
            numBlocks = numBlocks + len(stack)
#       Initialize the heuristic assuming that none of the blocks are in place, then the minimum possible value for h is
#       numBlocks
        h = 8*numBlocks

        goalState = list(string.ascii_lowercase[0:numBlocks])
        if self.state[0] == goalState:
            return 0
#       This is definitely not the goal state, so compute the heuristic value by comparing the current state with the
#       goal state
        for blkIdx, block in enumerate(goalState):
            flgNxtBlk = False
#       Search for "block" in the stacks, starting from 'a', find the first block which is out of place and compute the
#       heuristic based on how far it is from its correct position.
            for stackNo, stack in enumerate(self.state):
                for idx, letter in enumerate(stack):
                    if letter == block:
                        if stackNo == 0 and idx < len(stack):
                            if stack[idx] == goalState[idx]:
#                               I can't right away switch to the next block, for eg: initially the heuristic value is
#                               determined by the position of block 'a', if this is the first node with block 'a' in the right
#                               position then there is a discontinuity in the heuristic function resulting in a higher
#                               heuristic value being assigned if it is decided by the position of 'b'. This can be
#                               prevented by checking the parent to see if this is the case.
                                h = h - 8
                                if self.parent is None or stack[idx] not in self.parent.state[0]:
                                    return h
                                else:
#                                   This block is in its correct position, go to the next one
                                    flgNxtBlk = True
                                    break
#                       We found the first block that is out of place, this is the one that decides the heuristic value.
                        if stackNo != 0:
#                           If the block is not on the first stack, all the blocks on top of it must be moved first
                            h = h + len(stack[idx+1:])
#                       Irrespective of where the block is, all the out of place blocks on the first stack must be
#                       removed. Since the blocks are checked in order, block represents the index of the first block
#                       that is out of place on stack 0. An additional step is needed to actually get the block into
#                       place.
                        h = h + len(self.state[0][blkIdx:]) + 1
#                       All blocks > than the smallest block will have to be moved to other stacks to get the
#                       block and this reverses the order, so considering only this block is sufficient. Since the same
#                       approach is followed always, there is no risk of this being a short-sighted approach
                        for stack in self.state[1:]:
                            if len(stack) > 0:
                                minStack = stack[0]
                                minStackIdx = 0
                                for idx in range(1,len(stack)):
                                    if minStack > stack[idx]:
                                        minStack = stack[idx]
                                        minStackIdx = idx
                                for otherElem in stack[minStackIdx+1:]:
                                    if otherElem > minStack:
                                        h = h + 1
                        return h
                if flgNxtBlk:
                    break
        return

