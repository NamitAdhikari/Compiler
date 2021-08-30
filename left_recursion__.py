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
            try:
                if prod[1] == "'":
                    check = prod[:2]
                else:
                    check = prod[0]
            except IndexError:
                check = prod[0]

            if key == check:
                #				print(key, prod, item)
                flag = 1
                pos = pos + 1
                subfix.append(prod[1:len(prod)])
            #				print(flag, subfix, pos)
            if flag == 1:
                #				print(key, prod, item)
                # print(item[:item.index(prod)-1], item[pos:len(item)][0])
                for po in item[:item.index(prod)-1]:
                    #					print(po)
                    #					print(item[:item.index(prod)-1])
                    #print("set_item_pos = ", set([item[pos:len(item)][0]+key+"'"]))
                    new_grammar[key] = set(new_grammar[key])
                    #					print(f"new_grammar[key] 1 = {new_grammar[key]}")
                    if po[0] not in new_grammar:
                        new_grammar[key].add(po+key+"'")
                    else:
                        if po[0] != key:
                            new_grammar[key].add(item[pos:len(item)][0]+key+"'")
                        else:
                            try:
                                new_grammar[key].add(item[pos+1:len(item)][0]+key+"'")
                            except IndexError:
                                new_grammar[key].add(item[pos:len(item)][0]+key+"'")
                #					print(f"new_grammar[key] 2 = {new_grammar[key]}")
                new_grammar[key] = list(new_grammar[key])
                new_grammar.update({key+"'":[x+key+"'" for x in subfix]})
                new_grammar[f"{key}'"].append(f'\u03B5')
                flag=pos=0
    for key in grammar:
        if not len(new_grammar[key]):
            new_grammar[key] = grammar[key]

    return new_grammar


if __name__ == "__main__":
    #grammar = {"A":["ABd","Aa","a"],"B":["Be","b"]}
    #grammar = {"S": ["iEtSeS", "iEtS"], "E": ["b"]}
    #grammar = {"S": ["(L)", "a"], "L": ["L,S", "S"]}
    #grammar = {"E":["E+T","T"], "T":["T*F","F"], "F":["(E)","i"]}
    grammar = {
        "S": ["A"],
        "A": ["aB", "aC", "Ad", "Ae"],
        "B": ["bBc", "f"],
        "C": ["g"]
    }

    grammar = {
        "S": ["aAc", "bB"],
        "A": ["Abc", "Abd", "e"],
        "B": ["f", "g"],
        "C": ["h", "i"]
    }

    # grammar = {
    #     "E": ["TE'"],
    #     "E'": ["E", "e"],
    #     "T": ["F", "T'"],
    #     "T'": ["T", "e"],
    #     "F": ["PF'"],
    #     "F'": ["*F'", "e"],
    #     "P": ["(E)", "a", "b", "e"]
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
