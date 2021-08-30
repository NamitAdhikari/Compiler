def gr_mod(grammar):
    new_gram = dict()
    for line in grammar.split('\n'):
        line_split = line.split('->')
        lhs = ""
        rhs = []
        for rl in line_split:
            print("rl = ",rl)
            if not line_split.index(rl):
                lhs = rl.strip()
            else:
                for x in rl.split('|'):
                    rhs.append(x.strip())
            new_gram[lhs] = rhs

    print(new_gram)
    return new_gram



if __name__ == "__main__":
    grammar = open("grammar", "r").read()
    gr_mod(grammar)