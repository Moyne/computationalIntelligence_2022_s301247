import random
import heapq
import logging
import bisect
from typing import Callable
from time import perf_counter

NUMBER=0
WIDTH=100
METRIC=()
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

def __lentup__(a):
    len_=0
    for i in a:
        len_+=len(i)
    return len_

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

def goal_test(state):
    """This function tests if the current state has all of the numbers needed, to do that
    we test the length of a set(set so no duplicates) that has all the valid numbers of this state
    (a valid number is a number that is from 0 to N-1)"""
    return len(set(b for a in state for b in a))==NUMBER

def sequence_found(state):
    """This function returns the set of all the valid numbers found in this set
    (a valid number is a number that is from 0 to N-1)"""
    return set([b for a in state for b in a])

def result(state,action):
    """This function returns a new state starting from one and it and it adds a list(action)
    to its data"""
    #generate a state starting from last one
    lt=list(state)
    bisect.insort_right(lt,action)
    #add action to the state
    return tuple(lt)

def search(initial_state:tuple,
    actions:Callable,
    goal_test:Callable,
    parent_state:dict,state_cost:dict,
    priority_function:Callable,priority_function_inner:Callable):
    """This function search for a valid solution"""
    frontier = PriorityQueue()
    parent_state.clear()
    state_cost.clear()
    state = initial_state
    parent_state[state] = None
    state_cost[state] = 0
    while state is not None and not goal_test(state):
        #iterate through the actions of the state itself
        for a in actions(state):
            #generate the new state and its cost
            new_state=result(state,a)
            u_cost= 1
            state_cost_new_state=state_cost[state]+u_cost
            prio_=priority_function_inner(new_state)
            if prio_>METRIC[state_cost_new_state]:
                continue
            if new_state not in state_cost and new_state not in frontier:
                #add this new state to the parent state and state cost dictionaries
                parent_state[new_state]=state
                state_cost_new_state=state_cost[state]+u_cost
                state_cost[new_state]=state_cost_new_state
                #push this new state into the frontier
                frontier.push(new_state,p=priority_function(prio_))
                #logging.info(f"Pushed state {new_state}, with priority {prio_}")
        #if there is an element to be popped from the frontier do it and set it as the new state
        #otherwise put state as None because no element to expand is left so no solution has been found
        if frontier:
            state=frontier.pop()
            #logging.info(f"Popped state {state}, with priority {priority_function_inner(state)}")
            state_cost_new_state=state_cost[state]
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

def set_covering(numbers,widthval=100):
    """interface to the system, numbers is the list of size of problems we want to solve"""
    global WIDTH
    WIDTH=widthval
    for number in numbers:
        global NUMBER
        NUMBER=number
        #generate a new problem
        probl=problem(NUMBER,seed=42)
        global prob
        prob=tuple([tuple(a) for a in probl])
        #logging.info(f"Problem with value {NUMBER} : {prob}")
        global METRIC
        METRIC=tuple([0,0,2]+[_*5 for _ in range(1,len(prob))])
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
        state=tuple([()])
        parent_state=dict()
        sol=search(initial_state=state,actions=actionswidth,goal_test=goal_test,parent_state=parent_state,state_cost=state_cost,
            priority_function=lambda a: a,priority_function_inner=lambda a: -len(sequence_found(a))+__lentup__(a))
        print(f"The search for problem of value {NUMBER} lasted {perf_counter()-times_}")
        if len(sol)>0:
            sol_=sol[len(sol)-1]
            print(f"Path {sol} Solution {sol_} with weight {__lentup__(sol_)}")

#call the interface to solve the problems with the list of size of problems
set_covering([100],widthval=95)