import random
from sys import argv
from itertools import combinations
NUMBER=0
def problem(N, seed=None):
    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]
if __name__=="__main__":
    for __number__ in argv[1:len(argv)-1]:
        NUMBER=int(__number__)
        probl=problem(NUMBER,seed=42)
        prob=tuple([tuple(a) for a in probl])
        print(f"Problem generated with NUMBER {NUMBER}")
        #start_=tuple(combinations([_ for _ in range(0,len(prob))],10))
        print([len(_) for _ in prob])
        

def searchmem__(initial_state:tuple,
    goal_test:Callable,
    state_cost:dict,
    priority_function:Callable,
    priority_function_inner:Callable):
    """This function search for a valid solution"""
    frontier = PriorityQueue()
    #parent_state.clear()
    state_cost.clear()

    state = initial_state
    #parent_state[state] = None
    state_cost[state] = 0
    seq_found=0
    state_len=0
    #maxprio=-1
    while state is not None and not goal_test(state):
        #iterate through the actions of the state itself
        for a in actionsmem(state):
            #generate the new state and its cost
            new_state=resultmem(state,a)
            new_seq=sequence_foundmem(new_state)
            len_new_state=__lentupmem__(new_state)
            #if seq_found== new_seq or len_new_state>int(NUMBER*2):
                #print(f"Quitted because seq_found {seq_found} same as {new_seq} or {len_new_state} was bigger than {NUMBER*2}")
                #continue
            #u_cost= unit_cost(new_state)
            if new_state not in state_cost and new_state not in frontier:
                #add this new state to the parent state and state cost dictionaries
                #parent_state[new_state]=state
                prio_=priority_function_inner(new_seq,len_new_state)
                #print(f"Prio di {new_state} is {prio_}, 1.5*NUMBER is {1.5*NUMBER}")
                if prio_>1.5*NUMBER:
                    print(f"Quitted because prio {prio_} was bigger than {2*NUMBER}")
                    continue
                state_cost[new_state]=state_cost[state]+1
                #push this new state into the frontier
                frontier.push(new_state,p=priority_function(prio_))
                #print(f"Pushed state {new_state}, with priority {priority_function(new_state)}")
        #if there is an element to be popped from the frontier do it and set it as the new state
        #otherwise put state as None because no element to expand is left so no solution has been found
        if frontier:
            state=frontier.pop()
            seq_found=sequence_foundmem(state)
            #prio_=priority_function(state)
            #if prio_>maxprio:
                #print(f"Popped state {state}, with priority {prio_}")
                #maxprio=prio_
        else:
            state=None
            print("Couldn't find any solution")
    #iterate through the state to get its path
    #path = list()
    #s = state
    #while s:
        #path.append(s)
        #s = parent_state[s]
    #print(f"Found a solution in {len(path):,} steps; visited {len(state_cost):,} states")
    if state:
        print(f"Found a solution in {len(state):,} steps; visited {len(state_cost):,} states")
    return state



def searchmem_(initial_state:tuple,
    goal_test:Callable,
    state_cost:dict,
    priority_function:Callable,unit_cost:Callable):
    frontier = PriorityQueue()
    #parent_state.clear()
    state_cost.clear()

    state = initial_state
    #parent_state[state] = None
    state_cost[state] = 0
    gt=goal_test(state)
    min_prio=__lentupmem__(state)
    #print(f"Lentup start {min_prio}")
    while state is not None and gt:
        for a in actionsmem_(state):
            new_state=resultmem_(state,a)
            if not goal_test(new_state) or priority_function(new_state)>min_prio:
                continue
            u_cost= unit_cost(new_state)
            if new_state not in state_cost and new_state not in frontier:
                state_cost[new_state]=state_cost[state]+u_cost
                #push this new state into the frontier
                frontier.push(new_state,p=priority_function(new_state))
                hypmin_prio=__lentupmem__(new_state)
                if hypmin_prio<min_prio:
                    min_prio=hypmin_prio
                print(f"Pushed into stack with priority {priority_function(new_state)}")
        if frontier:
            state=frontier.pop()
            print(f"Popped from stack with priority {priority_function(state)}")
            
                #print(f"New min lentup {min_prio}")
            if min_prio==NUMBER:
                    break
        else:
            break
    if state:
        print(f"Found a solution in {len(state):,} steps; visited {len(state_cost):,} states")
    return state


#def resultmem_(state,action):
    """This function returns a new state starting from one and it and it adds a list(action)
    to its data"""
    #generate a state starting from last one
    #lt=list(state)
    #del lt[bisect.bisect_left(lt, action)]
    #return tuple(lt)
    #add action to the state