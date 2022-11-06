### ****PROPOSED SOLUTION FOR THE SET COVERING PROBLEM GA VERSION**** ###
***s301247@studenti.polito.it Mohamed Amine Hamdi***

*This solution uses a uniform crossover by default, and a wheel roulette for the selection of the parents, the algorithm generates for NUM_GENERATIONS a set of OFFSPRING_SIZE offspring, to do so 2 options are available, for 30% of the time a mutation of a parent taken from the population is made, otherwise two parents are selected and crossed over, after this step if we don't have a valid solution but the fitness is still pretty good we try to add to that genome a set until we either reach a bad indivual or we have a valid solution.*

*Finally we check if the new individual is new or if it's a duplicate, in the last case we try to mutate it, finally if at the end of this process we have a valid solution we add it to the offspring set.*

*The fitness function proposed is setupped so an optimal solution will have 2 x PROBLEM_SIZE as the fitness, and it tries to give a lot of weigth to repetitions into a genome, so we calculate it as 2*(# of covered elements) - total # of repetitions.*

*Lastly in the code we can find various heuristics to try to cut the searching space, in fact we calculate mutations starting from the ceiling of (-(-2 x PROBLEM_SIZE + f)) * PROBLEM_LEN / (10 x MAXREPETITIONS), this is a heuristic designed to remove a lot of sets in the beginning because we have a lot of bad solutions at the beginning because they have too many sets taken, this can be seen as a form of exploration, and then at the end when we try to apply exploitation this heuristic should have a ceiling of 1, so we can do swapping as our mutation.*

*This algorithm works pretty well but a limitation is on the speed because requiring 100 new unique valide solutions at each generations is quite expensive, and also trying to turn an invalid solution into a valid one can be expensive as well.*

***

## Task

Given a number $N$ and some lists of integers $P = (L_0, L_1, L_2, ..., L_n)$, 
determine is possible $S = (L_{s_0}, L_{s_1}, L_{s_2}, ..., L_{s_n})$
such that each number between $0$ and $N-1$ appears in at least one list

$$\forall n \in [0, N-1] \ \exists i : n \in L_{s_i}$$

and that the total numbers of elements in all $L_{s_i}$ is minimum. 

***

## Contributions
The code was developed stricly by me but before the final solution I discussed various other solutions with some of my collegues like Diego Gasco, Enrico Magliano, Krzyszstof Kleist, Giovanni Genna, Gabriele Cassetta.

***

## Set covering problem data

Results with N:

| N      | Weigth | Population     | Offspring |
| :---        |    :----:   |          ---: |     ---: |
| 50      | 66       |   10   |     100 |
| 100   | 162        |   10    |  100 |
| 500   | 1388       | 10      | 100 |
| 1000  | 3504       |  10     | 100 |