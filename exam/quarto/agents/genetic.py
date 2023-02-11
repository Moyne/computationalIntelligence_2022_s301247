import logging
import random
import quarto
import numpy as np
from scipy.stats import binom
import pickle
from .genome import Genome

class GeneticProgramming:
    def __init__(self) -> None:
        self.__POPULATION_SIZE__=5
        self.__OFFSPRING_SIZE__=20
        self.population=[Genome(None) for _ in range(self.__POPULATION_SIZE__)]
        self.population=sorted(self.population,key=lambda a: a.fitness,reverse=True)
        self.WEIGHTS_ROULETTE=[binom.pmf(k=_,n=self.__POPULATION_SIZE__-1,p=1/self.__POPULATION_SIZE__) for _ in range(self.__POPULATION_SIZE__)]

    def select_parent(self,k=2,weigths=None):
        # Using a wheel roulette TO SELECT K PARENTS, THIS IS WITHOUT REPLACEMENT, SO THE PARENT CAN'T BE TAKEN MORE THAN ONCE
        # IN A SINGLE CALL
        return [self.population[ind] for ind in np.random.choice(range(self.__POPULATION_SIZE__),k,p=self.WEIGHTS_ROULETTE if weigths is None else weigths,replace=False )]


    def cross_oversplit(self,genome1,genome2):
        """One point split crossover"""
        gen_choose,gen_place= [len(gen.choose_piece_rules) for gen in [genome1,genome2]], [len(gen.place_piece_rules) for gen in [genome1,genome2]]
        index_min_choose,index_min_place=gen_choose.index(min(gen_choose)),gen_place.index(min(gen_place))
        point_choose,point_place = random.randint(0,min(gen_choose)-1),random.randint(0,min(gen_place)-1)
        return [genome1,genome2][index_min_choose].choose_piece_rules[:point_choose] + [genome1,genome2][1-index_min_choose].choose_piece_rules[point_choose:], [genome1,genome2][index_min_place].place_piece_rules[:point_place] + [genome1,genome2][1-index_min_place].place_piece_rules[point_place:]

    def evolve(self,iterations):
        offspring=[]
        print(f'Population at the beginning is {self.population_stats()}')
        for i in range(iterations):
            minfit,maxfit=min([gen.fitness for gen in self.population]),max([gen.fitness for gen in self.population])
            weigths=[-minfit+self.population[_].fitness+1 for _ in range(self.__POPULATION_SIZE__)]
            weigths=[_/sum(weigths) for _ in weigths]
            for o in range(self.__OFFSPRING_SIZE__):
                #always mutate
                cross=True
                if random.random()<2:
                    cross=False
                    parent=self.select_parent(k=1,weigths=weigths)[0]
                    off=Genome(parent.quarto,parent.choose_piece_rules,parent.place_piece_rules)
                    off.mutate()
                else:
                    parents= self.select_parent(k=2,weigths=weigths)
                    choose_rules,place_rules=self.cross_oversplit(parents[0],parents[1])
                    off=Genome(parents[0].quarto,choose_rules,place_rules)
                off.evaluate_fitness()
                offspring.append(off)
                #print(f'Genome {o} of gen {i} was made by {"crossover" if cross else "mutation"} and has fitness {off.fitness}')
            self.population=sorted(self.population+offspring,key=lambda a: a.fitness,reverse=True)[:self.__POPULATION_SIZE__]
            offspring=[]
            print(f'Population after {i} gens is {self.population_stats()}')

    def population_stats(self):
        return [(i,h.fitness) for i,h in enumerate(self.population)]


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

    def place_piece(self) -> tuple[int, int]:
        return self.player.place_piece()