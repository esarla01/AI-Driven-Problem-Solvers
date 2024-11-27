import random
import time
import string
from typing import List


blackboard = {
    #State of the System
    "BATTERY_LEVEL": int,
    "SPOT_CLEANING": bool,
    "GENERAL_CLEANING": bool,
    "DUSTY_SPOT": bool,
    "HOME_PATH": "",
}

s = "SUCCESS"
f = "FAILURE"
r = "RUNNING"

# Nodes are the bulding blocks of the BT
class Node:

    def __init__(self, status): 
        self.status = status
    
    


### TASKS ###

# ---A task alters the state of the system--- #
class Task(Node):
    def __init__(self, status): 
        self.status = status
    

# --- Different Tasks --- #

class Find_Home (Task):
    def run(self):
        print("Finding Home!" + '\n')
        blackboard["HOME_PATH"] =  str(random.randint(1, 5)) + " m straight, " + str(random.randint(1, 5)) + " m  left."
        print("The home is at " + blackboard["HOME_PATH"] + '\n')
        time.sleep(1)


class Go_Home (Task):
    def run(self):
        print("Going Home!" + '\n')
        time.sleep(1)


class Dock (Task):
    def run(self):
        print("Dock!" + '\n')
        time.sleep(3) #charging takes 3 seconds
        blackboard["BATTERY_LEVEL"] = 100
        print("     The robot is charged. The battery is now 100%."+ '\n')
        time.sleep(1)
    

class Clean_Spot (Task):
    def run(self):
        print ("The spot is being cleaned!"  + '\n')
        time.sleep(1)


class Clean_Floor (Task):
    def run(self):
        is_room_clean = random.randint(0, 10) 
        if (is_room_clean > 7):
            print("The floor is cleaned! Nothing more to clean!"  + '\n')
            time.sleep(1)
            self.status = f
        else:
            print("Cleaning the floor!" + '\n')
            self.status = r


class Done_General (Task):
    def run(self):
        print("General cleaning is finished!"  + '\n')
        time.sleep(1)
        blackboard["GENERAl_CLEANING"] = False


class Done_Spot (Task):
    def run(self):
        print("The spot is done!"  + '\n')
        time.sleep(1)
        blackboard["SPOT_CLEANING"] = False
            

class Do_Nothing (Task):
    def run(self):
        print("Do nothing!"  + '\n')
        time.sleep(1)




### CONDITIONS ###

# ---A condition tests some propert of the system--- #
class Condition(Node):
    def __init__(self): 
        self.status = ""
        

# --- Different Conditions --- #

class Battery_Level(Condition):
    def run(self):
        answer = int(input("Enter the battery level (0-100):") + '\n')
        while(not (answer >= 0 and answer <= 100)):
            answer = int(input("Enter a valid battery level (0-100):") + '\n')
        time.sleep(1)
        blackboard["BATTERY_LEVEL"] = answer
        battery_level = blackboard.get("BATTERY_LEVEL")
        if (battery_level < 30):
            print("Battery is " + str(battery_level) + "%. Starting the charging sequence..." + '\n')
            time.sleep(1)
            self.status = s
        else:
            print("Battery is " + str(battery_level) + "%. No need to recharge!" + '\n')
            time.sleep(1)
            self.status = f

class Spot_Cleaning(Condition):
    def run(self):
        spot_cleaning = blackboard["SPOT_CLEANING"]
        if (spot_cleaning):
            print("Performing SPOT CLEANING..." + '\n')
            time.sleep(1)
            self.status = s
        else:
            self.status = f

class General_Cleaning(Condition):
    def run(self):
        general_cleaning = blackboard["GENERAL_CLEANING"]
        if (general_cleaning):
            print("Performing GENERAL CLEANING..."  + '\n')
            time.sleep(1)
            self.status = s
        else:
            self.status = f

class Dusty_Spot(Condition):
    def run(self):
        dusty_probability = random.randint(1, 10)
        if dusty_probability > 3:
            blackboard["DUSTY_SPOT"] = True
        else:
            blackboard["DUSTY_SPOT"] = False
        if (blackboard["DUSTY_SPOT"]):
            print("Starting the dusty spot sequence..." + '\n')
            time.sleep(1)
            self.status = s
        else:
            print("There is no dusty spot!"+ '\n')
            time.sleep(1)
            self.status = f

### COMPOSITES ###


# A composite aggregates other tree-nodes
class Composite(Node):

    def __init__(self, children):
        self.status = ""
        self.children = children
        

# --- Different Composites --- #

class Sequence(Composite):
    def run(self):
        for child in self.children:
            child.run()
            if child.status == f:
                self.status = f
                break
            elif child.status == s:
                self.status = s

