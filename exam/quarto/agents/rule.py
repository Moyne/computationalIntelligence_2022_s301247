import random
import agents.quartolib as quartolib
TRUE_PROPS=['high','solid','square','coloured']
def isnumber(a):
    return (isinstance(a,int) or isinstance(a,float) or isinstance(a,bool))
def tonum(a):
    if isnumber(a):
        return a
    else:
        return 0
IF_OPERATIONS={
    'mul': (lambda a,b: a*b if isnumber(a) and isnumber(b) else float(a) if isnumber(a) else float(b) if isnumber(b) else 0),
    'add': (lambda a,b: a+b if isnumber(a) and isnumber(b) else float(a) if isnumber(a) else float(b) if isnumber(b) else 0),
    'sub': (lambda a,b: a-b if isnumber(a) and isnumber(b) else float(a) if isnumber(a) else float(b) if isnumber(b) else 0),
    'not': (lambda a,b: not a),
    'or': (lambda a,b: a or b),
    #'truechar':(lambda a,b: a in TRUE_PROPS),
    #'falsechar':(lambda a,b: a not in TRUE_PROPS),
    'gt':(lambda a,b:tonum(a)>tonum(b)),
    'lt':(lambda a,b:tonum(a)<tonum(b)),
    'gte':(lambda a,b:tonum(a)>=tonum(b)),
    'lte':(lambda a,b:tonum(a)<=tonum(b)),
    'and': (lambda a,b: a and b),
    'eq': (lambda a,b: a==b),
    'ne': (lambda a,b: a!=b)
}

THEN_PLACE_OPERATIONS={
    'colmore': (lambda quarto,a,b: a if quartolib.compare_elements_in_columns(quarto,a[0],b[0]) else b),
    'colless': (lambda quarto,a,b: b if quartolib.compare_elements_in_columns(quarto,a[0],b[0]) else a),
    'rowmore': (lambda quarto,a,b: a if quartolib.compare_elements_in_rows(quarto,a[1],b[1]) else b),
    'rowless': (lambda quarto,a,b: b if quartolib.compare_elements_in_rows(quarto,a[1],b[1]) else a),
    'diagmore': (lambda quarto,a,b: a if quartolib.compare_elements_in_diag(quarto,a,b) else b),
    'diagless': (lambda quarto,a,b: b if quartolib.compare_elements_in_diag(quarto,a,b) else a),
    'antidiagmore': (lambda quarto,a,b: a if quartolib.compare_elements_in_antidiag(quarto,a,b) else b),
    'antidiagless': (lambda quarto,a,b: b if quartolib.compare_elements_in_antidiag(quarto,a,b) else a),
    'possible': (lambda quarto,a,b: a if quartolib.place_possible(quarto,a,b) else b)
}

THEN_CHOOSE_OPERATIONS={
    'moreunique': (lambda quarto,a,b: a if quartolib.compare_uniqueness(quarto,a,b) else b),
    'lessunique': (lambda quarto,a,b: b if quartolib.compare_uniqueness(quarto,a,b) else a),
    'trues': (lambda quarto,a,b: a if quartolib.compare_trues(quarto,a,b) else b),
    'falses': (lambda quarto,a,b: b if quartolib.compare_trues(quarto,a,b) else a),
    'diffinmostusedrownotcomplete': (lambda quarto,a,b: a if quartolib.more_different_in_most_used_row_not_complete(quarto,a,b) else b),
    'similarinmostusedrownotcomplete': (lambda quarto,a,b: b if quartolib.more_different_in_most_used_row_not_complete(quarto,a,b) else a),
    'diffinmostusedcolnotcomplete': (lambda quarto,a,b: a if quartolib.more_different_in_most_used_column_not_complete(quarto,a,b) else b),
    'similarinmostusedcolumnnotcomplete': (lambda quarto,a,b: b if quartolib.more_different_in_most_used_column_not_complete(quarto,a,b) else a),
    'diffinlessusedrownotcomplete': (lambda quarto,a,b: a if quartolib.more_different_in_less_used_row(quarto,a,b) else b),
    'similarinlessusedrownotcomplete': (lambda quarto,a,b: b if quartolib.more_different_in_less_used_row(quarto,a,b) else a),
    'diffinlessusedcolnotcomplete': (lambda quarto,a,b: a if quartolib.more_different_in_less_used_column(quarto,a,b) else b),
    'similarinlessusedcolumnnotcomplete': (lambda quarto,a,b: b if quartolib.more_different_in_less_used_column(quarto,a,b) else a),
    'differentdiag': (lambda quarto,a,b: a if quartolib.more_different_in_diagonal(quarto,a,b) else b),
    'similardiag': (lambda quarto,a,b: b if quartolib.more_different_in_diagonal(quarto,a,b) else a),
    'differentantidiag': (lambda quarto,a,b: a if quartolib.more_different_in_antidiagonal(quarto,a,b) else b),
    'similardiag': (lambda quarto,a,b: b if quartolib.more_different_in_antidiagonal(quarto,a,b) else a),
    'possible': (lambda quarto,a,b: a if quartolib.choose_possible(quarto,a,b) else b)
}

