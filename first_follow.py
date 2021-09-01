import copy


def get_terminals(grammar, first_s, follow_s):
    terminals = set()
    for key in grammar:
        terminals = terminals | set(first_s[key])
        terminals = terminals | set(follow_s[key])
    return terminals


def break_grammar(grammar):
    br_grammar = {}

    for key, rules in grammar.items():
        br_grammar[key] = []
        for rule in rules:
            rl = []
            for x in rule:
                rl.append(x)
                if x in ["'"]:
                    rl.pop(rl.index(x))
                    rl[-1] = f"{rl[-1]}'"
                
            br_grammar[key].append(rl)
    return br_grammar


def first(grammar, term, prev_term=None):
    a = []
    if term not in grammar:
        return [term]
    for i in grammar[term]:
        if i[0] not in grammar:
            a.append(i[0])
        elif i[0] in grammar:
            a += first(grammar, i[0])
    return a


def follow(grammar, term, follow_sets):
#    print(f'Follow grammar = \n{grammar}')
    starting_sym = next(iter(grammar))
    prods = grammar.items()
    if term == starting_sym:
        follow_sets[term] = follow_sets[term] | {'$'}
    
    for nt, rhs in prods:
        for alt in rhs:
            for char in alt:
                if char == term:
                    if len(alt) > 1:
                        following_str = alt[alt.index(char) + 1:]
                    else:
                        following_str = ''
                    
                #    print(f"{term} : {following_str}")

                    if len(following_str) == 0:
                        if nt == term:
                            continue
                        else:
                            if follow_sets[f"{nt}_flag"] == 1:
                                follow_sets[term] = follow_sets[term] | follow_sets[nt]
                            else:
                                gram = copy.deepcopy(grammar)
                                gram[nt].pop(gram[nt].index(alt))
                                follow_sets[term] = follow_sets[term] | follow(gram, nt, follow_sets)
                    else:
                        le = len(following_str)
                        follow_2 = set(first(grammar, following_str[0]))
                        if le == 1:
                            if '\u03B5' in follow_2:
                                follow_sets[term] = follow_sets[term] | follow_2 - {'\u03B5'}
                                if nt == term:
                                    continue

                                follow_sets[term] = follow_sets[term] | follow(grammar, nt, follow_sets)
                            else:
                                follow_sets[term] = follow_sets[term] | follow_2
                        elif le > 1:
                            if '\u03B5' in follow_2:
                                follow_sets[term] = follow_sets[term] | follow_2 - {'\u03B5'}
                                follow_sets[term] = follow_sets[term] | follow(grammar, following_str[1], follow_sets)
                            else:
                                follow_sets[term] = follow_sets[term] | follow_2

    if len(follow_sets[term]) != 0:
        follow_sets[f"{term}_flag"] = 1
    return follow_sets[term]



if __name__ == "__main__":

    from left_recursion__ import left_recursion
    from left_factoring import left_factoring

    grammar = {
        "E":["E+T","T"], 
        "T":["T*F","F"], 
        "F":["(E)","i"]
    }

    # grammar = {
    #     "S": ["L=R", "R"],
    #     "L": ["*R", "a"],
    #     "R": ["L"]
    # }

    # grammar = {
    #     "S": ["iEtSeS", "iEtS", "a"],
    #     "E": ["b"]
    # }

    # grammar = {
    #     "S": ["A"],
    #     "A": ["aA''"],
    #     "A''": ["BA'", "CA'"],
    #     "A'": ["dA'", "eA'", "\u03B5"],
    #     "B": ["bBc", "f"],
    #     "C": ["g"]
    # }

    # grammar = {
    #     "S": ["A"],
    #     "A": ["aB", "aC", "Ad", "Ae"],
    #     "B": ["bBc", "f"],
    #     "C": ["g"]
    # }

    print("Grammar:")
    for key, rules in grammar.items():
        print(key, "-> ", end="")
        for r in range(len(rules)):
            if r == 0:
                print(rules[r], end=" ")
            else:
                print("|", rules[r], end=" ")

        print("")
    print("")

    lr_grammar = left_recursion(grammar)
    print("After Removing Left Recursion:")
    for key, rules in lr_grammar.items():
        print(key, "-> ", end="")
        for r in range(len(rules)):
            if r == 0:
                print(rules[r], end=" ")
            else:
                print("|", rules[r], end=" ")

        print("")
    print("")

    lf_grammar, non_terminals = left_factoring(lr_grammar)

    print(f"After Performing Left Factoring:")
    for key, rules in lf_grammar.items():
        print(key, "-> ", end="")
        for r in range(len(rules)):
            if r == 0:
                print(rules[r], end=" ")
            else:
                print("|", rules[r], end=" ")

        print("")
    print("")

    br_grammar = break_grammar(lf_grammar)
    print(f"Breaking Grammar\n{br_grammar}\n\n")

    print(f"LF Grammar = \n{lf_grammar}\n\n")
    # for key, rules in br_grammar.items():
    #     print(key, "-> ", end="")
    #     for r in range(len(rules)):
    #         test_str = ""
    #         for x in rules[r]:
    #             test_str += x
    #         if r == 0:
    #             print(test_str, end=" ")
    #         else:
    #             print("|", test_str, end=" ")

    #     print("")
    # print("\n")

    first_sets = {}
    for i in br_grammar:
        first_sets[i] = list(set(first(br_grammar, i)))
        print(f"First({i}): ", first_sets[i])

    print("")

    follow_sets = {}
    for i in br_grammar:
        follow_sets[i] = set()
        follow_sets[f"{i}_flag"] = 0

    for i in br_grammar:
        follow_sets[i] = follow_sets[i] | follow(br_grammar, i, follow_sets)
        print(f"Follow({i}): ", follow_sets[i])

    terminals = get_terminals(lf_grammar, first_sets, follow_sets)   
    print(f"\nTerminals = {terminals}\n")
    print(f"Non Terminals = {non_terminals}\n")