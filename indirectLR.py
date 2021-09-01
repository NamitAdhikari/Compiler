import copy
from first_follow import break_grammar

from left_recursion__ import left_recursion

def checkForIndirect(grammar, a, ai):
    if ai not in grammar:
        return False
    if a == ai:
        return True
    for i in grammar[ai]:
        check = i[0]
        try:
            if i[1] == "'":
                check += "'"
        except IndexError:
            pass
        if check == ai:
            continue
        if check in grammar:
            if checkForIndirect(grammar, a, check):
                return True
            else:
                continue
    return False


def replace(grammar, term, r_term):
    # print(term, r_term)
    try:
        temp = grammar[term]
    except KeyError:
        return grammar
    newTemp = []
    for i in temp:
        check = i[0]
        try:
            if i[1] == "'":
                check += "'"
        except IndexError:
            pass
        if check == r_term:
            for k in grammar[check]:
                #  print(k)
                t = ""
                t += k
                t += i[1:]
                newTemp.append(t)
        else:
            newTemp.append(i)
    grammar[term] = newTemp
    #  print(grammar)
    return grammar


def removeLR(grammar):
    new_grammar = {}

    for key in grammar:
        new_grammar[key] = []

    key_list = []
    for i in range(0, len(grammar), 1):
        ai = list(grammar.keys())[len(grammar)-i-1]
        key_list.append(ai)
        for j in range(0, len(grammar[ai])):
            #  print(grammar[ai], j)
            aj = grammar[ai][j][0]
            try:
                if grammar[ai][j][1] == "'":
                    aj = aj + "'"
            except IndexError:
                pass
            if ai != aj:
                flag = checkForIndirect(grammar, ai, aj)
                # print(flag, ai, aj)
                if aj in grammar and flag:
                    new_grammar = replace(grammar, ai, aj)

    for key in new_grammar:
        if not len(new_grammar[key]):
            new_grammar[key] = grammar[key]

    #    print("grammar after inRe\n", new_grammar)

    new_grammar = left_recursion(new_grammar)

    #   print("grammar after lr\n", new_grammar)
    return new_grammar


if __name__ == "__main__":

    from first_follow import break_grammar

    gram = {
        "S": ["A"],
        "A": ["aB", "aC", "Ad", "Ae"],
        "B": ["bBc", "f"],
        "C": ["g"]
    }

    # gram = {
    #     "S": ["Aa", "b"],
    #     "A": ["Ac", "Sd", "\u03B5"]
    # }

    gram = {
        "E": ["TE'"],
        "E'": ["E", "e"],
        "T": ["F", "T'"],
        "T'": ["T", "e"],
        "F": ["PF'"],
        "F'": ["*F'", "e"],
        "P": ["(E)", "a", "b", "e"]
    }

    #gram = {"S": ["iEtSeS", "iEtS"], "E": ["b"]}

    print("gram\n", gram)

    result = removeLR(gram)

    br_gr = break_grammar(result)
    print(br_gr)

    for x, y in result.items():
        print(f'{x} -> {y}')
