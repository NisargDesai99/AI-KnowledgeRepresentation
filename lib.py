

class Clause:

    def __init__(self, var_list, clause_nums=None):
        self.var_list = var_list
        self.is_negated = False
        self.clause_nums = clause_nums


    def negate(self):
        self.is_negated = True
        self.var_list = [(var[1] if var[0] == '~' else '~' + var[0]) for var in self.var_list]
        return self.var_list


    def add_clause_nums(self, clause_nums):
        self.clause_nums = clause_nums


    # def is_negation_of(self, other):
    #     if len(self.var_list) != len(other.var_list):
    #         return False
    #     else:
    #         for i in range(len(self.var_list)):




    def __hash__(self):
        print('hash:', ''.join(sorted(self.var_list)))
        return ((''.join(sorted(self.var_list))).__hash__())


    def __eq__(self, other):
        return set(self.var_list) == set(other.var_list)


    def __ne__(self, other):
        return not set(self.var_list) == set(other.var_list)


    def __str__(self):
        if self.clause_nums is not None:
            return ''.join([var + ' ' for var in self.var_list]) + '{' + str(self.clause_nums[0]) + ',' + str(self.clause_nums[1]) + '}'
        return ''.join([var + ' ' for var in self.var_list]) + '{}'

        # return ''.join([var + (' ^ ' if self.is_negated else ' V ') for var in self.var_list])[:-3] + ' {' + str(self.clause_nums[0]) + ',' + str(self.clause_nums[1]) + '}'
        # return ''.join([var + (' ^ ' if self.is_negated else ' V ') for var in self.var_list])[:-3]


    def __repr__(self):
        return ''.join([var + (' ^ ' if self.is_negated else ' V ') for var in self.var_list])[:-3]


class KnowledgeBase:

    def __init__(self):
        self.clause_list = []
        self.theorem:Clause = None
        self.variables = set()


    def add_clause(self, stack=None, clause=None):
        if stack is not None:
            if not clause in stack:
                stack.append(clause)
        
        if not clause in self.clause_list:
            self.clause_list.append(clause)
        
        for var in clause.var_list:
            self.variables.add((var if var[0] != '~' else var[1]))


    def add_clauses(self, clause_list):
        for clause in clause_list:
            self.add_clause(clause=Clause(clause.strip().split()))


    def add_theorem_to_prove(self, theorem):
        self.theorem = Clause(theorem.strip().split())


    def check_resolution(self, clause1, clause2):
        print('checking resolution on clauses:', clause1, clause2)


    def resolve(self, clause1, clause2, clause_nums):
        c1_vars = { var[1] if var[0] == '~' else var : False if var[0] == '~' else True for var in clause1.var_list }
        c2_vars = { var[1] if var[0] == '~' else var : False if var[0] == '~' else True for var in clause2.var_list }
        # print('c1_vars:', c1_vars)
        # print('c2_vars:', c2_vars)
        
        if clause1.is_negation_of(clause2):
            return 'Contradiction'

        count = 0
        if len(clause1.var_list) == len(clause2.var_list):
            for c1_var in c1_vars:
                if c1_var in c2_vars and (c1_vars[c1_var] == (not c2_vars[c1_var])):
                    count += 1
            if count == len(c1_vars):
                return None

        s = {}
        for var in clause1.var_list:
            s[var[1] if var[0] == '~' else var] = False if var[0] == '~' else True

        resolvable = False
        count = 0
        for var in clause2.var_list:
            v = var[1] if var[0] == '~' else var
            b = False if var[0] == '~' else True
            if v in s and (not b) == s[v]:
                resolvable = True
                count += 1
                del s[v]
            else:
                s[var[1] if var[0] == '~' else var] = False if var[0] == '~' else True

        if count > 1:
            return None

        clause_str = ''
        for k,v in s.items():
            clause_str += ('~' if v == False else '') + k + ' '
        
        if resolvable:
            print('resolved: ', clause_str, ' | ', clause1, ' | ', clause2)
            return Clause(clause_str.strip().split(), clause_nums)
        else:
            return None


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

        print('starting to attempt resolutions')
        i = 0
        s = [c for c in self.clause_list]
        while len(s) > 0:
            s.pop()
            for j in range(i):
                print(self.clause_list[j])
                # print('attempting resolve:', self.clause_list[i], 'with', self.clause_list[j])
                result_clause = self.resolve(self.clause_list[i], self.clause_list[j], (i,j))
                print('result:', result_clause)
                if result_clause is not None:
                    self.add_clause(stack=s, clause=result_clause)
                    print(self)
            i += 1

        print(self)
        print('done running prove()')
        return False


    def __repr__(self):
        kb_str = ''
        counter = 1
        for clause in self.clause_list:
            kb_str += str(counter) + '. ' + str(clause) + '\n'
            counter += 1
        return kb_str




