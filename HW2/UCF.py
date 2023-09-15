import heapq
import copy 

# Nodes represent different arrangements of the pancake stack. 
class Node:
    children = [] # alternative arrangements of the current arragment after being flipped
    def __init__(self, array, backward_cost, rank): 
        self.array = array # arrangement of pancakes on the stack
        self.backward_cost = backward_cost #number of flips so far (records the backward cost)
        self.rank = rank # rank of the node in the tree

    # updates the arrangement of array corresponding to the given flip and increments the backward cost accordingly
    def child_arrangement(self, flip_index):
        #flip index: the index in the pancake stack arrangement where the spatula is inserted
        #flip all the pancakes in the stack in the corresponding order: the outer pancakes to inner pancakes 
        child = copy.deepcopy(self)

        for x in range((len(child.array)-flip_index) // 2):
            num_flips = 0

            temp = child.array[flip_index + x]
            child.array[flip_index + x] = child.array[len(child.array)- x- 1]
            child.array[len(child.array)- x- 1] = temp
            num_flips += 1

        child.backward_cost += num_flips
        child.rank += (len(child.array)-flip_index +1)

        return child

    # return a list of all pancake arrangements after all possible flips are applied
    def children_nodes(self):
        for i in range(0, len(self.array) - 1):
            self.children.append(self.child_arrangement(i)) 
        return self.children


    #---comparison functions to compare two nodes in the priority queue)---#
    
    # returns true if self has a lower total cost than other 
    def __lt__(self, other):
        bol_equal = not (self.backward_cost == other.backward_cost)
        if bol_equal:
                return self.backward_cost < other.backward_cost
        else: # in case the total costs are the same, conside their rank(which is the order they are added to the pq)
            return self.rank < other.rank
    
    
    def __repr__(self):
        return repr(self.array)


# Frontier of the A-Star search algorithm is a priority queue.
class Frontier():
        heap = []

        def __init__(self, node):
            self.heap.append(node)

        # push the node(pancake arrangement) onto the heap, maintaining heap invariant.
        def push(self, node):
            heapq.heappush(self.heap, node)

        # remove the root element in the heap and return that element
        def pop(self):
            root = heapq.heappop(self.heap)
            return root

        # return the root element
        def get(self):
            return self.heap[0]
        
        # replace the node with the lower back
        def replace(self, node):
            for x in range(len(self.heap)):
                if (self.heap[x].array == node.array):
                    if (node < self.heap[x]):
                        self.heap[x] = node
                        #heapq.heapify(self.heap)

        # check if the frontier contains the given node
        def contains(self, array):
            does_contain = False
            for i in range(len(self.heap)):
                if (self.heap[i].array == array):
                    does_contain = True
            return does_contain

        # check if the forntier is empty
        def is_Empty(self):
            if len(self.heap) == 0:
                return True
            else:
                return False 

        # print the frontier
        def __repr__(self):
            return repr(self.heap)

class A_Star():
        
        def __init__(self, initial_array):
            # keep track of the visited pancake arrangements
            self.visited = []
            # append the pancake arrangement that the user enters to the visited
            self.visited.append(Node(initial_array, 0, 1))
            # the frontier that feeds the a-star algorithm
            self.frontier = Frontier(Node(initial_array, 0, 1)) 

        # checks if the current arrangement of the pancakes is in the desired order
        def goal_state_check(self, node):
            check_flag = True
            if (not(len(node.array) == node.array[0])):
                check_flag = False
            for i in range((len(node.array) - 1)):
                if (not (node.array[i] - node.array[i+1] == 1)):
                    check_flag = False
            return check_flag

    	# exapnds the search 
        def expand_frontier(self, node):
            for child in node.children_nodes():
                if (not self.frontier.contains(child) and not self.visited_helper(child)):
                    self.frontier.push(child)
                    self.visited.append(child)
                elif self.frontier.contains(child):
                    self.frontier.replace(node)
          
        # checks if the node is in the visited list
        def visited_helper(self,node):
            for child in self.visited:
                if (child.array == node.array):
                    return True
            return False

        # runs the astar algorithm
        def algorithm(self):
            while (True):
                # check if the frotnier is empty
                if (self.frontier.is_Empty()) :
                    return False
                # pop the top element on the frontier
                to_be_explored = self.frontier.pop()
                # check if the popped element is in the goal state
                if (self.goal_state_check(to_be_explored)):
                    print("Goal state: ") # print the node if its in the goal state
                    print(to_be_explored)  
                    return to_be_explored
                # print the node regardless of its state
                print("Current state: ")
                print(to_be_explored)
                print('\n')
                # expand the node
                self.expand_frontier(to_be_explored)
                    

# --------- Main --------- #

print("You will enter up to 6 numbers from 1-6 in a random order! The numbers should have a comma and then a space in between each other!" + '\n')
numberList = input("Plase enter the numbers: ")
array = []
index = 0
array.append(int(numberList[index]))
while (index != -1 and index < len(numberList)-1):
    index = numberList.index(",", index)
    array.append(int(numberList[index + 2]))
    index = index + 2
astar = A_Star(array)
astar.algorithm()