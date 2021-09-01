from texttable import Texttable
import copy
from first_follow import first


def parsing_table (gram, gram_org, terminals, first_sets, follow_sets):
    parsing_table = dict()
    ptable = Texttable(0)
    term = list(terminals.copy())
    if '\u03B5' in term:
        term.pop(term.index("\u03B5"))
    h_list = ["Non Terminals"]
    h_list += [x for x in term]
    ptable.header(h_list)

    for i in gram:
        r_list = dict()
        for j in term:
            parsing_table[(i, j)] = []
            r_list[j] = []
            if j in first_sets[i]:
                ## NEED TO CHECK FIRST FOR gram_org[i] AND DECIDE PARSING TABLE BASED ON THAT
                ## HERE CHECK NEEDS TO BE DONE

                for temp in range(len(gram[i])):
                    temp_gram = copy.deepcopy(gram) 
                    tg = []     
                    if len(gram_org[i]) > 1: 
                        tg = list(gram[i])  
                        k = 0          
                        while (len(tg) != 1):
                            
                            if k == temp:
                                
                                tg = [tg[k]]
#                                print(i, j, k, temp, tg)
                                k -= 1

                            k += 1

                        temp_gram[i] = tg

                    fr = list(set(first(temp_gram, i)))
#                    print(f"{i} ->\t{fr}")
                    if j in fr:
                        temp -= 1
                        if not len(tg):
                            tg = gram[i][0]                       

                        if len(gram_org[i]) > 1:                        
                            tg = [x for sub_x in tg for x in sub_x]
                        
                        tg = gram_org[i][gram[i].index(tg)]

                        parsing_table[(i, j)] += [gram_org[i][gram_org[i].index(tg)]]
                        r_list[j] += [f"{i}->{gram_org[i][gram_org[i].index(tg)]}"]
            else:
                parsing_table[(i, j)] = [""]
                r_list[j] = [""]
        if '\u03B5' in first_sets[i]:
            for j in term:
                if j in follow_sets[i]:

                    if parsing_table[(i, j)] == ['']:
                        parsing_table[(i, j)] = ['\u03B5']
                    else:
                        parsing_table[(i, j)] += ['\u03B5']
                    
                    if r_list[j] == ['']:
                        r_list[j] = [f'{i}->\u03B5']
                    else:
                        r_list[j] += [f'{i}->\u03B5']
            
        ro_list = [i]
        for j in term:
            if len(r_list[j]) == 1:
                ro_list += r_list[j]
            elif len(r_list[j]) > 1:
                ro_list.append(list([x for x in r_list[j]]))

#        print(ro_list)
#        print(parsing_table)
        ptable.add_row(ro_list)
    
    print(ptable.draw())

    return parsing_table


if __name__ == "__main__":
    pass
