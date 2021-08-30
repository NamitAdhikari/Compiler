def main(grammar):

    print("\nGrammar:")
    for key, rules in grammar.items():
        print(key, "-> ", end="")
        for r in range(len(rules)):
            if r == 0:
                print(rules[r], end=" ")
            else:
                print("|", rules[r], end=" ")

        print("")
    print("")

    start_symbol = next(iter(grammar))

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

    first_sets = {}
    for i in br_grammar:
        first_sets[i] = list(set(first(br_grammar, i)))
        print(f"First({i}):\t", first_sets[i])

    print("")

    follow_sets = {}
    for i in br_grammar:
        follow_sets[i] = set()
        follow_sets[f"{i}_flag"] = 0

    for i in br_grammar:
        follow_sets[i] = follow_sets[i] | follow(br_grammar, i, follow_sets)
        print(f"Follow({i}):\t", follow_sets[i])

    terminals = get_terminals(lf_grammar, first_sets, follow_sets)   
    print(f"\nTerminals = {terminals}\n")
    print(f"Non Terminals = {non_terminals}\n")

    par_table = parsing_table(br_grammar, lf_grammar, terminals, first_sets, follow_sets)

    #user_input = "i-*(*i)"
    user_input = input("Enter string to parse: ")
    print("\nNow, Parsing ", user_input)
    parse(user_input, start_symbol, par_table)


if __name__ == "__main__":
    
    from grammar_modify import gr_mod
    from left_recursion__ import left_recursion
    from left_factoring import left_factoring
    from first_follow import break_grammar, first, follow, get_terminals
    from parsing_table import parsing_table
    from parse import parse


    # grammar = {
    #     "E":["E+T","T"], 
    #     "T":["T*F","F"], 
    #     "F":["(E)","i"]
    # }

    # grammar = {
    #     "S'": ["S"],
    #     "S": ["L=R", "R"],
    #     "L": ["*R", "i"],
    #     "R": ["L"]
    # }

    grammar = {
        "S": ["iEtSeS", "iEtS"],
        "E": ["b"]
    }

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

    # grammar = {
    #     "E": ["T", "T-E"],
    #     "T": ["F", "*F"],
    #     "F": ["i", "(E)"]
    # }

    # grammar = {
    #     "B": ["B+T", "T"],
    #     "T": ["T*F", "F"],
    #     "F": ["~B", "(B)", "t", "f"]
    # }

    # grammar = {
    #     "S": ["aAc", "bB"],
    #     "A": ["Abc", "Abd", "e"],
    #     "B": ["f", "g"],
    #     "C": ["h", "i"]
    # }

    # grammar = {
    #     "E": ["TE'"],
    #     "E'": ["E", "e"],
    #     "T": ["F", "T'"],
    #     "T'": ["T", "e"],
    #     "F": ["PF'"],
    #     "F'": ["*F'", "e"],
    #     "P": ["(E)", "a", "b", "e"]
    # }

    # grammar = {
    #     "S": ["Aa", "b"],
    #     "A": ["Ac", "Sd", "\u03B5"]
    # }

    # grammar = open("grammar", "r").read()
    # grammar = gr_mod(grammar)

    main(grammar)
