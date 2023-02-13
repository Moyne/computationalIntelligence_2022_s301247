import logging
import random
import quarto
import numpy as np
from scipy.stats import binom
import dill as pickle
from .genome import Genome,generate_rules,MINRULES,MAXRULES

class GeneticProgramming:
    def __init__(self) -> None:
        self.__POPULATION_SIZE__=5
        self.__OFFSPRING_SIZE__=30
        print(f'Generating initial population ...')
        self.population=[Genome(None) for _ in range(self.__POPULATION_SIZE__)]
        self.population=sorted(self.population,key=lambda a: a.fitness,reverse=True)[:self.__POPULATION_SIZE__]
        self.WEIGHTS_ROULETTE=[binom.pmf(k=_,n=self.__POPULATION_SIZE__-1,p=1/self.__POPULATION_SIZE__) for _ in range(self.__POPULATION_SIZE__)]

    def select_parent(self,k=2,weigths=None):
        # Using a wheel roulette TO SELECT K PARENTS, THIS IS WITHOUT REPLACEMENT, SO THE PARENT CAN'T BE TAKEN MORE THAN ONCE
        # IN A SINGLE CALL
        return [self.population[ind] for ind in np.random.choice(range(self.__POPULATION_SIZE__),k,p=self.WEIGHTS_ROULETTE if weigths is None else weigths,replace=False )]


    def cross_oversplit(self,genome1: Genome,genome2: Genome):
        """One point split crossover"""
        #gen_choose,gen_place= [len(gen.choose_piece_rules) for gen in [genome1,genome2]], [len(gen.place_piece_rules) for gen in [genome1,genome2]]
        #index_min_choose,index_min_place=gen_choose.index(min(gen_choose)),gen_place.index(min(gen_place))
        #point_choose,point_place = random.randint(0,min(gen_choose)-1),random.randint(0,min(gen_place)-1)
        c_rules=genome1.choose_piece_rules+genome2.choose_piece_rules
        p_rules=genome1.place_piece_rules+genome2.place_piece_rules
        random.shuffle(c_rules)
        random.shuffle(p_rules)
        #avg_c_rules,avg_p_rules=len(c_rules)//2,len(p_rules)//2
        #num_c_rules,num_p_rules=random.randint(avg_c_rules-4 if avg_c_rules-4>0 else 1,avg_c_rules+4 if avg_c_rules+4<len(c_rules) else len(c_rules)),random.randint(avg_p_rules-4 if avg_p_rules-4>0 else 1,avg_p_rules+4 if avg_p_rules+4<len(p_rules) else len(p_rules))
        return c_rules[:random.randint(MINRULES,MAXRULES)],p_rules[:random.randint(MINRULES,MAXRULES)]
        #return [genome1,genome2][index_min_choose].choose_piece_rules[:point_choose] + [genome1,genome2][1-index_min_choose].choose_piece_rules[point_choose:], [genome1,genome2][index_min_place].place_piece_rules[:point_place] + [genome1,genome2][1-index_min_place].place_piece_rules[point_place:]

    def cross_oversplit_rules(self,genome: Genome,new_c_rules,new_p_rules):
        """One point split crossover"""
        c_rules=genome.choose_piece_rules+new_c_rules
        random.shuffle(c_rules)
        p_rules=genome.place_piece_rules+new_p_rules
        random.shuffle(p_rules)
        #avg_c_rules,avg_p_rules=len(c_rules)//2,len(p_rules)//2
        #num_c_rules,num_p_rules=random.randint(avg_c_rules-4 if avg_c_rules-4>0 else 1,avg_c_rules+4 if avg_c_rules+4<len(c_rules) else len(c_rules)),random.randint(avg_p_rules-4 if avg_p_rules-4>0 else 1,avg_p_rules+4 if avg_p_rules+4<len(p_rules) else len(p_rules))
        return c_rules[:random.randint(MINRULES,MAXRULES)],p_rules[:random.randint(MINRULES,MAXRULES)]


    def evolve(self,iterations):
        offspring=[]
        print(f'Population at the beginning is {self.population_stats()}')
        for i in range(iterations):
            minfit,maxfit=min([gen.fitness for gen in self.population]),max([gen.fitness for gen in self.population])
            weigths=[-minfit+self.population[_].fitness+1 for _ in range(self.__POPULATION_SIZE__)]
            weigths=[_/sum(weigths) for _ in weigths]
            for o in range(self.__OFFSPRING_SIZE__ if i%6 else int(self.__OFFSPRING_SIZE__*0.9)):
                #always mutate
                cross=True
                if random.random()<1/3:
                    cross=False
                    parent=self.select_parent(k=1,weigths=weigths)[0]
                    off=Genome(parent.quarto,parent.choose_piece_rules,parent.place_piece_rules)
                    off.mutate()
                else:
                    parents= self.select_parent(k=2,weigths=weigths)
                    choose_rules,place_rules=self.cross_oversplit(parents[0],parents[1])
                    off=Genome(parents[0].quarto,choose_rules,place_rules)
                    #off.crossover_rules()
                off.evaluate_fitness()
                offspring.append(off)
                #print(f'Genome {o} of gen {i} was made by {"crossover" if cross else "mutation"} and has fitness {off.fitness}')
            self.population=sorted(self.population+offspring,key=lambda a: a.fitness,reverse=True)[:self.__POPULATION_SIZE__]
            if not i%6:
                print(f'Population after {i+1} gens before visitors is {self.population_stats()}')
                print(f'Visitor from out of the town are arriving')
                #choose_rules,place_rules=generate_rules()
                off_visitors=[Genome(None) for _ in range(int(0.1*self.__OFFSPRING_SIZE__))]
                #for _ in range(int(0.2*self.__OFFSPRING_SIZE__)):
                    #p=self.population[random.randint(0,self.__POPULATION_SIZE__-1)]
                    #c_rules,p_rules=self.cross_oversplit_rules(p,choose_rules,place_rules)
                    #ov=Genome(p.quarto,c_rules,p_rules)
                    #ov.crossover_rules()
                    #ov.evaluate_fitness()
                    #off_visitors.append(ov)
                print(f'Now they have meet the population they generated two kids with fitness of {[o.fitness for o in off_visitors]}')
                self.population=sorted(self.population[:self.__POPULATION_SIZE__-2]+off_visitors,key=lambda a: a.fitness,reverse=True)[:self.__POPULATION_SIZE__]
            offspring=[]
            print(f'Population after {i+1} gens is {self.population_stats()}')

    def population_stats(self):
        return [(f'fitness {h.fitness}',f'rand {h.random_pick}') for h in self.population]


    def get_best_player(self):
        return self.population[0]


            

class GeneticProg(quarto.Player):
    """Genetic Programming player"""

    def __init__(self, quarto: quarto.Quarto,best_player_file,generations) -> None:
        super().__init__(quarto)
        self.quarto=quarto
        print('Training phase ...')
        population=GeneticProgramming()
        population.evolve(generations)
        print(f'Population after {generations} gens is {population.population_stats()}')
        self.player=population.get_best_player()
        print(f'Player is\n{self.player}')
        try:
            with open(best_player_file,'wb') as file:
                pickle.dump(self.player, file,protocol=0)
        except OSError as error:
            print(f'Error while pickle saving best player {error}')
    
    def set_quarto(self,quarto):
        self.quarto=quarto
        self.player.set_quarto(self.quarto)

    def choose_piece(self) -> int:
        return self.player.choose_piece()

    def place_piece(self) -> tuple:
        return self.player.place_piece()