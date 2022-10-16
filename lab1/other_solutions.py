import random
import heapq
import logging
import bisect
from typing import Callable
from time import perf_counter
NUMBER=0
WIDTH=0
prob=()

class PriorityQueue:
    """A basic Priority Queue with simple performance optimizations, code taken from Prof Squillero repo"""

    def __init__(self):
        self._data_heap = list()
        self._data_set = set()

    def __bool__(self):
        return bool(self._data_set)
    def __contains__(self, item):
        return item in self._data_set
    def push(self, item, p=None):
        assert item not in self, f"Duplicated element"
        if p is None:
            p = len(self._data_set)
        self._data_set.add(item)
        heapq.heappush(self._data_heap, (p, item))

    def pop(self):
        p, item = heapq.heappop(self._data_heap)
        self._data_set.remove(item)
        return item

def problem(N, seed=None):
    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]

#here are the functions used by the search algorithm used, the mem versions are just versions that try to use a little bit less memory
#but because of how memory demanding the algorithm used is the impact is still light
#while the width versions of the actions functions serve to take only the WIDTH/100 most promising childs, this is done with a heuristics
#calculated in the function that is not aware of how the child will look like, so it's not the optimal heuristic but it works well
def __lentup__(a):
    """This function is used to calculate the summed length of a tuple that containes tuples"""
    len_=0
    for i in a:
        len_+=len(i)
    return len_

def __lentupmem__(a):
    len_=0
    for i in a:
        len_+=len(prob[i])
    return len_

def actions_(state):
    """This function generates the list of actions that we can take starting from a state
    , states already seen or duplicates of already seen states shouldn't be considered"""
    return [tup_ for tup_ in prob if tup_ not in state]

def set_still_needed(state):
    """This function generates the difference between two sets, so we can get which numbers we haven't covered yet with our state"""
    return set([_ for _ in range(0,NUMBER)])-set(sequence_found(state))

