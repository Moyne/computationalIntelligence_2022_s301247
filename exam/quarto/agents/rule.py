import random
from .actionslib import get_choose_actions,get_place_actions
from .quartolib import get_choose_functions,get_place_functions

OPERATIONS={
    'mul': (lambda a,b: a+b if type(a)==type(b) and isinstance(a,str) else a*b),
    'not': (lambda a,b: not a),
    'or': (lambda a,b: a or b),
    'and': (lambda a,b: a and b),
    'eq': (lambda a,b: a==b),
    'ne': (lambda a,b: a!=b)
}
OPERATIONS_LIST=list(OPERATIONS.keys())
OPERATIONS_WITH_ONE_OPERAND=set(['not'])

ACTIONS_CHOOSE= get_choose_actions()
ACTIONS_PLACE= get_place_actions()
CHOOSE_FUNCTIONS=get_choose_functions()
PLACE_FUNCTIONS=get_place_functions()
CHOOSE_VALUES=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
PLACE_VALUES=[0,1,2,3,4]
POSSIBLE_CHOOSE_VALUES=[[(op,'operation') for op in OPERATIONS_LIST],[(func,'function') for func in CHOOSE_FUNCTIONS],[(val,'value') for val in CHOOSE_VALUES]]

POSSIBLE_PLACE_VALUES=[[(op,'operation') for op in OPERATIONS_LIST],[(func,'function') for func in PLACE_FUNCTIONS],[(val,'value') for val in PLACE_VALUES]]

class Node:
    def __init__(self,parent,choose_piece,quarto,value=None) -> None:
        self.parent=parent
        self.quarto=quarto
        self.choose_piece=choose_piece
        self.childs=[]
        if value is None:
            value=random.choice(POSSIBLE_CHOOSE_VALUES[random.randint(0,2)] if choose_piece else POSSIBLE_PLACE_VALUES[random.randint(0,2)])
        self.value=value[0]
        self.op=value[1]=='operation'
        self.func=value[1]=='function'
        self.val=value[1]=='value'
        #print(f'Value for node is {value} , op {self.op} func {self.func} val {self.val}')
        if self.op:
            #print(f'Need a child or two')
            self.childs.append(Node(self,self.choose_piece,self.quarto))
            if self.op not in OPERATIONS_WITH_ONE_OPERAND:
                self.childs.append(Node(self,self.choose_piece,self.quarto))
        else:
            pass
            #print(f'No need for childs')

    def mutate(self):
        if random.random()<0.5 and self.op:
            #mutate one of the childs
            self.childs[random.randint(0,len(self.childs)-1)].mutate()
        else:
            #mutate myself
            if random.random()<0.5 and self.parent is not None:
                #go full random, don't care about what type of thing I was before
                value=random.choice(POSSIBLE_CHOOSE_VALUES[random.randint(0,2)] if self.choose_piece else POSSIBLE_PLACE_VALUES[random.randint(0,2)])
                self.value=value[0]
                self.op=value[1]=='operation'
                self.func=value[1]=='function'
                self.val=value[1]=='value'
                if self.op:
                    #print(f'Need a child or two')
                    if random.random()<0.5 and len(self.childs)>0:
                        #keep old childs
                        if self.op in OPERATIONS_WITH_ONE_OPERAND and len(self.childs)==2:
                            #remove one of the two childs in case
                            self.childs.pop(random.randint(0,len(self.childs)-1))
                    else:
                        self.childs=[]
                        self.childs.append(Node(self,self.choose_piece,self.quarto))
                        if self.op not in OPERATIONS_WITH_ONE_OPERAND:
                            self.childs.append(Node(self,self.choose_piece,self.quarto))
                else:
                    self.childs=[]
            else:
                #keep my old type
                value=random.choice(POSSIBLE_CHOOSE_VALUES[0 if self.op else 1 if self.func else 2] if self.choose_piece else POSSIBLE_PLACE_VALUES[0 if self.op else 1 if self.func else 2])
                self.value=value[0]
                self.op=value[1]=='operation'
                self.func=value[1]=='function'
                self.val=value[1]=='value'
                if self.op:
                    #print(f'Need a child or two')
                    if random.random()<0.5 and len(self.childs)>0:
                        #keep old childs
                        if self.op in OPERATIONS_WITH_ONE_OPERAND and len(self.childs)==2:
                            #remove one of the two childs in case
                            self.childs.pop(random.randint(0,len(self.childs)-1))
                    else:
                        self.childs=[]
                        self.childs.append(Node(self,self.choose_piece,self.quarto))
                        if self.op not in OPERATIONS_WITH_ONE_OPERAND:
                            self.childs.append(Node(self,self.choose_piece,self.quarto))
                else:
                    self.childs=[]

            

    def set_quarto(self,quarto):
        self.quarto=quarto
        if self.op:
            for child in self.childs:
                child.set_quarto(self.quarto)

    def eval(self):
        if not self.op:
            if self.val:
                return self.value
            else:
                return self.value(self.quarto)
        else:
            evals=[child.eval() for child in self.childs] + [None,None]
            left_val,rigth_val=evals[0],evals[1]
            #print(f'Left val {left_val} --- rigth val {rigth_val}')
            return OPERATIONS[self.value](left_val,rigth_val)

    def __str__(self):
        if self.op:
            if self.op not in OPERATIONS_WITH_ONE_OPERAND:
                return f'({str(self.childs[0])}) {self.value} ({str(self.childs[1])})'
            else:
                return f'{self.value} ({str(self.childs[0])})'

        elif self.func:
            return f'{self.value.__name__}'
        else:
            return f'{self.value}'

