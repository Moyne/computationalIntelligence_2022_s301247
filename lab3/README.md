### ***PROPOSED SOLUTION FOR THE FIRST TWO POINTS OF NIM***
***s301247@studenti.polito.it Mohamed Amine Hamdi***

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