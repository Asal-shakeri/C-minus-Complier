class Terminal:
    def __init__(self, name):
        self.name = name
        self.first = [name]

    def __str__(self):
        s = f"{self.name}"
        return s


class NonTerminal:
    def __init__(self, name, first=[], follow=[]):
        self.name = name
        self.first = first
        self.follow = follow

    def __str__(self):
        s = f"{self.name}"
        return s


class Action:
    def __init__(self, name):
        self.name = name


class Rule:
    def __init__(self, left, right, predict_set=None):
        self.left = left
        self.right = right
        self.predict_set = ([], predict_set)[predict_set is None]

    def add_predict(self, *args):
        self.predict_set.extend(args)


class Grammar:
    def __init__(self, non_terminals, terminals):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.rules = []
        self.predict_sets = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def import_rules(self, path):
        with open(path, encoding='utf-8') as f:
            for line in f.readlines():
                raw_rule = line.split("->")
                raw_rule[1].strip('\n')
                right = []
                for e in raw_rule[1].split():
                    if e:
                        right.append(self.get_element_by_id(e.rstrip()))
                left = self.get_element_by_id(raw_rule[0].rstrip())
                self.add_rule(Rule(left, right))

    def import_firsts(self, path):
        with open(path, encoding='utf-8') as f:
            for line in f.readlines():
                first = line.split()
                nt = self.get_element_by_id(first[0])
                nt.first = [self.get_element_by_id(e.rstrip()) for e in first[1:]]

    def import_follows(self, path):
        with open(path) as f:
            for line in f.readlines():
                follow = line.split()
                nt = self.get_element_by_id(follow[0])
                nt.follow = [self.get_element_by_id(e.rstrip()) for e in follow[1:]]

    def import_predict_sets(self, path):
        with open(path) as f:
            for i, line in enumerate(f.readlines()):
                predict_set = line.split()
                self.predict_sets.append([self.get_element_by_id(e.rstrip()) for e in predict_set[0:]])
                self.rules[i].predict_set = [self.get_element_by_id(e.rstrip()) for e in predict_set[0:]]

    def get_element_by_id(self, name):
        for nt in self.non_terminals:
            if nt.name == name: return nt
        for t in self.terminals:
            if t.name == name: return t
        return Action(name)

    def is_terminal(self, name):
        for t in self.terminals:
            if t.name == name: return True
        return False


def init_terminals():
    terminals_str = 'EPSILON ID [NUM]; ; (Params)Compound-stmt int void ,Param ] [ Statement-list} {Declaration-list Expression; break; else ) ( if repeat until return =Expression [Expression]H < == + −'
    # return [Terminal(x) for x in terminals_str.split(' ')]

    return [Terminal('$'), Terminal('ε'), Terminal('ID'), Terminal(';'), Terminal('['), Terminal('NUM'),
            Terminal(']'), Terminal('('), Terminal(')'), Terminal('int'), Terminal('void'), Terminal(','),
            Terminal('{'), Terminal('}'), Terminal('break'), Terminal('if'), Terminal('else'), Terminal('while'),
            Terminal('return'), Terminal('switch'), Terminal('case'), Terminal('default'), Terminal(':'),
            Terminal('='), Terminal('<'), Terminal('=='), Terminal('+'), Terminal('-'), Terminal('*')]


def init_non_terminals():
    non_terminals_str='Program Declaration-list Declaration Declaration-initial Declaration-prime Type-specifier Fun-declaration-prime Var-declaration-prime Params Param-list Param-prime Param Compound-stmt Statement-list Statement Expression-stmt Return-stmt Iteration-stmt Selection-stmt Expression Return-stmt-prime Simple-expression-zegond B Simple-expression-prime H C D G Additive-expression-zegond Additive-expression-prime Relop Additive-expression Term Term-prime Term-zegond Addop Factor Factor-prime Factor-zegond ∗Factor (Expression) NUM Var-prime (Args) [Expression] Arg-list Arg-list-prime ,Expression'
    # return [NonTerminal(x) for x in non_terminals_str.split(' ')]
    return [
            
        
            NonTerminal('Program'), NonTerminal('Declaration-list'), NonTerminal('Declaration'),
            NonTerminal('Declaration-initial'), NonTerminal('Declaration-prime'),
            NonTerminal('Var-declaration-prime'),
            NonTerminal('Fun-declaration-prime'), NonTerminal('Type-specifier'), NonTerminal('Params'),
            NonTerminal('Param-list-void-abtar'), NonTerminal('Param-list'), NonTerminal('Param'),
            NonTerminal('Param-prime'), NonTerminal('Compound-stmt'), NonTerminal('Statement-list'),
            NonTerminal('Statement'), NonTerminal('Expression-stmt'), NonTerminal('Selection-stmt'),
            NonTerminal('Iteration-stmt'), NonTerminal('Return-stmt'), NonTerminal('Return-stmt-prime'),
            NonTerminal('Switch-stmt'), NonTerminal('Case-stmts'), NonTerminal('Case-stmt'),
            NonTerminal('Default-stmt'), NonTerminal('Expression'), NonTerminal('B'), NonTerminal('H'),
            NonTerminal('Simple-expression-zegond'), NonTerminal('Simple-expression-prime'), NonTerminal('C'),
            NonTerminal('Relop'), NonTerminal('Additive-expression'), NonTerminal('Additive-expression-prime'),
            NonTerminal('Additive-expression-zegond'), NonTerminal('D'), NonTerminal('Addop'),
            NonTerminal('Term'), NonTerminal('Term-prime'), NonTerminal('Term-zegond'), NonTerminal('G'),
            NonTerminal('Signed-factor'), NonTerminal('Signed-factor-prime'), NonTerminal('Signed-factor-zegond'),
            NonTerminal('Factor'), NonTerminal('Var-call-prime'), NonTerminal('Var-prime'),
            NonTerminal('Factor-prime'), NonTerminal('Factor-zegond'), NonTerminal('Args'),
            NonTerminal('Arg-list'), NonTerminal('Arg-list-prime')]


def init_grammar():
    grammar = Grammar(init_non_terminals(), init_terminals())
    grammar.import_firsts("Parser/data/Firsts.txt")
    grammar.import_follows("Parser/data/Follows.txt")
    grammar.import_rules("Parser/data/grammar.txt")
    grammar.import_predict_sets("Parser/data/Predicts.csv")
    return grammar
