from texttable import Texttable


def parse(user_input, start_symbol, parsing_table):
    parse_t = Texttable(0)
    h_list = ['Stack', 'Input', 'Action']
    parse_t.header(h_list)

    stack = []
    stack.append("$")
    stack.append(start_symbol)
    user_input += "$"

    flag = 0

    while len(stack) > 1:
        r_list = {}
        top = stack[-1]

        current_input = user_input[0]

        if top == current_input:
            r_list['Stack'] = ""
            for s in stack:
                r_list['Stack'] += s
            r_list['Input'] = user_input
            r_list['Action'] = f'Pop "{current_input}"'

            stack.pop()
            user_input = user_input[1:]
                        
        else:
            key = (top, current_input)

            if key not in parsing_table or parsing_table[key] == ['']:
                flag = 1
                break
            
            value = [x for x in parsing_table[key][0]]

            r_list['Stack'] = ""
            for s in stack:
                r_list['Stack'] += s
            r_list['Input'] = user_input
            r_list['Action'] = f'{top} -> {parsing_table[key][0]}'

            if value[0] != '\u03B5':
                value = value[::-1]
                stack.pop()
                el = len(value)-1
                while True:
                    if "'" not in value:
                        break
                    if value[el] == "'":
                        tmp = el
                        da = value.pop(el)
                        el += 1
                        nt = value.pop(el-1)
                        el += 1
                        value.insert(tmp, f"{nt}{da}")
                        el -= 1
                    el -= 1


                for element in value:
                    stack.append(element)
            else:
                stack.pop()

        ro_list = []
        for x in h_list:
            ro_list.append(r_list[x])

        parse_t.add_row(ro_list)

    if flag == 0:
        parse_t.add_row([stack[0], user_input, 'Accept'])
        print("")
        print(parse_t.draw(), end="\n\n")
    else:
        print(parse_t.draw(), end="\n\n")
        print('String not accepted\n')



if __name__ == "__main__":
    usr_input = "i-*(*i)"
    start_symbol = "E"
    parsing_table = {
        ('E', '$'): [''], 
        ('E', 'i'): ["TE'"], 
        ('E', '-'): [''], 
        ('E', '*'): ["TE'"], 
        ('E', ')'): [''], 
        ('E', '('): ["TE'"], 

        ("E'", '$'): ['ε'], 
        ("E'", 'i'): [''], 
        ("E'", '-'): ['-E'], 
        ("E'", '*'): [''], 
        ("E'", ')'): ['ε'], 
        ("E'", '('): [''], 
        
        ('T', '$'): [''], 
        ('T', 'i'): ['F'], 
        ('T', '-'): [''], 
        ('T', '*'): ['*F'], 
        ('T', ')'): [''], 
        ('T', '('): ['F'], 
        
        ('F', '$'): [''], 
        ('F', 'i'): ['i'], 
        ('F', '-'): [''], 
        ('F', '*'): [''], 
        ('F', ')'): [''], 
        ('F', '('): ['(E)']
    }

    parse(usr_input, start_symbol, parsing_table)
