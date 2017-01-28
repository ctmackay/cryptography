# Simple mono-alphabetic substituion cipher 
# key consists of a 26 letter mapping (one to one)
# Charles MacKay  (charlestmackay@gmail.com)

import alpha
import CryptMatrixTools as cmt
import random
import string
import copy
import numpy as np
import time


def encrypt(plain_text,key):
    plain_text = cmt.cleanText(plain_text,False) #remove punctutation and non alpha chars
    plain_text = plain_text.upper() # convert to uppercase
    cipher_text = '' #initalize empty string
    
    alf = alpha.giveAlphabet('u') #return a A-Z list with numbered indicies
    # if key is not in list format
    newMapping = []
    for k in key:
        newMapping.append(k) # create a new mapping based on the key

    #iterate over the entire plain text
    for p in plain_text:
        # replace letter in plain text, using the letter mapping in the key
        cipher_text += newMapping[ alf[p]] 

    return cipher_text

def decrypt(cipher_text,key):
    alf = alpha.giveAlphabet('u') # Alphabet to number list (ie. A=0, B=1)
    regAlpha = alpha.giveAlphaList('u') # Number to alphabet list (ie. 0=A, 1=B)
   
    # make the key indexible to map to the actual alphabet
    key_dict = dict()
    i = 0
    for k in key:
        key_dict[k] = i
        i = i+1
    
    # decrypt plain text using the key to alphabet mapping
    plain_text = '' 
    #iterate over entire plaintext
    for c in cipher_text:
        # map the key position to the position in the normal alphabet
        plain_text += regAlpha[key_dict[c]]

    return plain_text

def letterFrequencyAnalysis(text):
    letterFreqList = []
    for i in range(0,26):
        cur_letter = string.ascii_uppercase[i]
        count = text.count(cur_letter)
        tupl = (cur_letter,count,i)
        letterFreqList.append(tupl)
    return letterFreqList

def listOccurances(letterFreqList,text_length):
    print "list sorted by frequency of occurance"
    sorted_list = sorted(letterFreqList,key=lambda x: x[1],reverse=True)

    for i in range(0,26):
        print sorted_list[i][0],
        print sorted_list[i][1],
        print "%.2f"%((sorted_list[i][1]*1.0/text_length)*100),
        print '%'


def genKeyBasedOnLetterFreq(letterFreqList):
    # ordered list of most common english letters
    ordered_list = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D', 'L', 'C', 'U', 'M', 'W', 'F', 'G', 'Y', 'P', 'B', 'V', 'K', 'J', 'X', 'Q', 'Z']

    #sort our letter frequency analysis so we get the most common first
    sorted_list = sorted(letterFreqList,key=lambda x: x[1],reverse=True)
 
    alf = alpha.giveAlphabet('u')
    # generate a blank key so we can index the positions
    key = []
    for i in range(0,26):
        key.append('')

    # fill in our key based off the most common frequency words
    i = 0
    for o in ordered_list:
        key[alf[o]] = sorted_list[i][0]
        i=i+1

    return key

def generateRandomKey():
    seed='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    key_list = list(seed)
    random.shuffle(key_list)
    return key_list

def geneticAlgorithmAttack(cipher_text, iterations):
    key = genKeyBasedOnLetterFreq(letterFrequencyAnalysis(cipher_text))
    #key = generateRandomKey()
    print "inital guess for key",key
    E = cmt.getE() #Construct 𝐸 matrix based on English language text
    decrypted_text = decrypt(cipher_text,key) #Decrypt the ciphertext with the putative key and construct 𝐷 matrix
    D = cmt.getD(decrypted_text)
    score = cmt.scoreFunction(D,E)
    print "inital score from decryption with key", score
    print "inital decryption with key", decrypted_text
    i = 0
    while i < iterations:
        i=i+1
        tempkey = copy.deepcopy(key)
        Dp = np.copy(D)

        a = random.randint(0,25)
        b = random.randint(0,25)
        tempkey[a],tempkey[b] = tempkey[b],tempkey[a] # Swap element a and b in tempkey.
        cmt.swapRows(Dp,a,b) #swap rows and columns in the D' matrix
        cmt.swapColumns(Dp,a,b)
        newscore = cmt.scoreFunction(Dp,E) #score with new D'

        if newscore < score:
            D = np.copy(Dp)
            key = copy.deepcopy(tempkey) # if improved, save permutation
            score = newscore

    print key,score
    decrypted_text = decrypt(cipher_text,key)
    print decrypted_text