def actionswidth(state):
    """This function generates the list of actions that we can take starting from a state
    , states already seen or duplicates of already seen states shouldn't be considered"""
    set_=set_still_needed(state)
    lensetneeded_=len(set_)
    list_=[]
    for a in prob:
        if a not in state:
            ind_=(-len(set_-set(a))+len(set_))*(len(a)//lensetneeded_)
            bisect.insort_right(list_,a,key=lambda a :ind_)
    return [tup_ for _,tup_ in zip(range(0,int(WIDTH/100*len(list_))),list_)]


def isDupPresentmem(state,cont):
    """Function to check for duplicates in the memory version in the memory version"""
    for a in state:
        if prob[a]==cont:
            return True
    return False


def actionsmem(state):
    """This function generates the list of actions that we can take starting from a state
    , states already seen or duplicates of already seen states shouldn't be considered"""
    return [prob.index(a) for a in prob if not isDupPresentmem(state,a)]

def set_still_neededmem(state):
    return set([_ for _ in range(0,NUMBER)])-set(sequence_foundmem(state))

def actionsmemwidth(state):
    """This function generates the list of actions that we can take starting from a state
    , states already seen or duplicates of already seen states shouldn't be considered"""
    set_=set_still_neededmem(state)
    lensetneeded_=len(set_)
    list_=[]
    for a in prob:
        if not isDupPresentmem(state,a):
            ind_=(-len(set_-set(a))+len(set_))*(len(a)//lensetneeded_)
            bisect.insort_right(list_,prob.index(a),key=lambda a :ind_)
    return [tup_ for _,tup_ in zip(range(0,int(WIDTH/100*len(list_))),list_)]

def goal_test(state):
    """This function tests if the current state has all of the numbers needed, to do that
    we test the length of a set(set so no duplicates) that has all the valid numbers of this state
    (a valid number is a number that is from 0 to N-1)"""
    return len(set(b for a in state for b in a))==NUMBER

def goal_testmem(state):
    """This function tests if the current state has all of the numbers needed, to do that
    we test the length of a set(set so no duplicates) that has all the valid numbers of this state
    (a valid number is a number that is from 0 to N-1)"""
    return len(set([b for a in state for b in prob[a]]))==NUMBER
def sequence_found(state):
    """This function returns the set of all the valid numbers found in this set
    (a valid number is a number that is from 0 to N-1)"""
    return set([b for a in state for b in a])

def sequence_foundmem(state):
    """This function returns the set of all the valid numbers found in this set
    (a valid number is a number that is from 0 to N-1)"""
    return set([b for a in state for b in prob[a]])
def result(state,action):
    """This function returns a new state starting from one and it and it adds a list(action)
    to its data"""
    #generate a state starting from last one
    lt=list(state)
    bisect.insort_right(lt,action)
    #add action to the state
    return tuple(lt)

def resultmem(state,action):
    """This function returns a new state starting from one and it and it adds a list(action)
    to its data"""
    #generate a state starting from last one
    lt=list(state)
    bisect.insort_right(lt,action)
    return tuple(lt)
    #add action to the state

#functions that do the search algorithm
def search(initial_state:tuple,
    actions:Callable,
    goal_test:Callable,
    parent_state:dict,state_cost:dict,
    priority_function:Callable,unit_cost:Callable):
    """This function search for a valid solution"""
    frontier = PriorityQueue()
    parent_state.clear()
    state_cost.clear()
    state = initial_state
    parent_state[state] = None
    state_cost[state] = 0
    #print(f"\n\nNUMBER {NUMBER} WIDTH {WIDTH}\n\n")
    while state is not None and not goal_test(state):
        #iterate through the actions of the state itself
        #print(f"State {state}")
        #for a in actions(state):
        for a in actions(state):
            #generate the new state and its cost
            #print(f"\n\nTuple {a}")
            new_state=result(state,a)
            u_cost= unit_cost(new_state)
            if new_state not in state_cost and new_state not in frontier:
                #add this new state to the parent state and state cost dictionaries
                parent_state[new_state]=state
                state_cost[new_state]=state_cost[state]+u_cost
                #push this new state into the frontier
                frontier.push(new_state,p=priority_function(new_state))
                #logging.info(f"Pushed state {new_state}, with priority {priority_function(new_state)}")
        #if there is an element to be popped from the frontier do it and set it as the new state
        #otherwise put state as None because no element to expand is left so no solution has been found
        if frontier:
            state=frontier.pop()
            #logging.info(f"Popped state {state}, with priority {priority_function(state)}")
        else:
            state=None
            print("Couldn't find any solution")
    #iterate through the state to get its path
    path = list()
    s = state
    while s:
        path.append(s)
        s = parent_state[s]
    print(f"Found a solution in {len(path):,} steps; visited {len(state_cost):,} states")
    """if state:
        print(f"Found a solution in {len(state):,} steps; visited {len(state_cost):,} states")
    return state"""
    return list(reversed(path))

def searchmem(initial_state:tuple,
    actions: Callable,
    goal_test:Callable,
    state_cost:dict,
    priority_function:Callable):
    """This function search for a valid solution"""
    frontier = PriorityQueue()
    state_cost.clear()

    state = initial_state
    state_cost[state] = 0
    #seq_found=()
    while state is not None and not goal_test(state):
        #iterate through the actions of the state itself
        for a in actions(state):
            #generate the new state and its cost
            new_state=resultmem(state,a)
            #new_seq=sequence_foundmem(new_state)
            #if new_seq==seq_found:
                #continue
            #u_cost= unit_cost(new_state)
            if new_state not in state_cost and new_state not in frontier:
                #add this new state to the parent state and state cost dictionaries
                #parent_state[new_state]=state
                state_cost[new_state]=state_cost[state]+1
                #push this new state into the frontier
                frontier.push(new_state,p=priority_function(new_state))
                #logging.info(f"Pushed state {new_state}, with priority {priority_function(new_state)}")
        #if there is an element to be popped from the frontier do it and set it as the new state
        #otherwise put state as None because no element to expand is left so no solution has been found
        if frontier:
            state=frontier.pop()
            #logging.info(f"Popped state {state}, with priority {priority_function(state)}")
            #seq_found=sequence_foundmem(state)
            #prio_=priority_function(state)
            #if prio_>maxprio:
                #print(f"Popped state {state}, with priority {prio_}")
                #maxprio=prio_
        else:
            state=None
            print("Couldn't find any solution")
    if state:
        print(f"Found a solution in {len(state):,} steps; visited {len(state_cost):,} states")
    return state

def set_covering(numbers,mem=False,widthex=False,widthval=100):
    """interface to the system, numbers is the list of size of problems we want to solve , mem is a bool to start the mem version instead of the normal one, and also widthex is a boolean to select if
the width is limited, and in that case widthval is the value to limit it, so 50 will make us search 50% of the nodes of a child etc.
so with 100 we have the normal version(a little bit slower because of the additional calculation that without the widthex we don't do)"""
    if widthex:
        global WIDTH
        WIDTH=widthval
    for number in numbers:
        global NUMBER
        NUMBER=number
        #generate a new problem
        probl=problem(NUMBER,seed=42)
        global prob
        prob=tuple([tuple(a) for a in probl])
        print(f"Problem with value {NUMBER} : {prob}")
        #setup for the search
        #the priority function used start with minus len of the sequence found of that set
        #so if the state is like [[0,1,5,8]] the sequence found will be [0,1,5] so its len
        #will be 3, so we have -3, then we add to this the len of the whole state, len of
        #the State class has been written in a way to sum the len of all of the lists inside
        #the outer list, so in this case we'll get 4, so -3 + 4 = 1, this will be the priority
        #of this priority queue, in this way we favorite the states that don't have any
        #duplicates or non valid numbers(8 in this case), so a state like [[0,3],[2,5]]
        #will have priority equal to 0 and will be popped before the last one
        state_cost=dict()
        times_=perf_counter()
        if mem:
            state=tuple()
            if widthex:
                sol=searchmem(initial_state=state,actions=actionsmemwidth,goal_test=goal_testmem,state_cost=state_cost,
                priority_function=lambda a: -len(sequence_foundmem(a))+__lentupmem__(a))
            else:
                sol=searchmem(initial_state=state,actions=actionsmem,goal_test=goal_testmem,state_cost=state_cost,
                priority_function=lambda a: -len(sequence_foundmem(a))+__lentupmem__(a))
            print(f"The search for problem of value {NUMBER} lasted {perf_counter()-times_}")
            if sol:
                print(f"Solution {tuple([prob[a] for a in sol])} with weight {__lentupmem__(sol)}")
        else:
            state=tuple([()])
            parent_state=dict()
            if widthex:
                sol=search(initial_state=state,actions=actionswidth,goal_test=goal_test,parent_state=parent_state,state_cost=state_cost,
                priority_function=lambda a: -len(sequence_found(a))+__lentup__(a),unit_cost=lambda a: 1)
            else:
                sol=search(initial_state=state,actions=actions_,goal_test=goal_test,parent_state=parent_state,state_cost=state_cost,
                priority_function=lambda a: -len(sequence_found(a))+__lentup__(a),unit_cost=lambda a: 1)
            print(f"The search for problem of value {NUMBER} lasted {perf_counter()-times_}")
            if len(sol)>0:
                sol_=sol[len(sol)-1]
                print(f"Path {sol} Solution {sol_} with weight {__lentup__(sol_)}")

#call the function to solve the desired problem
set_covering([100],mem=False,widthex=True,widthval=5)