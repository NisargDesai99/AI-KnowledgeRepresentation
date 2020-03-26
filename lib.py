

class Clause:

    def __init__(self, var_list):
        self.var_list = var_list
        self.is_negated = False


    def __str__(self):
        return ''.join([var + ' V ' for var in self.var_list])[:-3]


    def __repr__(self):
        return ''.join([var + ' V ' for var in self.var_list])[:-3]


class KnowledgeBase:

    def __init__(self):
        self.clause_set = set()


    def add_clause(self, clause):
        self.clause_set.add(clause)


    def __negate(self, clause):
        pass


    def check_resolution(self, clause1, clause2):
        print('checking resolution on clauses:', clause1, clause2)


    def prove(self):
        print('running prove()')




    def __repr__(self):
        return ''.join([ (clause.__str__() + '\n') for clause in self.clause_set])




