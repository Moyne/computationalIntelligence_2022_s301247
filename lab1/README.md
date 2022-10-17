### ****PROPOSED SOLUTION FOR THE SET COVERING PROBLEM**** ###
***s301247@studenti.polito.it Mohamed Amine Hamdi***

#### *note: states visited are counted as all the elements added to the frontier, not the ones popped from it*

This solution is a mix between a beam search, A* and best first algorithms.

The code alone can be found in ***set_covering_solution.py***

This is because to keep track of states to visit next we have a priority queue where optimal states are favorited because the priority function calculates the amount of elements seen and take the unary minus of it and add it to the size of the state, so if a state is optimal it will have priority function 0 and will get chosen as the first candidate, so we aren't going breadth first because if a state is horrible we may never reach the point where the priority queue pops it.

After this point I chose a metric of where to stop at each level, this is done because otherwise the problem will explode too much space wise, so to contain it I chose the ***metric*** (0,2,5,10,15,...,etc.), this metric is used so if a state gets a priority of 20 and it is on the third level of the tree we will cut it immediately because 20>METRIC[3] so 20>10, knowing this we can guarantee with a really really high confidence that continuing with that state and expanding it wouldn't generate a good solution, so instead we only expand states that are in the range of our metric, this mechanism let us save a lot of precious memory and generate with a good confidence a solution that we can say is optimal in a reasonable amount of time also for big Ns(20 mins for N=50 getting the optimal weight 65) and keeping the memory down without exploding it.

The metric seems to be working not too badly but for sure it could be better, I chose this starting testing other solutions(can be checked on the last part of this notebook or in ***other_solutions.py***) and noticing how the optimal solution was growing, so for example the optimal solution with ***N=20*** had weight ***23*** while for ***N=40*** it had weight ***54***, so I tried to approximize how much loss for each level we have usually before finding the optimal solution, obviously this metric works better in some cases than others but for my testing it can generate the optimal solution without exploding in space too much.

***

The states are represented as a ***tuple of tuples***, this is done because tuples are immutables like our states and also this gives us theoretically a slight edge on performance with respect to lists, I used tuples also because I wanted to keep track of duplicate states and to do so I needed a hashable data structure without the need to write a hash function for a data structure, the other go to data structure was a set but it lacked this part.

A module used all over my implementations is the bisect one, this is because my states are tuples that are always ordered, so two states that have the same sets can be skipped because just doing a simple ***if in frontier or in state_cost*** will get them because the hash will be equivalent, this module helps me inserting in order because it divides the tuple in two and searches for the position recursevely.

Another piece used was the PriorityQueue version of prof.Squillero.

(In other solutions I used as a state a tuple of numbers representing the sets of integers picked inyo this state, this gave the program a small improvement of memory, but after the use of the metric the space explosion was resolved and so memory was not an issue so I got back to the first implementation of states)

***

## Task

Given a number $N$ and some lists of integers $P = (L_0, L_1, L_2, ..., L_n)$, 
determine is possible $S = (L_{s_0}, L_{s_1}, L_{s_2}, ..., L_{s_n})$
such that each number between $0$ and $N-1$ appears in at least one list

$$\forall n \in [0, N-1] \ \exists i : n \in L_{s_i}$$

and that the total numbers of elements in all $L_{s_i}$ is minimum. 

***

## Contributions
The code was developed stricly by me but before the final solution I discussed various other solutions with some of my collegues like Diego Gasco, Enrico Magliano, Krzyszstof Kleist, Giovanni Genna, Gabriele Casetti.

***Set covering problem data***

## Results proposed solution (other solutions have interesting data as well, especially with width limitation)

#### *note: states visited are counted as all the elements added to the frontier, not the ones popped from it*

Results with N:

- 5:
- - Found a solution in 6 steps; visited 41 states with weight 5 in 0.0002668999950401485 secs

- 10:
- - Found a solution in 5 steps; visited 1,549 states with weigth 10 in 0.006042899971362203 secs

- 20:
- - Found a solution in 6 steps; visited 38,129 states with weight 23 in 0.30784149997634813 secs

- 40:
- - Found a solution in 6 steps; visited 520,162 states with weight 54 in 23.404796299990267 secs

