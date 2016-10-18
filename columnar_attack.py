import itertools
import CryptMatrixTools as cmt
import Decrypt
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

def geneticAlgorithmAttack(cipher_text,key_length,max_iterations,isEnglish):
    universal_set = generateRandomKey(key_length)
    generation=[] # empty list of key objects with key value and score
    #build a pool of N random keys
    N = key_length * 30
    for i in range(0,N):
        #rand_key_length = random.randint(min_key_length,max_key_length)
        rand_key = generateRandomKey(key_length)
        kso = KeyScore(rand_key,0) # add our new key to the list, with inital score of 0
        if kso not in generation:
            generation.append(kso)
    if isEnglish:
        E = cmt.getE()
    else:
        E = cmt.getGermanE()
    genNumber=1
    while genNumber < max_iterations:
        for k in generation:
            if k.score == 0:
                putative_text = Decrypt.decryptMyText(cipher_text,k.key,False)
                D = cmt.getD(putative_text)
                k.updateScore(cmt.scoreFunction(D,E))

        generation_sorted = sorted(generation, key = lambda ko: ko.score,reverse=False) # sort the list based on best scores
    
        #take top N best keys, and mate with eachother
        #max=int(len(generation_sorted)*0.25)
        top_surviving = []
        top_surviving = generation_sorted[:N]
        generation[:] = []# top_surviving #clear out the old gen, and fill in the new parents+children
        for i in range(0,len(top_surviving)):
            parent1 = top_surviving[i].key # take the parents keys
            #parent2 = top_surviving[i+1].key
            pivot_point = random.randint(0,key_length) #find a pivot point for generation of new child
            child = parent1[:pivot_point]

            #spawn a new child
            while len(child) < key_length:
                parent2 = list(set(universal_set) - set(child))  # take only from parent2 what is not already in child
                parent_num = random.choice(parent2)
                if (parent_num not in child):
                    child.append(parent_num)
            if top_surviving[i] not in generation:
                generation.append(top_surviving[i]) # add the parents back in the pool
           # if top_surviving[i+1] not in generation:
             #   generation.append(top_surviving[i+1])
            if child not in generation:
                generation.append(KeyScore(child,0)) #add the new child  in the pool

        genNumber+=1
    #for the last generation
    if genNumber == max_iterations:
        for k in generation:
            if k.score == 0:
                putative_text = Decrypt.decryptMyText(cipher_text,k.key,False)
                D = cmt.getD(putative_text)
                k.updateScore(cmt.scoreFunction(D,E))
        generation_sorted = sorted(generation, key = lambda ko: ko.score,reverse=False) # sort the list based on best scores
    return generation_sorted[0:10] #return top 5 best keys

def main():
    with open(r'C:\Users\Charl\Dropbox\Graduate School\SJSU 2016\Fall 2016\CS 265\project\scripts\text files\my_crypt.txt') as f:
        mole1 = f.read()
    #cipher_text = 'ENEAC DBCTE NCOSH MTCGO TENAE EOEHT OTESO AGOTC TUOEB IMSSE EARTN TIYEW WOOGE EENEW PICNI NOSES TUAPM RUAKN RHMSF RNRCT ESAEF EDODO HDCOH CIHRO VRLDW EENYN ANBIS CDHLD UMUEO YLIIY AATBR SALEE TAOCN CGNOA IHESR SHFNS NBSTT ALEEO ENOAM ODEEE IMITI AHEHD TNTTA OARET MIFIT GOAOE ORRLT ILNDE AHTOE NIETD DNTTH AOERT INEOR LIWTB LNWOT DFWIC KNNNL LTLTY LDTOC DLEED MGGID SLSLD BITTB PTLRA OAEWE LDTVT DSNAN CINNE YLEAE HANTU HOWAN EASNE PHIUF LSDTD AELIT OICEB SSAHI OEAMO EEHEN TATIL NRTPD SHBST TOANE TROER ENEFS MNHNV TMRED CETMH HSOEC OGAAN UNWRO RIHDO SEOAE TTCDP TGIDR PPTLE OOAON OLATM REEAA LTICG EIANC YNATR EYNET AEGIR WDNSH YENEE RWSNF NPNUE UNYIE OHLAO TLLDH LTMIF KTFEH UVNNA VATON OCLNS LSRNC SCNIN DAATT DORHE ORLTF SEFFG AAOIE DDSTS YSCSA RNASV DLHIH DRRDE DHANW NTINR UWFDE EHMCD TSREH PTMNR IEASI WELMR EHMPO NIETA TOONL UHITE LHEDD INOHO HEEJS MOECD CAOTI NOTIO YIETM HEREL EYTNA HWAHY ETETP NELND LRWIR DAENC ONERO VDRCH DRSEN MAEOA HIYWY RANNH CEETT EETTL ETISI COOUH MCDIE EEBAE UHRMR DGHCM NESEG LYHEE EHCDH UPEEH HHRHR ORRNM REISH TWBRO RWIAL NEAOA TERNR DHCHS SRTTT WHSRR TMETN LGGGU IIWHT NAMSL NODNE ETTAG DRHNL RDOSA RAFOM HMIES AYNEA ASIAS OEASO UTEOE IOENS LFNME RNKCP EETAP LSRHS NUCEW OUTTE OOSMA TSWHU DWDNT RNMRS FTAON NDAAI AHMDE SUMOV OASAR EIAOE ILERN ETTDE WTTET MAQOE EREEC RNADC TBNTN NONET AEEIA ABTOH BESOS AYARM GEAHW TNRHE ADNAC ADNBI RNEHG DEOAO ACARE WDRTU EOKSA DDBAR PCHTN STXLA RTPDM REORI HDOEA ATENK PDRIW AAOSE OEMER HOLEW SFLBO NHBEO TEAUY OETMF PRENT OIBUN STEEM DENI'
    #cipher_text = 'EVLNE ACDTK ESEAQ ROFOJ DEECU WIREE'
    cipher_text = cmt.cleanText(mole1,False)
    print cipher_text
    print len(cipher_text)
    #print getCipherTextDividers(len(cipher_text),100)
    for i in range(5,7):
        keyz = geneticAlgorithmAttack(cipher_text,i,100,True)
        for k in keyz:
            print k.key, k.score
            print Decrypt.decryptMyText(cipher_text,k.key,False)

    i = 0
    for k in keyz:
        print k.key, k.score
        print Decrypt.decryptMyText(cipher_text,k.key,False)
        i=i+1
        if i >10:
            break

main()
