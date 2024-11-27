# Assignment 4: Sudoku Solver
# Goal: Create a program that fills in a sudoku game.
import functools
import copy




# EASY

input_board = [
    [6, 0, 8, 7, 0, 2, 1, 0, 0],
    [4, 0, 0, 0, 1, 0, 0, 0, 2],
    [0, 2, 5, 4, 0, 0, 0, 0, 0],
    [7, 0, 1, 0, 8, 0, 4, 0, 5],
    [0, 8, 0, 0, 0, 0, 0, 7, 0],
    [5, 0, 9, 0, 6, 0, 3, 0, 1],
    [0, 0, 0, 0, 0, 6, 7, 5 ,0],
    [2, 0, 0, 0, 9, 0, 0, 0 ,8],
    [0, 0, 6, 8, 0, 5, 2, 0 ,3]
]

# HARD

# input_board = [
#     [0, 7, 0, 0, 4, 2, 0, 0, 0],
#     [0, 0, 0, 0, 0, 8, 6, 1, 0],
#     [3, 9, 0, 0, 0, 0, 0, 0, 7],
#     [0, 0, 0, 0, 0, 4, 0, 0, 9],
#     [0, 0, 3, 0, 0, 0, 7, 0, 0],
#     [5, 0, 0, 1, 0, 0, 0, 0, 0],
#     [8, 0, 0, 0, 0, 0, 0, 7 ,6],
#     [0, 5, 4, 8, 0, 0, 0, 0 ,0],
#     [0, 0, 0, 6, 1, 0, 0, 5 ,0]
# ]


# Example of my own

# input_board = [
#     [0, 0, 0, 6, 0, 0, 4, 0, 0],
#     [7, 0, 0, 0, 0, 3, 6, 0, 0],
#     [0, 0, 0, 0, 9, 1, 0, 8, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 5, 0, 1, 8, 0, 0, 0, 3],
#     [0, 0, 0, 3, 0, 6, 0, 4, 5],
#     [0, 4, 0, 2, 0, 0, 0, 6 ,0],
#     [9, 0, 3, 0, 0, 0, 0, 0 ,0],
#     [0, 2, 0, 0, 0, 0, 1, 0 ,0]
# ]

# For Manual Entry of the SUDOKU BOARD

# input_board = []
# for i in range(1, 10):
#     rowList = []
#     for j in range(1, 10):
#         val = input("Enter value for the given slot (0 represent empty cells) in row " + str(i) + " and col " + str(j) + ": ")
#         rowList.append(val)
#     input_board.append(rowList)


# PLEASE COMMENT OUT ALL THE INPUT BOARDS EXCEPT THE ONE YOU ARE USING or ALL THE BOARD IF YOU ARE USING THE MANUAL WAY
# IMPORTANT: 0 represent empty cells

# Visually displays the information in the Sudoku board on the terminal.
def display_board(board):
    print("  State of the Sudoku Board:  ")
    for x in range(len(board) + 1):
        if x % 3 == 0:
            print("  - - - -  - - - - - - - - - ")

        if x == len(board):
                break

        for y in range(len(board[0])):
            if y % 3 == 0:
                print(" | ", end="")

            if y == 8:
                print(board[x][y], " | ")
            else:
                print(str(board[x][y]) + " ", end="")



    

