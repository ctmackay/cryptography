import string
# build an alphabet dictionary

def giveAlphabet(case):
    alphabet = dict()
    if case.upper() == 'U':
        for i in range (0,26):
            letter = string.ascii_uppercase[i]
            alphabet[letter] = i
        return alphabet
    else:
        for i in range (0,26):
            letter = string.ascii_lowercase[i]
            alphabet[letter] = i
        return alphabet

def giveAlphaList(case):
    alpha_list = []
    if case.upper() == 'U':
        for i in range (0,26):
            letter = string.ascii_uppercase[i]
            alpha_list.append(letter)
        return alpha_list
    else:
        for i in range (0,26):
            letter = string.ascii_lowercase[i]
            alpha_list.append(letter)
        return alpha_list