def jakobsenAttack(cipher_text):
    # indices in my key
    a = 0 
    b = 0
    key = genKeyBasedOnLetterFreq(letterFrequencyAnalysis(cipher_text)) #Get initial Key based on letter frequencies in the ciphertext.
    print "inital guess for key",key
    E = cmt.getE() #Construct E matrix based on English language text
    decrypted_text = decrypt(cipher_text,key) #Decrypt the ciphertext with the putative key and construct D matrix
    D = cmt.getD(decrypted_text)
    score = cmt.scoreFunction(D,E)
    print "inital score from decryption with key", score

    while b != 25:
        if (a+b) <= 25:
            tempkey = copy.deepcopy(key)
            Dp = np.copy(D)
            tempkey[a],tempkey[b] = tempkey[b],tempkey[a] # Swap element a and b in tempkey.
            cmt.swapRows(Dp,a,b) #swap rows and columns in the D' matrix
            cmt.swapColumns(Dp,a,b)
            newscore = cmt.scoreFunction(Dp,E) #score with new D'
            if newscore < score:
                score = newscore
                key = copy.deepcopy(tempkey)
                D = np.copy(Dp)
                a=0
                b=0
            else:
                tempkey = copy.deepcopy(key)
                Dp = np.copy(D)
                a = a+1
        else:
            a=0
            b=b+1
            tempkey = copy.deepcopy(key)
            Dp = np.copy(D)

    decrypted_text = decrypt(cipher_text,key)
    return decrypted_text


def main():
    #plain_text = 'thisistotestthesimplesubstitutioncipher'
#    print plain_text
    key = ['K', 'M', 'J', 'Y', 'X', 'A', 'I', 'B', 'R', 'F', 'L', 'T', 'H', 'E', 'O', 'U', 'W', 'D', 'V', 'G', 'S', 'Q', 'P', 'N', 'C', 'Z']
    #print key

    # sample plain text. 
    plain_text = 'A letter. For me. That was something of an event. The crisp-cornered envelope, puffed up with its thickly folded contents, was addressed in a hand that must have given the postman a certain amount of trouble. Although the style of the writing was old-fashioned, with its heavily embellished capitals and curly flourishes, my first impression was that it had been written by a child. The letters seemed untrained. Their uneven strokes either faded into nothing or were heavily etched into the paper.'
    plain_text = cmt.cleanText(plain_text,False) #clean up, remove punctuations
    plain_text = plain_text.upper() # convert to caps
    print 'plaintext', plain_text 
    print 'length of text', len(plain_text)

    cipher_text = encrypt(plain_text,key) # encrypt plaintext using key
    print 'encrypted text', cipher_text
    print 'digram frequency score', cmt.scoreFunction(cmt.getD(plain_text),cmt.getE()) # print score of actual text


    #analyzed_text = letterFrequencyAnalysis(cipher_text)
    #listOccurances(analyzed_text,len(cipher_text))

    #possible_key = genKeyBasedOnLetterFreq(analyzed_text)
    #print possible_key

    #decrypted_text = decrypt(cipher_text,possible_key)
    #print decrypted_text

    #start_time = time.time()
    #generalHillClimbAttack(cipher_text)
    #print ('general hill climb attack took %s seconds'%(time.time() - start_time))

    print '\n\nperforming attack...\n'
    # perform attack and time
    start_time = time.time()
    #print geneticAlgorithmAttack(cipher_text, 2000)
    print jakobsenAttack(cipher_text)
    print ('jackobsen attack took %s seconds'%(time.time() - start_time))
main()