THEN_LEAF_PLACE_FUNCTIONS=quartolib.get_then_place_functions()

THEN_LEAF_CHOOSE_FUNCTIONS=quartolib.get_then_choose_functions()

IF_OPERATIONS_LIST=list(IF_OPERATIONS.keys())
IF_OPERATIONS_CHOOSE=['not','or','and','ne','eq','ne']#,'truechar','falsechar']
IF_OPERATIONS_PLACE=['mul','add','sub','not','or','gt','lt','gte','lte','and','eq','ne']
IF_OPERATIONS_WITH_ONE_OPERAND=set(['not','truechar','falsechar'])
IF_CHOOSE_FUNCTIONS=quartolib.get_choose_functions()
IF_PLACE_FUNCTIONS=quartolib.get_place_functions()
IF_PLACE_VALUES=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,True,False]
IF_CHOOSE_VALUES=['high','not_high','solid','not_solid','coloured','not_coloured','square','not_square',True,False]

IF_POSSIBLE_CHOOSE_VALUES=[[(op,'operation') for op in IF_OPERATIONS_CHOOSE],[(func,'function') for func in IF_CHOOSE_FUNCTIONS],[(val,'value') for val in IF_CHOOSE_VALUES]]

IF_POSSIBLE_PLACE_VALUES=[[(op,'operation') for op in IF_OPERATIONS_PLACE],[(func,'function') for func in IF_PLACE_FUNCTIONS],[(val,'value') for val in IF_PLACE_VALUES]]

THEN_POSSIBLE_CHOOSE_VALUES=[[(op,'operation') for op in list(THEN_CHOOSE_OPERATIONS.keys())],[(leaf,'leaf') for leaf in THEN_LEAF_CHOOSE_FUNCTIONS]]

THEN_POSSIBLE_PLACE_VALUES=[[(op,'operation') for op in list(THEN_PLACE_OPERATIONS.keys())],[(leaf,'leaf') for leaf in THEN_LEAF_PLACE_FUNCTIONS]]


