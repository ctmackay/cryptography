import itertools
import CryptMatrixTools as cmt
import Decrypt_Columnar as Decrypt
import random
#import math
from copy import deepcopy

class KeyScore(object):
    def __init__(self,k,s):
        self.key = k
        self.score = s
    def updateScore(self,s):
        self.score = s



def buildInitalKey(key_size):
    key=[]
    for i in range(key_size):
        key.append(i)

    return key

def permuateAllKeys(key_list):
    perm_keys = []
    for permutation in itertools.permutations(key_list):
        perm_keys.append(permutation)
    return perm_keys

def generateRandomKey(key_length):
    key_seed=list() #empty key
    for i in range(0,key_length): #build a custom sized key
        key_seed.append(i)
    random.shuffle(key_seed) #randomize
    return key_seed

# check if key is already in the list.
# faster than rescoring every key 
def contains(keylist, filter):
    for keyobject in keylist:
        if keyobject.key == filter:
            return True
    return False; #could not find key


def bruteForceAttack(cipher_text,key):
    pKeys = permuateAllKeys(key)
    kScoreList = []

    max_score = 0
    i = 0
    max_index=0
    for k in pKeys:
        putative_text = Decrypt.decryptMyText(cipher_text,k,False)
        D = cmt.getD(putative_text)
        #print D[:5,:5]
        E = cmt.getE()
        score = cmt.scoreFunction(D,E)
        #if score > max_score:
        #    max_score = score
        #    max_index=i
        kso = KeyScore(k,score)
        kScoreList.append(kso)
        #i = i+1
    #return max_score,max_index,pKeys
    return kScoreList

def tabuSearch(cipher_text,key):
    print 'in progress'

#get the key lengths that divide the text into equal number of columns (only works with regular column transposition with nulls)
def getCipherTextDividers(ct_length,max_key_length):
    possible_lengths=[] #initalize empty set
    for i in range(2,max_key_length+1): #go from 2 to max key length
        if ct_length % i == 0:
            possible_lengths.append(i)

    return possible_lengths


# function to crack columnar transposition cipher by keeping the fittest keys.
# high fitness is a score that has high similiarity to the digram frequency matrix in the encoded language
def geneticAlgorithmAttack(cipher_text, key_length, max_iterations, isEnglish):
    universal_set = set(generateRandomKey(key_length))
    generation=[] # empty list of key objects with key value and score

    #build a pool of N random keys
    N = key_length * 30
    for i in range(0,N):
        #rand_key_length = random.randint(min_key_length,max_key_length)
        rand_key = generateRandomKey(key_length)
        kso = KeyScore(rand_key,0) # add our new key to the list, with inital score of 0
        #if not contains(generation,rand_key): #unique keys only
        generation.append(kso)


    #choose which scoring function we will be using
    if isEnglish:
        E = cmt.getE()
    else:
        E = cmt.getGermanE()


    genNumber=1
    while genNumber < max_iterations:
        for k in generation:
            if k.score == 0: # if the score is 0, we need to rescore
                putative_text = Decrypt.decryptMyText(cipher_text,k.key,False)
                D = cmt.getD(putative_text)
                k.updateScore(cmt.scoreFunction(D,E))
                #print k.key,k.score

        generation_sorted = sorted(generation, key = lambda ko: ko.score,reverse=False) # sort the list based on best scores
    
        #take top N best keys, and mate with eachother
        #max=int(len(generation_sorted)*0.25)
        top_surviving = []
        top_surviving = generation_sorted[:N]
        generation[:] = [] #clear out the old gen, and fill in the new parents+children
        generation = top_surviving[:]

        for i in range(0,len(top_surviving)):
            parent1 = top_surviving[i].key # take the parents keys
            #parent2 = top_surviving[i+1].key
            pivot_point = random.randint(0,key_length) #find a pivot point for generation of new child
            child = parent1[:pivot_point] # take a portion of the key from parent 1


            #spawn a new child using a mutation of missing parts
            parent2 = list(universal_set - set(child))  # take only from parent2 what is not already in child
            random.shuffle(parent2) # scramble DNA
            child = child + parent2 # create new children using mutated key DNA
            assert (len(child) == key_length), "Child key has incorrect length"

            if not contains(generation,child): # only add if child is unique
                generation.append(KeyScore(child,0)) #add the new child  in the pool

        genNumber+=1

    #for the last generation, score and sort 1 more time. 
    if genNumber == max_iterations:
        for k in generation:
            if k.score == 0:
                putative_text = Decrypt.decryptMyText(cipher_text,k.key,False)
                D = cmt.getD(putative_text)
                k.updateScore(cmt.scoreFunction(D,E))
        generation_sorted = sorted(generation, key = lambda ko: ko.score,reverse=False) # sort the list based on best scores

    return generation_sorted[0:10] #return top 10 best keys

def main():
    #with open(r'C:\Users\Charl\Dropbox\Graduate School\SJSU 2016\Fall 2016\CS 265\project\scripts\text files\my_crypt.txt') as f:
        #mole1 = f.read()

    cipher_text = 'ARLWT HSLAN LZEHE TBEAT NEAZG SYLCI NHPYN ZOAPO HTDIL IAZTP OSTLR MSORE KTYDE HRIAH YZERL LUWAW NLEZE EROAI RIDIR ZHENA OLHSI NPALE AEHTO EYTTZ'
    #cipher_text = 'EVLNE ACDTK ESEAQ ROFOJ DEECU WIREE'
    #cipher_text = cmt.cleanText(mole1,False)
    print cipher_text
    print len(cipher_text)
    #print getCipherTextDividers(len(cipher_text),100)


    key_len = len('LONGKEYLEN') # cheating to get the key length

    #for i in range(5,5):
    keyz = geneticAlgorithmAttack(cipher_text,key_len,100,True) # 100-1000 iterations seems ok. when you have too many iterations, the score goes lower, but the real answer might be higher.
    for k in keyz:
        print k.key, k.score
        print Decrypt.decryptMyText(cipher_text,k.key,False)

    #i = 0
    #for k in keyz:
    #    print k.key, k.score
    #    print Decrypt.decryptMyText(cipher_text,k.key,False)
    #    i=i+1
    #    if i >10:
    #        break

main()
