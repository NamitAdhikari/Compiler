def left_recursion(grammar):
    flag = 0
    pos = 0
    new_grammar = {}
    for key in grammar:
        new_grammar[key] = list()

    for key in grammar.copy():
        subfix = []
        item = grammar[key]
        for prod in item:
            indx = 0
            try:
                if prod[1] == "'":
                    indx = 1
            except IndexError:
                pass
            check = prod[:indx + 1]

            if key == check:
                # print(key, check)
                flag = 1
                pos = pos + 1
                subfix.append(prod[indx + 1:])
            # print(len(subfix))
            if flag == 1:
                # print(item, prod)
                it_list = [x for x in item if x not in [prod, '\u03B5']]
                # print(it_list)
                # for po in item[:item.index(prod)-1]:
                for po in it_list:
                    # print(po, pos)
                    new_grammar[key] = set(new_grammar[key])
                    check = po[0]
                    try:
                        if po[1] == "'":
                            check += po[1]
                    except IndexError:
                        pass
                    # print("check", check)
                    if check not in new_grammar:
                        new_grammar[key].add(po + key + "'")
                    else:
                        #	print(check, key)
                        if check != key:
                            # new_grammar[key].add(item[pos:len(item)][0]+key+"'")
                            new_grammar[key].add(check + key + "'")
                        else:
                            try:
                                if item[pos + 1:len(item)][0][0] != key:
                                    new_grammar[key].add(
                                        item[pos + 1:len(item)][0] + key + "'")
                            except IndexError:
                                if item[pos:len(item)][0][0] != key:
                                    new_grammar[key].add(
                                        item[pos:len(item)][0] + key + "'")
                # print(new_grammar[key])
                new_grammar[key] = list(new_grammar[key])
                if subfix != ['']:
                    new_grammar.update(
                        {key + "'": [x + key + "'" for x in subfix]})
                    new_grammar[f"{key}'"].append(f'\u03B5')
                else:
                    new_grammar[f"{key}'"] = [f'\u03B5']
                flag = pos = 0
    for key in grammar:
        if not len(new_grammar[key]):
            new_grammar[key] = grammar[key]

    return new_grammar


if __name__ == "__main__":
    # grammar = {"A":["ABd","Aa","a"],"B":["Be","b"]}
    # grammar = {"S": ["iEtSeS", "iEtS"], "E": ["b"]}
    # grammar = {"S": ["(L)", "a"], "L": ["L,S", "S"]}
    # grammar = {"E":["E+T","T"], "T":["T*F","F"], "F":["(E)","i"]}
    # grammar = {
    #     "S": ["A"],
    #     "A": ["aB", "aC", "Ad", "Ae"],
    #     "B": ["bBc", "f"],
    #     "C": ["g"]
    # }

    # grammar = {
    #     "S": ["aAc", "bB"],
    #     "A": ["Abc", "Abd", "e"],
    #     "B": ["f", "g"],
    #     "C": ["h", "i"]
    # }

    grammar = {
        "E": ["TE'"],
        "E'": ["E", "e"],
        "T": ["F", "T'"],
        "T'": ["T", "e"],
        "F": ["PF'"],
        "F'": ["*F'", "e"],
        "P": ["(E)", "a", "b", "e"]
    }

    # grammar = {
    #  	"S": ["Aa", "b"],
    # 	"A": ["Ac", "Sd", "\u03B5"]
    # }

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

    # grammar = {
    #     "S": ["aAc", "bB"],
    #     "A": ["Abc", "Abd", "e"],
    #     "B": ["f", "g"],
    #     "C": ["h", "i"]
    # }

    lr_grammar = left_recursion(grammar)

    print("\nLR Grammar:")
    for key, rules in lr_grammar.items():
        print(key, "-> ", end="")
        for r in range(len(rules)):
            if r == 0:
                print(rules[r], end=" ")
            else:
                print("|", rules[r], end=" ")

        print("")
    print("")