# Return a list of all the possible values that can be inserted to a
# given cell on the boad checking if that value is already on the same
# row, column or square.
def legal_values(board, row, col):
    #print("Row: ", row, "  Col:", col, " Value: ", board[row][col])

    legal_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # Put all the values that cannot be inserted in the given cell to a ]
    # list and remove these illegal values in the list from the list for 
    # all possible elements, which is named legal_values.

    illegal_values = []

    # case 1: check row 
    for i in range(0, 9):
        if board[row][i] != 0:
            illegal_values.append(board[row][i])

    
    # case 2: check column
    for i in range(0, 9):
        if board[i][col] != 0 and not (board[i][col] in illegal_values):
            illegal_values.append(board[i][col])


    # case 3: check square
    square_x = (row // 3) *3
    square_y = (col // 3) *3   
    for i in range(square_x , square_x  + 3):       # iterate over the values in the square
        for j in range(square_y, square_y + 3):     # where the given cell is located
            if board[i][j] != 0 and not (board[i][j] in illegal_values):
                illegal_values.append(board[i][j])
    
    #print([x for x in legal_values if x not in illegal_values])

    list_values = [x for x in legal_values if x not in illegal_values]

    
    return list_values




# Forwards Checking: Store all the domain of each unassigned cell on the board 
# in a dictionary. 
def set_domains(board):
    # empty dictionary
    domain_set = {}
    for i in range(0, 9):
        for j in range(0, 9):
            if board[i][j] == 0:
                domain_set.update({(i,j) : legal_values(board, i , j)})
            else:
                domain_set.update({(i,j) : list()})
    return domain_set

# Print the keys and values of variable in the dictionary on seperate lines.
def print_domain(domain):
    print("------DOMAIN------")
    print("|Cell   :  Values|")
    print("------------------")
    for key in domain: 
        print(key, ' : ', domain[key])




# Variable Ordering: Sort the variables from the fewest legal values in its
# domain to the highest legal values in its domain.
def variable_ordering(domain_dict):
    domain_dict =  dict(sorted(domain_dict.items(), key=lambda item: len(item[1])))
    return domain_dict



# Value Ordering: Create a frequency list based on the frequency of the values on the row, column and 
# square that each box is located. Order the possible values that box can take based on that list so 
# that less frequent possible values are in the front vice versa.
def value_ordering(domain):
    keys = list(domain.keys())
   
    # initialize the frequency list for all slots/boxes on the sudoku 
    total_freq = {};  freq_row = {}; freq_col = {}; freq_square = {}
    for box in set_domains(input_board):
        freq_row[box] = freq_col[box] = freq_square[box] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    # store all the frequency from row, col, and square 
    count_row(domain, freq_row); count_col(domain, freq_col); count_square(domain, freq_square)

    # sum all the freqency from row, col, and square
    add_dict(domain, total_freq, freq_row, freq_col, freq_square)

    # sort each list of the corresponding key based on this new freqency list
    for x in range(0, 81):
        if (len(domain[keys[x]]) >= 2):

            # comparator for sorting
            def comparator(a, b):
                if total_freq[keys[x]][a-1] < total_freq[keys[x]][b-1]:
                    return 1
                elif total_freq[keys[x]][a-1] > total_freq[keys[x]][b-1]:
                    return -1
                else:
                    return 0

            domain[keys[x]] = sorted(domain[keys[x]], key=functools.cmp_to_key(comparator), reverse = True)

    return domain


# Maps slots on the sudoku board to the frequency of values on their row.
def count_row(domain, freq_dict):
    keys = list(domain.keys())
    freq_list = []
    for x in range(0, 81):
        # create a freq list for every row
        if x % 9 == 0:

            freq_list = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            for i in range(x, x + 9):
                # puts all possible values of a slot in the freq list
                for elts in domain[keys[i]]:
                    freq_list[elts-1] += 1

            index = -1  #find the slot that has the value with freq 1
            for i in range(0, 9):
                # find the value with freq 1
                if freq_list[i] == 1:
                    index = i

            for i in range(x, x + 9): # go over the slots in a row

                for elts1 in domain[keys[i]]: # go over legal values of that slot (elts: 1 -9)

                    if index == elts1 -1 : # cell with that value is keys(k)
                        # update the input board
                        input_board[x // 9][i % 9] = elts1 
                        
                        # remove legal values of that slot from the freq list
                        for elts2 in domain[keys[i]]:
                             freq_list[elts2-1] -= 1
                        
            freq_dict[keys[x]] = freq_list
        
        else : 
            freq_dict[keys[x]] = freq_list 

        


# Maps slots on the sudoku board to the frequency of values on their column.
def count_col(domain, freq_dict):
    keys = list(domain.keys())
    freq_list = []
    for x in range(0, 9):
        freq_list = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        # Store the freq of elements in all cols
        for i in range(x, len(freq_dict), 9):
            for elts in domain[keys[i]]:
                freq_list[elts-1] += 1


        # --------------  OPTIMIZATION -------------- #

        # If there is any possible value with frequency of 1 in that 
        # column, put that value on the corresponding spot on the board
        index = -1 # find the value with freq 1
        for i in range(0, 9):
            if freq_list[i] == 1:
                index = i
        
        for i in range(x, len(freq_dict), 9):
            for elts in domain[keys[i]]:
                if index == elts - 1:                       
                    # update the input board
                    input_board[i// 9][x % 9] = elts
                
                    # remove legal values of that slot from the freq list
                    for elts2 in domain[keys[i]]:
                        freq_list[elts2-1] -= 1
        # --------------  ------------ -------------- #


        # insert the same freq-list to all elements on the column
        for i in range(x, len(freq_dict), 9):
            freq_dict[keys[i]] = freq_list
        





# Maps slots on the sudoku board to the frequency of values on their square.
def count_square(domain, freq_dict):
    keys = list(domain.keys()) 
    for i in range(0, 81, 27):
        for j in range(i, i + 9, 3):          
            square_helper(j,keys, domain, freq_dict)



# Helps mapping for squares.
def square_helper(index, keys, domain, freq_dict):
    freq_list = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(0, index + 20, 9):
        for j in range(i, i + 3):
            for elts in domain[keys[j]]:     
                freq_list[elts-1] += 1

    # --------------  OPTIMIZATION -------------- #

    # If there is any possible value with frequency of 1 in that 
    # square, put that value on the corresponding spot on the board 
    index = -1 # find the value with freq 1
    for i in range(0, 9):
        # find the value with freq 1
        if freq_list[i] == 1:
            index = i


    for i in range(0, index + 20, 9):
        for j in range(i, i + 3):

            for elts1 in domain[keys[j]]:
                if index == elts1 - 1:                       
                    # update the input board
                    input_board[i// 9][j % 9] = elts1 
                
                    # remove legal values of that slot from the freq list
                    for elts2 in domain[keys[i]]:
                        freq_list[elts2-1] -= 1
    
    # --------------  ------------ -------------- #

    for i in range(0, index + 20, 9):
        for j in range(i, i + 3):
            freq_dict[keys[j]] = freq_list  
            

# Sum up the frequency of values on row, column, and square
def add_dict(domain, dict0, dict1, dict2, dict3):
    keys = list(domain.keys())
    for i in range(0, 81):
        dict0.update({keys[i]  :  add_list(dict1[keys[i]], dict2[keys[i]], dict3[keys[i]])})
    return dict0

# Add three lists of frequency to each other
def add_list(list1, list2, list3):
    list0 = []
    for i in range(0, 9):
        list0.append(list1[i] + list2[i] + list3[i])
    return list0

# given the domain of a board, find the empty slot with least legal values 
def next_empty(domain):
    for key in domain.keys():
        if len(domain[key]) != 0:
            return helper_next_empty(key)
    return None

# return the position on the board of a slot
def helper_next_empty(key):
    for i in range(0, 9):
        for j in range(0, 9):
            if key[0] == i and key[1] == j:
                return [i, j]


# Termination Case 1: for recursion in depth-first-search
# Find the next empty cell in the board. If all the cell are populated, 
# then returns false which indicates the board is full.
def board_complete(board):
    for i in range(0, 9):
        for j in range(0, 9):
            if (board[i][j] == 0): 
                return False
    return True        

# Termination Case 2: for recursion in depth-first-search
# Check if all the values on the board comply by the rules of sudoku
def checkBoard(board):
    for i in range(0, 9):
        # create a freq list for every row
        freq_row = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for j in range(0 , 9):
            freq_row[board[i][j] -1] += 1

        if freq_row != [1, 1, 1, 1, 1, 1, 1, 1, 1]:
            return False

        freq_col = [0, 0, 0, 0, 0, 0, 0, 0, 0]
         # Store the freq of elements in all cols
        for i in range(0,  9):
            freq_col[board[j][i] -1] += 1

        if freq_col != [1, 1, 1, 1, 1, 1, 1, 1, 1]:
            return False


        # case 3: check square
        freq_square = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        square_x = (i // 3) *3
        square_y = (j // 3) *3   
        for r in range(square_x , square_x  + 3):       
            for c in range(square_y, square_y + 3):     
                freq_square[board[r][c] -1] += 1
        
        if freq_square != [1, 1, 1, 1, 1, 1, 1, 1, 1]:
            return False

    return True
   
  

BOARD = None
solved = False
domain = None
board = None

# Use depth-first-search to find the solution for the sudoku board.
def run_sudoku(newboard):

    global BOARD; global solved; global domain; global board

    # Termination Cases:
    if board_complete(board) == True and checkBoard(board) == True:
        BOARD = copy.deepcopy(board)
        solved = True

    else:
        if next_empty(domain) == None:
            return

        spot = next_empty(domain)
        row = spot[0]; col = spot[1]

        # get legal values
        legal_values = domain[(row, col)]

        # put each legal value of an empty cell 1q
        for i in range(0, len(legal_values)):

            # deep copy to return back to the old state when back tracking
            newboard = copy.deepcopy(board) 

            # update the next empty cell with a value in its list of all legal values
            board[row][col] = legal_values[i]
            domain = variable_ordering(value_ordering(set_domains(board)))

            # recursion
            run_sudoku(newboard)

            # Termination Case:
            if solved:
                
                return "  SUDOKU IS SOLVED: "

            # Back-Tracking
            if not solved:
                board = copy.deepcopy(newboard)
                domain = variable_ordering(value_ordering(set_domains(board)))


  


# display the initial version of the board
display_board(input_board)
    

# set domains, do forward, checking, value ordering, variable ordering, smart backtracking
domain = variable_ordering(value_ordering(set_domains(input_board)))

# run SUDOKU
board = input_board
sudoku = run_sudoku(input_board)
print(sudoku)


# display the final version of the board
display_board(BOARD)