

class Clause:

    def __init__(self, var_list):
        self.var_list = var_list
        self.is_negated = False


    def negate(self):
        self.is_negated = True
        self.var_list = [('~' if var[0] != '~' else '') + var for var in self.var_list]
        return self.var_list
        

    def __str__(self):
        return ''.join([var + (' ^ ' if self.is_negated else ' V ') for var in self.var_list])[:-3]


    def __repr__(self):
        return ''.join([var + (' ^ ' if self.is_negated else ' V ') for var in self.var_list])[:-3]


class KnowledgeBase:

    def __init__(self):
        self.clause_list = []
        self.theorem:Clause = None
        self.variables = set()


    def add_clause(self, clause):
        if clause not in self.clause_list:
            self.clause_list.append(clause)
        for var in clause.var_list:
            self.variables.add((var if var[0] != '~' else var[1]))


    def add_clauses(self, clause_list):
        for clause in clause_list:
            self.add_clause(Clause(clause.strip().split()))


    def add_theorem_to_prove(self, theorem):
        self.theorem = Clause(theorem.strip().split())


    def check_resolution(self, clause1, clause2):
        print('checking resolution on clauses:', clause1, clause2)


    def resolve(self, clause1, clause2):
        print('attempting resolution:', clause1, ' || ', clause2)
        c1_vars = { var for var in clause1.var_list }
        c2_vars = { var for var in clause2.var_list }

        print('c1_vars:', c1_vars)
        print('c2_vars:', c2_vars)
        

    def prove(self):
        print('running prove()')

        """
        negate the theorem to be proven and add the result to the list of sentences in the KB
        put the list of sentences into CNF
        until there is NO RESOLVABLE pair of clauses
            - find resolvable clauses and resolve them
            - add the results of resolution to the list of clauses
            - if NIL (empty clause) is produced, stop and report that the (original) theorem is true
        report that the (original) theorem is false
        """

        # print('original:\n', self)
        
        # negates the theorem and asserts into the KB
        self.add_clauses([literal for literal in self.theorem.negate()])
        print(self)
        

        # TODO: figure out a way to find clauses that can be resolved
        print(self.variables)

        for i in range(len(self.clause_list)):
            for j in range(i):
                self.resolve(self.clause_list[i], self.clause_list[j])
            


        print('done running prove()')
        return False


    def __repr__(self):
        return ''.join([ (clause.__str__() + '\n') for clause in self.clause_list])




