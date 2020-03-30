import time


class Clause:

    def __init__(self, var_list=None, clause_nums=None):
        self.var_list = var_list
        self.is_negated = False
        self.clause_nums = clause_nums


    def negate(self):
        self.is_negated = True
        self.var_list = ['~' + var if var[0] != '~' else var[1:] for var in self.var_list]
        return self.var_list


    def add_clause_nums(self, clause_nums):
        self.clause_nums = clause_nums


    def is_negation_of(self, other):
        self_var_list_len = len(self.var_list)
        other_var_list_len = len(other.var_list)
        if self_var_list_len > 1 or other_var_list_len > 1 or self_var_list_len != other_var_list_len:
            return False
        else:
            if self.var_list[0][0] == '~' and self.var_list[0][1:] == other.var_list[0]:
                return True
            elif other.var_list[0][0] == '~' and other.var_list[0][1:] == self.var_list[0]:
                return True
            else:
                return False


    def var_list_equivalent_with(self, other):
        self_set = { v[1:] if v[0] == '~' else v for v in self.var_list }
        other_set = { v[1:] if v[0] == '~' else v for v in other.var_list }
        return self_set == other_set


    def __hash__(self):
        # print('hash:', ''.join(sorted(self.var_list)))
        return (''.join(sorted(self.var_list))).__hash__()
        # return ((''.join(set(self.var_list)).__hash__()))


    def __eq__(self, other):
        return set(self.var_list) == set(other.var_list)


    def __ne__(self, other):
        return not set(self.var_list) == set(other.var_list)


    def __str__(self):
        if self.var_list is None:
            return ''
        if self.clause_nums is not None:
            return ''.join([var + ' ' for var in self.var_list]) + '{' + str(self.clause_nums[0]) + ', ' + str(self.clause_nums[1]) + '}'
        return ''.join([var + ' ' for var in self.var_list]) + '{}'

    def __repr__(self):
        if self.var_list is None:
            return ''
        if self.clause_nums is not None:
            return ''.join([var + ' ' for var in self.var_list]) + '{' + str(self.clause_nums[0]) + ', ' + str(self.clause_nums[1]) + '}'
        return ''.join([var + ' ' for var in self.var_list]) + '{}'


class KnowledgeBase:

    def __init__(self):
        self.clause_list = []
        self.clause_set = set()
        self.theorem:Clause = None
        # self.variables = set()
        self.contradiction_pair:tuple = None


    def add_clause(self, clause, stack=None):
        
        if stack is not None:
            if clause not in stack:
                stack.append(clause)

        if clause not in self.clause_set:
            self.clause_list.append(clause)
            self.clause_set.add(clause)
        
        # for var in clause.var_list:
        #     self.variables.add((var if var[0] != '~' else var[1:]))


    def add_clauses(self, clause_list):
        for clause in clause_list:
            self.add_clause(clause=Clause(clause.strip().split()))


    def add_theorem_to_prove(self, theorem):
        self.theorem = Clause(theorem.strip().split())


    def resolve(self, clause1, clause2, clause_nums):

        if clause1.is_negation_of(clause2):
            return Clause()

        c1_vars = { var[1:] if var[0] == '~' else var : False if var[0] == '~' else True for var in clause1.var_list }
        c2_vars = { var[1:] if var[0] == '~' else var : False if var[0] == '~' else True for var in clause2.var_list }

        count = 0
        if len(clause1.var_list) == len(clause2.var_list):
            for c1_var in c1_vars:
                if c1_var in c2_vars and (c1_vars[c1_var] == (not c2_vars[c1_var])):
                    count += 1
            if count == len(c1_vars):
                return None

        s = {}
        for var in clause1.var_list:
            s[var[1:] if var[0] == '~' else var] = False if var[0] == '~' else True

        resolvable = False
        count = 0
        for var in clause2.var_list:
            v = var[1:] if var[0] == '~' else var
            b = False if var[0] == '~' else True
            if v in s and (not b) == s[v]:
                resolvable = True
                count += 1
                del s[v]
            else:
                s[v] = b

        if count > 1:
            return None

        clause_str = ''
        for k,v in s.items():
            clause_str += ('~' if v == False else '') + k + ' '
        
        if resolvable:
            return Clause(clause_str.strip().split(), clause_nums)
        else:
            return None


    def prove(self):

        """
        negate the theorem to be proven and add the result to the list of sentences in the KB
        put the list of sentences into CNF
        until there is NO RESOLVABLE pair of clauses
            - find resolvable clauses and resolve them
            - add the results of resolution to the list of clauses
            - if NIL (empty clause) is produced, stop and report that the (original) theorem is true
        report that the (original) theorem is false
        """

        # negates the theorem and asserts into the KB
        self.add_clauses([literal for literal in self.theorem.negate()])

        i = 0
        counter = len(self.clause_list)
        while counter > 0:
            counter -= 1
            for j in range(i):
                if i >= len(self.clause_list):
                    return False
                result_clause = self.resolve(self.clause_list[i], self.clause_list[j], (i+1,j+1))
                if result_clause is not None:
                    if result_clause.var_list is None:
                        self.contradiction_pair = (i+1,j+1)
                        return True
                    else:
                        counter += 1
                        self.add_clause(result_clause)
            i += 1

        return False


    def __repr__(self):
        kb_str = ''
        counter = 1
        for clause in self.clause_list:
            kb_str += str(counter) + '. ' + str(clause) + '\n'
            counter += 1
        if self.contradiction_pair is not None:
            kb_str += str(counter) + '. Contradiction {' + str(self.contradiction_pair[0]) + ', ' + str(self.contradiction_pair[1]) + '}\nValid.'
        else:
            kb_str += "Invalid."
        return kb_str




