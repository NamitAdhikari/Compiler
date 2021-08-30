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
#    terminals = set()
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
                #new_alph = f"{key}'"
#                print(key + "->" + i + new_alph)

                if key not in new_grammar:
                    new_grammar[key] = []
                    
                new_grammar[key].append(i + new_alph)
                non_terminals.add(key)

                index = []
                for k in grammar[key]:
                    if k.startswith(i):
                        index.append(k)
                
#                print(new_alph + "->", end="")

                string_var = ""
                for j in index[:-1]:
                    string = j.replace(i, "", 1) + "|"
                    if string == "|":
#                        print("\u03B5", "|", end="")
                        string_var += f"\u03B5 |"
                    else:
#                        print(string, end="")
                        string_var += string
                
                string = index[-1].replace(i, "", 1) + "|"
                if string == "|":
#                    print("\u03B5", "|", end="")
                    string_var += f"\u03B5 |"
                else:
#                    print(string, end="")
                    string_var += string
#                print("")
                #print(f"string_var = {string_var}")
                if new_alph not in new_grammar:
                    new_grammar[new_alph] = [x for x in string_var.rstrip("|").rstrip().split('|')]
                else:
                    new_grammar[new_alph] = [new_grammar[new_alph], [x for x in string_var.rstrip("|").rstrip().split('|')]]

                non_terminals.add(new_alph)
                new_alph = f"{new_alph}'"

    #print(new_grammar)
    #print(f"\n\n{new_grammar}\n")
    return new_grammar, non_terminals


if __name__ == "__main__":

    #grammar = {"S": ["iEtSeS", "iEtS", "a"], "E": ['b']}
    #grammar = {"A": ["aAB", "aBc", "aAc"]}
    #grammar = {"S": ["A"], "A": ["aB", "aC", "Ad", "Ae"], "B": ["bBc", "f"], "C": ["g"]}
    grammar = {
        "S": ["A"],
        "A": ["aBA'", "aCA'"],
        "B": ["bBc", "f"],
        "C": ["g"],
        "A'": ["dA'", "eA'", "\u03B5"]
    }

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
