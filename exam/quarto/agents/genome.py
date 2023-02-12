import random
import copy
import quarto
from .rule import Rule
import agents.quartolib as quartolib
from .actionslib import random_choose,random_place
import numpy as np
NUMROWS=4
NUMCOLUMNS=4
NEWLINE="\n"
class RandomPlayer(quarto.Player):
    """Random player"""

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)

    def choose_piece(self) -> int:
        return random.randint(0, 15)

    def place_piece(self) -> tuple[int, int]:
        return random.randint(0, 3), random.randint(0, 3)

class Genome(quarto.Player):
    def __init__(self,quarto: quarto.Quarto,choose_piece_rules=None,place_piece_rules=None) -> None:
        super().__init__(quarto)
        self.quarto=quarto
        self.choose_piece_rules=copy.deepcopy(choose_piece_rules) if choose_piece_rules is not None else [Rule(True,None) for _ in range(random.randint(10,15))]
        self.place_piece_rules=copy.deepcopy(place_piece_rules) if place_piece_rules is not None else [Rule(False,None) for _ in range(random.randint(10,15))]
        self.evaluating_choose_piece_rules=self.choose_piece_rules
        self.evaluating_place_piece_rules=self.place_piece_rules
        self.fitness=0
        self.evaluating=False
        self.evaluating_genome=False
        self.random_pick=0
        #print(f'\tChoose piece rules :\n {NEWLINE.join([str(rule) for rule in self.choose_piece_rules])} \n\t;Place piece rules:\n {NEWLINE.join([str(rule) for rule in self.place_piece_rules])}')
        if choose_piece_rules is None:
            self.evaluate_fitness()
            print(f'Generated genome with fitness {self.fitness}')
    
    def set_quarto(self,quarto):
        self.quarto=quarto
        for rule in self.choose_piece_rules+self.place_piece_rules:
            rule.set_quarto(self.quarto)

    def choose_piece(self):
        board=self.quarto.get_board_status()
        placed_pieces=quartolib.get_placed_pieces(board)
        possible_pieces=[_ for _ in range(NUMROWS*NUMCOLUMNS) if _ not in placed_pieces]
        rules_to_use=self.evaluating_choose_piece_rules if self.evaluating else self.choose_piece_rules
        for rule in rules_to_use:
            val=rule.evaluate()
            #print(f'Evaluated rule {rule} with val {val}')
            if val:
                act=rule.action()
                if act in possible_pieces:
                    if self.evaluating:
                        rule.evaluated(True,True)
                    return act
                else:
                    if self.evaluating:
                        rule.evaluated(True,False)
            else:
                if self.evaluating:
                    rule.evaluated(False,False)
        if self.evaluating_genome:
            self.random_pick+=1
        return random_choose(self.quarto)

    def place_piece(self):
        board=self.quarto.get_board_status()
        possible_placements=[(a[1],a[0]) for a in np.argwhere(board==-1).tolist()]
        rules_to_use=self.evaluating_place_piece_rules if self.evaluating else self.place_piece_rules
        for rule in rules_to_use:
            val=rule.evaluate()
            #print(f'Evaluated rule {rule} with val {val}')
            if val:
                act=rule.action()
                #print(f'Possible placements {possible_placements} act {act}')
                if act in possible_placements:
                    if self.evaluating:
                        rule.evaluated(True,True)
                    return act
                else:
                    if self.evaluating:
                        rule.evaluated(True,False)
            else:
                if self.evaluating:
                    rule.evaluated(False,False)
        if self.evaluating_genome:
            self.random_pick+=1
        return random_place(self.quarto)
    
    def mutate(self):
        self.choose_piece_rules[random.randint(0,len(self.choose_piece_rules)-1)].mutate()
        self.place_piece_rules[random.randint(0,len(self.place_piece_rules)-1)].mutate()

    

    def evaluate_fitness(self):
        #evaluate choose piece rules
        self.evaluating=True
        for i in range(len(self.choose_piece_rules)):
            #put rule as first
            self.evaluating_choose_piece_rules= [self.choose_piece_rules[i]] + self.choose_piece_rules[:i] + self.choose_piece_rules[i+1:]
            make_sense=False
            #count=0
            # run only if the rule needs to be evaluated, so if the rule is mutated, otherwise use old data
            while not make_sense and self.choose_piece_rules[i].needs_evaluation():
                #print(f'\tEvaluating choose rule #{i}')
                for _ in range(3):
                    self.choose_piece_rules[i].reset_game_stats()
                    game = quarto.Quarto()
                    playerindex=random.randint(0,1)
                    game.set_players((RandomPlayer(game), self) if playerindex==1 else (self, RandomPlayer(game)))
                    self.set_quarto(game)
                    winner = game.run()
                    #print(f'\tWon ? {winner==playerindex}')
                    self.choose_piece_rules[i].evaluate_game_rule(True if winner==playerindex else False)
                    #logging.warning(f"main: Winner: player {winner}")
                make_sense=self.choose_piece_rules[i].rule_make_sense and self.choose_piece_rules[i].action_make_sense
                #print(f'Rule choose {i} makes sense? {make_sense} , rule? {self.choose_piece_rules[i].rule_make_sense} act? {self.choose_piece_rules[i].action_make_sense}')
                if not make_sense:
                    self.choose_piece_rules[i].mutate(self.choose_piece_rules[i].rule_make_sense,self.choose_piece_rules[i].action_make_sense)
                #count+=1
                #if count==10:

            
        self.evaluating_choose_piece_rules=self.choose_piece_rules

        for i in range(len(self.place_piece_rules)):
            #put rule as first
            self.evaluating_place_piece_rules= [self.place_piece_rules[i]] + self.place_piece_rules[:i] + self.place_piece_rules[i+1:]
            make_sense=False
            # run only if the rule needs to be evaluated, so if the rule is mutated, otherwise use old data
            while not make_sense and self.place_piece_rules[i].needs_evaluation():
                #print(f'\tEvaluating place rule #{i}')
                for _ in range(3):
                    self.place_piece_rules[i].reset_game_stats()
                    game = quarto.Quarto()
                    playerindex=random.randint(0,1)
                    game.set_players((RandomPlayer(game), self) if playerindex==1 else (self, RandomPlayer(game)))
                    self.set_quarto(game)
                    winner = game.run()
                    #print(f'\tWon ? {winner==playerindex}')
                    self.place_piece_rules[i].evaluate_game_rule(True if winner==playerindex else False)
                    #logging.warning(f"main: Winner: player {winner}")
                make_sense=self.place_piece_rules[i].rule_make_sense and self.place_piece_rules[i].action_make_sense
                #print(f'Rule place {i} makes sense? {make_sense} , rule? {self.place_piece_rules[i].rule_make_sense} act? {self.place_piece_rules[i].action_make_sense}')
                if not make_sense:
                    self.place_piece_rules[i].mutate(self.place_piece_rules[i].rule_make_sense,self.place_piece_rules[i].action_make_sense)
            
        self.evaluating_place_piece_rules=self.place_piece_rules

        self.evaluating=False
        #updated priority of rules, checking first the rules less probable to be true
        self.choose_piece_rules=sorted(self.choose_piece_rules,key=lambda a: a.rule_true)
        self.place_piece_rules=sorted(self.place_piece_rules,key=lambda a: a.rule_true)
        #now evaluate whole genome
        self.evaluating_genome=True
        wins=0
        #print(f'\tNow evaluating whole genome')
        for _ in range(100):
            game = quarto.Quarto()
            playerindex=random.randint(0,1)
            game.set_players((RandomPlayer(game), self) if playerindex==1 else (self, RandomPlayer(game)))
            self.set_quarto(game)
            winner = game.run()
            #print(f'\tWon ? {winner==playerindex}')
            if winner==playerindex:
                wins+=1
        self.fitness= wins - self.random_pick
        #print(f'Won in total {wins} games, total of {self.random_pick} random picks so fitness is {self.fitness}')


    def __str__(self):
        return f'\tChoose piece rules :\n{NEWLINE.join([str(rule) for rule in self.choose_piece_rules])} \n\t; Place piece rules :\n{NEWLINE.join([str(rule) for rule in self.place_piece_rules])}'