RECURSION_MAX_DEPTH=100
class ThenNode:
    def __init__(self,parent,choose_piece,quarto) -> None:
        self.parent=parent
        self.quarto=quarto
        self.choose_piece=choose_piece
        self.childs=[]
        self.depth=0 if self.parent is None else self.parent.depth+1
        value=random.choice(THEN_POSSIBLE_CHOOSE_VALUES[0 if self.parent is None else random.choice([0,1,1]) if self.depth<RECURSION_MAX_DEPTH else 1] if self.choose_piece else THEN_POSSIBLE_PLACE_VALUES[0 if self.parent is None else random.choice([0,1,1]) if self.depth<RECURSION_MAX_DEPTH else 1])
        if self.parent is None:
            value=('possible','operation')
        self.value=value[0]
        self.op=value[1]=='operation'
        self.leaf=value[1]=='leaf'
        self.optdict=None
        #print(f'Value for node is {value} , op {self.op} func {self.func} val {self.val}')
        if self.op:
            self.optdict=THEN_CHOOSE_OPERATIONS if self.choose_piece else THEN_PLACE_OPERATIONS
            self.childs.append(ThenNode(self,self.choose_piece,self.quarto))
            self.childs.append(ThenNode(self,self.choose_piece,self.quarto))

    def mutate(self):
        if random.random()<0.5 and self.op:
            #mutate one of the childs
            num=random.randint(0,2)
            if num==0 or num==2:
                self.childs[0].mutate()
            if num==1 or num==2:
                self.childs[1].mutate()
        else:
            #mutate myself
            if random.random()<0.5 and self.parent is not None:
                #go full random, don't care about what type of thing I was before
                value=random.choice(THEN_POSSIBLE_CHOOSE_VALUES[random.choice([0,1,1]) if self.depth<RECURSION_MAX_DEPTH else 1] if self.choose_piece else THEN_POSSIBLE_PLACE_VALUES[random.choice([0,1,1]) if self.depth<RECURSION_MAX_DEPTH else 1])
                self.value=value[0]
                self.op=value[1]=='operation'
                self.leaf=value[1]=='leaf'
                if self.op:
                    self.optdict=THEN_CHOOSE_OPERATIONS if self.choose_piece else THEN_PLACE_OPERATIONS
                    if random.random()<1/3 or len(self.childs)!=2:
                        self.childs=[]
                        self.childs.append(ThenNode(self,self.choose_piece,self.quarto))
                        self.childs.append(ThenNode(self,self.choose_piece,self.quarto))
                    elif len(self.childs)==2:
                        num=random.randint(0,6)
                        if num==0 or num==2:
                            self.childs[0].mutate()
                        if num==1 or num==2:
                            self.childs[1].mutate()
                else:
                    self.childs=[]
            else:
                #keep my old type
                value=random.choice(THEN_POSSIBLE_CHOOSE_VALUES[0 if self.op else 1] if self.choose_piece else THEN_POSSIBLE_PLACE_VALUES[0 if self.op else 1])
                self.value=value[0]
                self.op=value[1]=='operation'
                self.leaf=value[1]=='leaf'
                if self.op:
                    self.optdict=THEN_CHOOSE_OPERATIONS if self.choose_piece else THEN_PLACE_OPERATIONS
                    if random.random()<1/3:
                        self.childs=[]
                        self.childs.append(ThenNode(self,self.choose_piece,self.quarto))
                        self.childs.append(ThenNode(self,self.choose_piece,self.quarto))
                    else:
                        num=random.randint(0,6)
                        if num==0 or num==2:
                            self.childs[0].mutate()
                        if num==1 or num==2:
                            self.childs[1].mutate()
                        
                else:
                    self.childs=[]

    def set_quarto(self,quarto):
        self.quarto=quarto
        if self.op:
            for child in self.childs:
                child.set_quarto(self.quarto)

    def action(self):
        if not self.op:
            return self.value(self.quarto)
        else:
            evals=[child.action() for child in self.childs]
            left_val,rigth_val=evals[0],evals[1]
            return self.optdict[self.value](self.quarto,left_val,rigth_val)

    def __str__(self):
        if self.op:
            return f'({str(self.childs[0])}) {self.value} ({str(self.childs[1])})'
        else:
            return f'{self.value.__name__}'