- 50:
- - Found a solution in 6 steps; visited 4,877,807 states states with weight 54 in 1282.1018204999855 secs
- - Path [((),), ((), (1, 2, 40, 47, 16, 22, 23, 24, 30)), ((), (1, 2, 40, 47, 16, 22, 23, 24, 30), (32, 34, 3, 36, 38, 6, 8, 41, 10, 43, 45, 48, 17, 18, 20, 26)), ((), (1, 2, 40, 47, 16, 22, 23, 24, 30), (32, 34, 3, 36, 38, 6, 8, 41, 10, 43, 45, 48, 17, 18, 20, 26), (35, 4, 37, 42, 12, 13, 46, 48, 21, 30)), ((), (0, 33, 3, 35, 6, 7, 41, 9, 11, 44, 14, 15, 48, 49, 25, 27, 29, 31), (1, 2, 40, 47, 16, 22, 23, 24, 30), (32, 34, 3, 36, 38, 6, 8, 41, 10, 43, 45, 48, 17, 18, 20, 26), (35, 4, 37, 42, 12, 13, 46, 48, 21, 30)), ((), (0, 33, 3, 35, 6, 7, 41, 9, 11, 44, 14, 15, 48, 49, 25, 27, 29, 31), (1, 2, 40, 47, 16, 22, 23, 24, 30), (2, 3, 4, 5, 38, 39, 41, 18, 19, 23, 28, 29), (32, 34, 3, 36, 38, 6, 8, 41, 10, 43, 45, 48, 17, 18, 20, 26), (35, 4, 37, 42, 12, 13, 46, 48, 21, 30))]
- - Solution ((), (0, 33, 3, 35, 6, 7, 41, 9, 11, 44, 14, 15, 48, 49, 25, 27, 29, 31), (1, 2, 40, 47, 16, 22, 23, 24, 30), (2, 3, 4, 5, 38, 39, 41, 18, 19, 23, 28, 29), (32, 34, 3, 36, 38, 6, 8, 41, 10, 43, 45, 48, 17, 18, 20, 26), (35, 4, 37, 42, 12, 13, 46, 48, 21, 30)) with weight 65

For 100 and successive iterations I didn't have the time to see if the metric helps or if it needs to be tuned in a better way.


***

***

## Results other solutions

Solutions with other implementations, can see immediately the huge difference in the N=40 example where the proposed solution takes less time and find the solution in 6,85% of the states used by the other solutions.

***Anyway we can see by the solutions with 50 that the width limitations can help really really a lot without causing much loss in the optimality of the solution, so we can evince that an implementation that can guarantee limitation in both width and metrics can be really effective.***

#### *note: states visited are counted as all the elements added to the frontier, not the ones popped from it*

- 5:
- - problem : ((0,), (1,), (0,), (4,), (0,), (1,), (4,), (4,), (4,), (1, 3), (0, 1), (2,), (1,), (0,), (0, 2), (2, 4), (3,), (3,), (4,), (2, 4), (0,), (1,), (0, 1), (3,), (2, 3))
- - Found a solution in 6 steps; visited 41 states in 0.0004899000050500035 secs
- - Path [((),), ((), (0,)), ((), (0,), (1,)), ((), (0,), (1,), (2,)), ((), (0,), (1,), (2,), (3,)), ((), (0,), (1,), (2,), (3,), (4,))] Solution ((), (0,), (1,), (2,), (3,), (4,)) with weight 5

***

- 10:
- - ((0, 4), (1, 2, 3), (9, 6), (0, 1), (8, 9, 3), (8, 3), (0, 3, 4, 7, 9), (4, 5, 6), (1, 3, 5), (1, 6), (0, 9, 4, 5), (8, 1, 6), (9, 3, 5), (0, 3), (1, 3, 6), (2, 5, 7), (1, 3, 4, 9), (8, 2, 3), (3, 4, 5, 6, 8), (0, 3), (1, 3, 4, 6), (3, 6, 7), (2, 3, 4), (9, 6), (8, 2, 3, 7), (0, 1), (9, 2, 6), (6,), (8, 0, 4, 1), (1, 4, 5, 6), (0, 4, 7), (8, 1, 4), (2, 5), (9, 5), (0, 1, 3, 4, 5), (9, 3), (1, 7), (8, 2), (8, 2, 7), (8, 9, 3, 6), (4, 5, 6), (8, 1, 3, 7), (0, 5), (0, 9, 3), (0, 3), (0, 5), (8, 3), (8, 2, 3, 7), (1, 3, 6, 7), (5, 6))
- - Found a solution in 5 steps; visited 1,549 states in 0.00596939999377355 secs
- - Path [((),), ((), (0, 1)), ((), (0, 1), (4, 5, 6)), ((), (0, 1), (4, 5, 6), (8, 2, 7)), ((), (0, 1), (4, 5, 6), (8, 2, 7), (9, 3))] Solution ((), (0, 1), (4, 5, 6), (8, 2, 7), (9, 3)) with weight 10