class Selection(Composite):
    def run(self):
        status_is = s
        for child in self.children:
            child.run()
            if child.status == s:
                self.status = s
            elif child.status == f:
                status_is = f
        self.status = status_is      

class Priority(Composite):
    def run(self):
        for child in self.children:
            child.run()
            if child.status == r:
                self.status = r
            elif child.status == s:
                self.status = s
            else: 
                self.status = f

               


### DECORATOR ###
# A decorator alters the basic behaviour of the tree-node it is associated with
class Decorator(Node):

    def __init__(self, child): 
        self.status = ""
        self.child = child

# --- Different Decorators --- #

class Timer(Decorator):
    def __init__(self, child, time):
        super().__init__(child)
        self.status = ""
        self.time = time

    def run(self):
        tic = time.time()
        elapsed = 0
        print("    Running the task!" + '\n')
        while (elapsed < self.time):
            self.child.run()
            self.status = r
            elapsed = time.time() - tic
        print("    The task is completed after " + str(self.time) + " seconds!" + '\n')
        self.status = s

class Until_Fails(Decorator):
   
    def run(self):
        print("     Repeating the task until fails."+ '\n')
        while self.child.status != f:
            self.child.run()
        self.status = s
        print("     Done!" + '\n')



def bt_build():
    print("Building the Behaviour Tree" + '\n')

    ###################### Sub-Tree 1 ######################

    battery_level = Battery_Level()
    find_home = Find_Home(s)
    go_home = Go_Home(s)
    dock = Dock(s)
    children_subtree1 = [battery_level, find_home, go_home, dock]
    seq_battery = Sequence(children_subtree1)


    ###################### Sub-Tree 2 ######################

    #### Sub-Tree 2 - Branch 1 ####
    spot = Spot_Cleaning()
    clean_spot1 = Clean_Spot(s)
    clean_timer1 = Timer(clean_spot1, 20)
    done_spot = Done_Spot(s)
    c1_children_subtree2 = [spot, clean_timer1, done_spot]

    seq_spot = Sequence(c1_children_subtree2)

    #### Sub-Tree 2 - Branch 2 (Dusty Spot) ####
    dusty_spot = Dusty_Spot()
    clean_spot2 = Clean_Spot(s)
    clean_timer2 = Timer(clean_spot2, 35)
    c2_children_subtree2 = [dusty_spot, clean_timer2]

    seq_dusty = Sequence(c2_children_subtree2)

    #### Sub-Tree 2 - Branch 2 (Priority) ####
    clean_floor = Clean_Floor(s)
    until_fails = Until_Fails(clean_floor)
    c3_children_subtree2 = [seq_dusty, until_fails]

    prio_dusty = Priority(c3_children_subtree2)


    #### Sub-Tree 2 - Branch 2 (Done General) ####
    done_general = Done_General(s)
    c4_children_subtree2 = [prio_dusty, done_general]

    seq_done_general = Sequence(c4_children_subtree2)

    #### Sub-Tree 2 - Branch 2 (General Cleaning) ####
    general_cleaning = General_Cleaning()
    c5_children_subtree2 = [general_cleaning, seq_done_general]

    seq_general_cleaning = Sequence(c5_children_subtree2)

    #### Sub-Tree 2 - Branch 2 (All) ####
    children_subtree2 = [seq_spot, seq_general_cleaning]

    second_branch_selector = Selection(children_subtree2)

    #### Main-Tree - Branch 2 (All) ####
    do_nothing = Do_Nothing(s)
    children = [seq_battery, second_branch_selector, do_nothing]

    tree_priority = Priority(children)
    return tree_priority
    

### input take-in ###

def pick_cleaning():
    cleaning_pick = int(input("Spot cleaning (1), general cleaning (2), both (3), do nothing (4), or exit (5)? ") + '\n')
    if cleaning_pick == 1:
        blackboard["SPOT_CLEANING"] = True
        blackboard["GENERAL_CLEANING"] = False
    elif cleaning_pick == 2:
        blackboard["SPOT_CLEANING"] = False
        blackboard["GENERAL_CLEANING"] = True
    elif cleaning_pick == 3:
        blackboard["SPOT_CLEANING"] = True
        blackboard["GENERAL_CLEANING"] = True
    elif cleaning_pick == 4:
        blackboard["SPOT_CLEANING"] = False
        blackboard["GENERAL_CLEANING"] = False
    elif cleaning_pick == 5:
        exit()
    else:
        print("Invalid input. Enter 1,2,3, or 4!" + '\n')
        pick_cleaning()


### Main ###
    
count = 0
while (count < 15):
    pick_cleaning()
    bt_build().run()
    time.sleep(1)

    