class IfNode:
    def __init__(self,parent,choose_piece,quarto) -> None:
        self.parent=parent
        self.quarto=quarto
        self.choose_piece=choose_piece
        self.childs=[]
        value=random.choice(IF_POSSIBLE_CHOOSE_VALUES[0 if self.parent is None else random.randint(0,2)] if choose_piece else IF_POSSIBLE_PLACE_VALUES[0 if self.parent is None else random.randint(0,2)])
        self.value=value[0]
        self.op=value[1]=='operation'
        self.func=value[1]=='function'
        self.val=value[1]=='value'
        #print(f'Value for node is {value} , op {self.op} func {self.func} val {self.val}')
        if self.op:
            #print(f'Need a child or two')
            self.childs.append(IfNode(self,self.choose_piece,self.quarto))
            if self.value not in IF_OPERATIONS_WITH_ONE_OPERAND:
                self.childs.append(IfNode(self,self.choose_piece,self.quarto))
        else:
            pass
            #print(f'No need for childs')

    def mutate(self):
        if random.random()<0.5 and self.op:
            #mutate one of the childs
            num=random.randint(0,2)
            if (num==0 or num==2) or (self.value in IF_OPERATIONS_WITH_ONE_OPERAND):
                self.childs[0].mutate()
            if (num==1 or num==2) and (self.value not in IF_OPERATIONS_WITH_ONE_OPERAND):
                self.childs[1].mutate()
        else:
            #mutate myself
            if random.random()<0.5 and self.parent is not None:
                #go full random, don't care about what type of thing I was before
                value=random.choice(IF_POSSIBLE_CHOOSE_VALUES[random.randint(0,2)] if self.choose_piece else IF_POSSIBLE_PLACE_VALUES[random.randint(0,2)])
                self.value=value[0]
                self.op=value[1]=='operation'
                self.func=value[1]=='function'
                self.val=value[1]=='value'
                if self.op:
                    #print(f'Need a child or two')
                    if random.random()<1/3 and len(self.childs)>0:
                        #keep old childs
                        if self.value in IF_OPERATIONS_WITH_ONE_OPERAND and len(self.childs)==2:
                            #remove one of the two childs in case
                            self.childs.pop(random.randint(0,len(self.childs)-1))
                        elif (self.value not in IF_OPERATIONS_WITH_ONE_OPERAND) and (len(self.childs)==1):
                            self.childs.append(IfNode(self,self.choose_piece,self.quarto))
                        num=random.randint(0,6)
                        if num==0 or num==2 or (num==3 and (self.value in IF_OPERATIONS_WITH_ONE_OPERAND)):
                            self.childs[0].mutate()
                        if (num==1 or num==2) and (self.value not in IF_OPERATIONS_WITH_ONE_OPERAND):
                            self.childs[1].mutate()
                    else:
                        self.childs=[]
                        self.childs.append(IfNode(self,self.choose_piece,self.quarto))
                        if self.value not in IF_OPERATIONS_WITH_ONE_OPERAND:
                            self.childs.append(IfNode(self,self.choose_piece,self.quarto))
                else:
                    self.childs=[]
            else:
                #keep my old type
                value=random.choice(IF_POSSIBLE_CHOOSE_VALUES[0 if self.op else 1 if self.func else 2] if self.choose_piece else IF_POSSIBLE_PLACE_VALUES[0 if self.op else 1 if self.func else 2])
                self.value=value[0]
                self.op=value[1]=='operation'
                self.func=value[1]=='function'
                self.val=value[1]=='value'
                if self.op:
                    #print(f'Need a child or two')
                    if random.random()<1/3 and len(self.childs)>0:
                        #keep old childs
                        if self.value in IF_OPERATIONS_WITH_ONE_OPERAND and len(self.childs)==2:
                            #remove one of the two childs in case
                            self.childs.pop(random.randint(0,len(self.childs)-1))
                        elif (self.value not in IF_OPERATIONS_WITH_ONE_OPERAND) and (len(self.childs)==1):
                            self.childs.append(IfNode(self,self.choose_piece,self.quarto))
                        num=random.randint(0,6)
                        if num==0 or num==2 or (num==3 and (self.value in IF_OPERATIONS_WITH_ONE_OPERAND)):
                            self.childs[0].mutate()
                        if (num==1 or num==2) and (self.value not in IF_OPERATIONS_WITH_ONE_OPERAND):
                            self.childs[1].mutate()
                    else:
                        self.childs=[]
                        self.childs.append(IfNode(self,self.choose_piece,self.quarto))
                        if self.value not in IF_OPERATIONS_WITH_ONE_OPERAND:
                            self.childs.append(IfNode(self,self.choose_piece,self.quarto))
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
            return IF_OPERATIONS[self.value](left_val,rigth_val)

    def __str__(self):
        if self.op:
            if self.value not in IF_OPERATIONS_WITH_ONE_OPERAND:
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
        self.if_node=IfNode(None,self.choose_piece,self.quarto)
        self.then_node=ThenNode(None,self.choose_piece,self.quarto)
        #data and evaluations
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
        self.if_node.set_quarto(self.quarto)
        self.then_node.set_quarto(self.quarto)

    def evaluate(self):
        return self.if_node.eval()

    def evaluate_game_rule(self,won):
        self.rule_true+=self.game_true
        self.rule_evaluations+=self.game_evaluations
        self.rule_make_sense= self.rule_true>0 and self.rule_true<0.5*self.rule_evaluations
        self.action_make_sense=self.rule_true>0 and self.action_possible>=(2*(self.rule_true/3))
        self.rule_quality+=((self.game_evaluations-self.game_true)/self.game_evaluations) * 10 if won else -((self.game_true/self.game_evaluations) * 10)
        #self.rule_fitness= 10 * self.rule_quality + 15 * self.rule_true

    def mutate(self,rule_make_sense=True,action_possible=True):
        if (random.random()<0.3 and rule_make_sense) or (rule_make_sense and not action_possible):
            #mutate then tree
            self.then_node.mutate()
        else:
            #mutate if tree
            self.if_node.mutate()
        #self.if_node.mutate()
        #self.then_node.mutate()
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
        return self.rule_evaluations==0

    def action(self):
        return self.then_node.action()

    def __str__(self):
        return f'Rule: if {str(self.if_node)} ---> action {self.then_node} ::= rule quality {self.rule_quality}'