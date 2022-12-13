### ***PROPOSED SOLUTION FOR THE FIRST TWO POINTS OF NIM***
***s301247@studenti.polito.it Mohamed Amine Hamdi***

# P1 AND P2

## Task

Develop a hard coded strategy and an evolved agent for the nim game

***

## Contributions
The code was developed stricly by me but before the final solution I discussed various other solutions with some of my collegues like Diego Gasco, Enrico Magliano, Krzyszstof Kleist, Giovanni Genna, Gabriele Cassetta.

***

## ***Proposed solution***

*For this solution I started by developing a set of hard coded rules that aims at being pretty balanced, not too overpowered and not too weak*.

*After this set of rules I tried to build an evolved agent that tries to optimize the order of these rules, I wanted to build an agent that can optimize also the parameters of there rules but I couldn't build in time a set of rules that can be really parametrized, mainly because some of them are appropriate only in a specific moment, but I plan to do it for the next delivery hopefully, so my goal is to develop an agent that can understand both the ordering of rules and the parameters that that rule should use*.

*For the evolutions I used a population of 1 and an offspring of 5, only mutation is used and survival is based purely on fitness*.

*Fitness is defined as the # of won games out of 10 against a pure random bot*.

*Because of time restrictions caused by deliveries of other projects I couldn't develop a great set of rules where each rule is not taken too many times with respect to the other ones and also I couldn't develop a fully fledged evolutionary algorithm*.

### ***Results***

| N      | Won games |
| :---        |    :----:   |
| 0 evolutions       | 4/10        |
| 5 evolutions      | 9/10     |
| 10 evolutions       | 9/10     |

***

# P3 AND P4

## Task

Develop a minmax version and a reinforcement learning version of the algorithm for the Nim game

***

## Contributions
The code was developed stricly by me but before the final solution I discussed various other solutions with some of my collegues like Diego Gasco, Enrico Magliano, Krzyszstof Kleist, Giovanni Genna, Gabriele Cassetta.

***

## ***Proposed solution***

*Because of the same time restrictions of the other two points I couldn't develop a complete version of the code I wanted to build, for example I developed a minmax agent that calculates everything at the first move and keeps all in memory without using any pruning or smarter choice, in the next weeks hopefully I will be able to change this behaviour, rigth now it is working in the intended way but for nim with a huge number of possibilities the computational capability is huge*.

*For the reinforcement learning instead I developed the provided code before the lectures about it with just the idea of a reward, so also here I want to do some changes, like giving different rewards per move in the same game, for now I developed an agent that plays a game and at the end of it through a backpropagation it gives rewards to moves used, each state has a fixed # of moves, this was to not require much memory for our program, in fact every time a significant # of moves are bad according to our scores we refresh them searching for **new** moves, my idea was to give these new moves more probability to be picked and not be useless, I tried to do it but the result was not the expected one so I left that code commented*.

*So in the next weeks I hope to be able to deliver a more complete version of both algorithms*.

### ***Results***

| Against      | Won games |
| :---        |    :----:   |
| Gabriele       | 970/1000       |
| Pure random      | 600/1000  |
| Optimal agent       | 0/1000     |

***