***

- 20:
- - ((8, 4, 7), (0, 1, 2, 3, 6, 13, 17, 18), (0, 6, 16, 17, 19), (0, 5, 7, 8, 13, 14, 17, 18), (2, 3, 4, 6, 8, 10), (1, 3, 8, 11, 14, 19), (2, 3, 9, 11, 12, 17, 18, 19), (1, 2, 9, 7), (3, 5, 6, 7, 8, 11, 12, 14), (2, 5, 7, 8, 12, 14, 17, 19), (17, 10, 1, 7), (2, 6, 8, 10, 12, 15, 18), (4, 7, 8, 14, 17, 18), (4, 7, 11, 12, 15, 16, 18), (1, 3, 4, 5), (2, 8, 12, 13, 14, 16, 17, 19), (0, 3, 5, 8, 9, 10, 13, 14, 17), (8, 16, 5), (16, 9, 19, 6), (0, 5, 11, 16, 17), (0, 1, 3, 7, 9, 10, 11, 15), (18, 2, 15), (4, 5, 8, 13, 15, 16, 17, 19), (6, 9, 11, 12, 17), (2, 3, 7, 10, 14, 16), (17, 18, 7), (0, 1, 2, 7), (16, 10, 2, 7), (4, 6, 15, 17, 18), (3, 6, 7, 13, 15), (1, 3, 13, 14), (3, 6, 7, 10, 14, 17), (5, 7, 8, 13, 14), (0, 1, 2, 3, 5, 7, 14, 17))
- - Found a solution in 6 steps; visited 40,109 states in 0.1827651999774389 secs
- - Path [((),), ((), (0, 5, 11, 16, 17)), ((), (0, 5, 11, 16, 17), (1, 3, 13, 14)), ((), (0, 5, 11, 16, 17), (1, 3, 13, 14), (2, 6, 8, 10, 12, 15, 18)), ((), (0, 5, 11, 16, 17), (1, 3, 13, 14), (2, 6, 8, 10, 12, 15, 18), (8, 4, 7)), ((), (0, 5, 11, 16, 17), (1, 3, 13, 14), (2, 6, 8, 10, 12, 15, 18), (8, 4, 7), (16, 9, 19, 6))] Solution ((), (0, 5, 11, 16, 17), (1, 3, 13, 14), (2, 6, 8, 10, 12, 15, 18), (8, 4, 7), (16, 9, 19, 6)) with weight 23

***

- 40:
- - ((34, 5, 6, 37, 8, 14, 15, 17), (32, 1, 2, 35, 34, 5, 38, 12, 13, 14, 26, 28), (0, 5, 6, 38, 9, 10, 13, 16, 17, 21, 22, 24, 27), ... , (32, 35, 4, 38, 8, 9, 12, 15, 17, 24, 26, 29, 30), (32, 0, 34, 37, 9, 17, 18, 19, 22, 28, 30, 31))
- - Found a solution in 6 steps; visited 7,586,233 states in 65.18534940003883 secs
- - Solution ((), (0, 32, 34, 33, 6, 38, 9, 10, 11, 12, 16, 19, 23), (1, 3, 35, 39, 8, 7, 13, 17, 18, 28, 31), (2, 4, 5, 38, 7, 36, 37, 39, 11, 15, 25, 26), (2, 35, 3, 14, 17, 20, 24, 29), (33, 35, 37, 17, 21, 22, 23, 27, 29, 30)) with weight 54

***

