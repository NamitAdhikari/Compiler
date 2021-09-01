from itertools import takewhile


def groupby(rules):
    d = {}
    ls = [ y[0] for y in rules ]
    initial = list(set(ls))
    for y in initial:
        for i in rules:
            if i.startswith(y):
                if y not in d:
                    d[y] = []
                d[y].append(i)
    return d


def prefix(x):
    return len(set(x)) == 1


def left_factoring(grammar):
    
    new_grammar = dict()
    non_terminals = set()
    for key in grammar:
        common = []
        
        for k, l in groupby(grammar[key]).items():

            if len(l) > 1:
                r = [l[0] for l in takewhile(prefix, zip(*l))]
                common.append(''.join(r))
            elif len(l) == 1:
                new_grammar[key] = list(l[0])
                non_terminals.add(key)

        if not len(common):
            new_grammar[key] = grammar[key]
            non_terminals.add(key)
        else:
            new_alph = f"{key}'"
            if new_alph in grammar:
                new_alph = f"{new_alph}'"
            for i in common:

                if key not in new_grammar:
                    new_grammar[key] = []
                    
                new_grammar[key].append(i + new_alph)
                non_terminals.add(key)

                index = []
                for k in grammar[key]:
                    if k.startswith(i):
                        index.append(k)
                
                string_var = []
                for x in index:
                    string_var.append(x.replace(i, ""))
                if "" in string_var:
                    string_var.pop(string_var.index(""))
                    string_var.append('\u03B5')

                if new_alph not in new_grammar:
                    new_grammar[new_alph] = [x for x in string_var]
                else:
                    new_grammar[new_alph] = [new_grammar[new_alph], [x for x in string_var]]

                non_terminals.add(new_alph)
                new_alph = f"{new_alph}'"


    return new_grammar, non_terminals


if __name__ == "__main__":

    grammar = {"S": ["iEtSeS", "iEtS", "a"], "E": ['b']}
    #grammar = {"A": ["aAB", "aBc", "aAc"]}
    #grammar = {"S": ["A"], "A": ["aB", "aC", "Ad", "Ae"], "B": ["bBc", "f"], "C": ["g"]}
    # grammar = {
    #     "S": ["A"],
    #     "A": ["aBA'", "aCA'"],
    #     "B": ["bBc", "f"],
    #     "C": ["g"],
    #     "A'": ["dA'", "eA'", "\u03B5"]
    # }

    print("")
    for key, rules in grammar.items():
        print(key, "-> ", end="")
        for r in range(len(rules)):
            if r == 0:
                print(rules[r], end=" ")
            else:
                print("|", rules[r], end=" ")

        print("")
    print("\n")

    # print(grammar, "\n\n")

    new_grammar, non_terminals = left_factoring(grammar)

    for key, rules in new_grammar.items():
        print(key, "-> ", end="")
        for r in range(len(rules)):
            if r == 0:
                print(rules[r], end=" ")
            else:
                print("|", rules[r], end=" ")

        print("")
    print("\n")

    print(f"Non-Terminals = {non_terminals}")