class Rule:
    def __init__(self,choose_piece,quarto):
        self.quarto=quarto
        self.choose_piece=choose_piece
        self.node=Node(None,self.choose_piece,self.quarto,(random.choice(OPERATIONS_LIST),'operation'))
        self.act=random.choice(ACTIONS_CHOOSE if self.choose_piece else ACTIONS_PLACE)
        self.rule_make_sense=True
        self.action_make_sense=True
        self.rule_quality=0
        self.rule_evaluations=0
        self.rule_true=0
        self.game_true=0
        self.game_evaluations=0
        self.action_possible=0

    def set_quarto(self,quarto):
        self.quarto=quarto
        self.node.set_quarto(quarto)

    def evaluate(self):
        return self.node.eval()

    def evaluate_game_rule(self,won):
        self.rule_quality+=(1 if won else -1) * (self.game_true/self.game_evaluations)
        self.rule_true+=self.game_true
        self.rule_evaluations+=self.game_evaluations
        self.rule_make_sense= True if self.rule_true>0 and self.rule_true!=self.rule_evaluations else False
        self.action_make_sense=False if self.action_possible==0 else True
        #self.rule_fitness= 10 * self.rule_quality + 15 * self.rule_true

    def mutate(self,rule_make_sense=True,action_possible=True):
        if (random.random()<0.3 and rule_make_sense) or (rule_make_sense and not action_possible):
            #mutate action
            self.act=random.choice(ACTIONS_CHOOSE if self.choose_piece else ACTIONS_PLACE)
        else:
            #mutate rule per se
            self.node.mutate()
        #reset values
        self.reset_evaluation_stats()

    def evaluated(self,thruth,action):
        self.game_evaluations+=1
        self.game_true+=thruth
        self.action_possible+=action

    def reset_evaluation_stats(self):
        self.rule_make_sense=True
        self.action_make_sense=True
        self.rule_quality=0
        self.rule_evaluations=0
        self.rule_true=0
        self.game_true=0
        self.game_evaluations=0
        self.action_possible=0

    def reset_game_stats(self):
        self.game_true=0
        self.game_evaluations=0

    def needs_evaluation(self):
        return self.rule_quality==0 or self.rule_true==0 or self.rule_evaluations==0

    def action(self):
        return self.act(self.quarto)

    def __str__(self):
        return f'Rule: node # {str(self.node)} ---> action {self.act.__name__}'