- 50 WITH LIMITATED ALGORITHM WITH 25% AS WIDTH PARAMETER:
- - ((1, 34, 5, 6, 37, 8, 43, 14, 15, 47, 17), (0, 1, 2, 5, 10, 12, 13, 14, 17, 26, 28, 32, 34, 35, 37, 38, 41, 44, 45, 48), (2, 34, 35, 5, 6, 38, 7, 9, 13, 46, 48, 17, 16, 18, 21, 22, 24, 29), (2, 4, 5, 6, 10, 12, 13, 14, 17, 18, 22, 23, 24, 29, 36, 40, 42, 45, 49), (34, 35, 4, 38, 40, 41, 10, 43, 44, 46, 15, 14, 17, 24, 29), ... , (0, 3, 5, 6, 10, 13, 14, 16, 19, 23, 25, 27, 40, 41, 42, 44, 45, 46, 48), (0, 4, 5, 6, 7, 8, 14, 20, 21, 23, 24, 27, 28, 30, 33, 37, 43, 44, 46), (0, 33, 4, 36, 39, 8, 41, 9, 43, 10, 13, 46, 48, 49, 22, 24, 28))
- - Found a solution in 6 steps; visited 3,938,464 states in 104.93217300000833 secs
- - Solution ((), (0, 1, 2, 5, 10, 12, 13, 14, 17, 26, 28, 32, 34, 35, 37, 38, 41, 44, 45, 48), (0, 3, 36, 4, 6, 7, 40, 9, 11, 43, 16, 18, 19, 21, 25, 28, 30, 31), (2, 6, 8, 42, 43, 13, 15, 49, 19, 22, 23, 27), (32, 33, 35, 38, 39, 42, 46, 48, 20, 27, 28, 29), (34, 38, 47, 48, 19, 22, 24, 26)) with weight 70

***

- 50 WITH LIMITATED ALGORITHM WITH 15% AS WIDTH PARAMETER:
- - Found a solution in 7 steps; visited 1,539,982 states in 69.73105619999114 secs
- - Solution ((), (0, 33, 34, 35, 32, 7, 41, 10, 43, 46, 16, 48, 17, 49, 18, 21, 27, 29), (1, 2, 6, 39, 9, 10, 11, 42, 44, 14, 15, 47, 17, 21, 24, 26, 30), (1, 3, 38, 7, 15, 19, 20, 23, 31), (2, 36, 37, 38, 7, 39, 5, 43, 15, 25, 26), (4, 36, 39, 40, 12, 45, 15, 49, 26, 29, 30), (32, 34, 4, 8, 10, 13, 15, 16, 18, 22, 23, 28)) with weight 78

Here we can see how cutting the width doesn't destroy our solution, with 25% width we still can get 70, 70/65 so the bloat is not huge, also with 15% we don't get much bloat, with 50 we can't run the algorithm without width limitation because of how memory effective it is, while with the proposed solution we get pretty much costant in the space world

***

Let's try with N=100 and a really low width value, 5% (otherwise the problem would be too big)

- 100 WITH THE STANDARD WITH 5% AS WIDTH PARAMETER:
- - Found a solution in 8 steps; visited 2,701,485 states in 573.1298935000086 secs
- - Solution ((), (0, 2, 28, 34, 38, 45, 48, 49, 53, 55, 61, 62, 68, 69, 73, 74, 77, 89, 94, 95, 96, 97, 98), (3, 4, 8, 13, 19, 20, 22, 24, 25, 28, 29, 30, 31, 34, 35, 39, 42, 44, 48, 51, 52, 58, 60, 65, 71, 79, 82, 84, 85, 89, 94, 95, 98), (3, 6, 10, 16, 17, 21, 23, 27, 33, 35, 41, 43, 48, 49, 50, 51, 54, 58, 59, 68, 72, 75, 79, 82, 84, 85, 86, 92, 97), (5, 8, 10, 12, 15, 20, 24, 26, 29, 33, 34, 35, 37, 45, 46, 47, 48, 58, 68, 70, 73, 79, 80, 81, 82, 84, 85, 87, 89, 90, 93, 98), (7, 8, 9, 10, 17, 19, 20, 27, 29, 30, 31, 33, 34, 35, 36, 40, 42, 49, 52, 53, 54, 56, 57, 59, 60, 62, 64, 66, 69, 70, 78, 80, 81, 88, 90, 91, 92, 95, 96, 98, 99), (8, 11, 17, 18, 27, 28, 31, 33, 34, 40, 46, 50, 51, 54, 58, 63, 65, 68, 71, 72, 74, 82, 83, 91, 95, 96), (32, 1, 67, 68, 70, 8, 76, 14, 80, 49, 48, 19, 20, 54, 87, 59, 92)) with weight 201

The result has weight 201, it is not bad comparing other greedy solutions and the fact that it took only 573 secs and with 5% as width
