# Charles MacKay
# Abhinaya
# python scripts to do matrix operations

import numpy as np
import alpha
import re

# scoring function checks our putative text digram frequency vs the english language digram frequency
def scoreFunction(D,E):
    return np.sum(np.absolute(np.subtract(D,E)))

# remove unwanted characters and spaces
def cleanText(text,spacesOnly):
    if spacesOnly:
        return text.replace(' ','')
    else: #clean everything
        return re.sub('[^A-Za-z]+', '', text)


def normalizeMat(x,msg_len):
    return x/msg_len

def swapRows(matrix,row1,row2):
    matrix[[row1,row2]] = matrix[[row2,row1]] #row swap
    #return matrix

def swapColumns(matrix,col1,col2):
    matrix[:,[col1,col2]] = matrix[:,[col2,col1]] # col swap   
    #return matrix

def getD(putative_text):
    #putative_text=putative_text.upper()
    aNums = alpha.giveAlphabet('u')
    # initialize the D matrix
    D = np.zeros((26, 26))
    # scan the text and update frequency
    for i in range(0,len(putative_text)-1):
        letter1 = putative_text[i]
        letter2 = putative_text[i+1]    
        #print letter1,letter2
        D[aNums[letter1],aNums[letter2]] = D[aNums[letter1],aNums[letter2]] + 1
        #print D[aNums[letter1],aNums[lette r2]]

    fx = np.vectorize(normalizeMat)
    result_array = fx(D,len(putative_text))
    return result_array

# english E
def BuildE():
    f = open("big_text_file.txt",'r')
    data = f.read()
    f.close()
    bigString = cleanText(data,False)

    d = getD(bigString)

    #fx = np.vectorize(normalizeMat)
    #result_array = fx(d,len(bigString))

    #print result_array[:5,:5]

    np.save('digram_freq', d, allow_pickle=True,fix_imports=True)

def getE():
    E = np.load("digram_freq.npy") #, fix_imports=True)
    return E

def getGermanE():
    E = np.load('german_digram_freq.npy')
    return E

def buildGermanE():
    f = open(r'C:\Users\Charl\Dropbox\Graduate School\SJSU 2016\Fall 2016\CS 265\project\scripts\text files\large_german_text.txt','r')
    data = f.read()
    f.close()
    bigString = data.upper() #= cleanText(data,False)

    result_array = getD(bigString)

    print result_array[:5,:5]
    np.savetxt('german_digram_freq.txt',result_array,fmt='%2f')
    np.save('german_digram_freq', result_array, allow_pickle=True,fix_imports=True)

def main():
   print 'hi'
    #buildGermanE()
    #txt = 'ONTHEEVENINGOFTHELASTDAYSMARCHANORDERHADBEENRECEIVEDTHATTHECOMMANDERINCHIEFWOULDINSPECTTHEREGIMENTONTHEMARCHTHOUGHTHEWORDSOFTHEORDERWERENOTCLEARTOTHEREGIMENTALCOMMANDERANDTHEQUESTIONAROSEWHETHERTHETROOPSWERETOBEINMARCHINGORDERORNOTITWASDECIDEDATACONSULTATIONBETWEENTHEBATTALIONCOMMANDERSTOPRESENTTHEREGIMENTINPARADEORDERONTHEPRINCIPLETHATITISALWAYSBETTERTOBOWTOOLOWTHANNOTBOWLOWENOUGHSOTHESOLDIERSAFTERATWENTYMILEMARCHWEREKEPTMENDINGANDCLEANINGALLNIGHTLONGWITHOUTCLOSINGTHEIREYESWHILETHEADJUTANTSANDCOMPANYCOMMANDERSCALCULATEDANDRECKONEDANDBYMORNINGTHEREGIMENTINSTEADOFTHESTRAGGLINGDISORDERLYCROWDITHADBEENONITSLASTMARCHTHEDAYBEFOREPRESENTEDAWELLORDEREDARRAYOFTWOTHOUSANDMENEACHOFWHOMKNEWHISPLACEANDHISDUTYHADEVERYBUTTONANDEVERYSTRAPINPLACEANDSHONEWITHCLEANLINESSANDNOTONLYEXTERNALLYWASALLINORDERBUTHADITPLEASEDTHECOMMANDERINCHIEFTOLOOKUNDERTHEUNIFORMSHEWOULDHAVEFOUNDONEVERYMANACLEANSHIRTANDINEVERYKNAPSACKTHEAPPOINTEDNUMBEROFARTICLESAWLSOAPANDALLASTHESOLDIERSSAYTHEREWASONLYONECIRCUMSTANCECONCERNINGWHICHNOONECOULDBEATEASEITWASTHESTATEOFTHESOLDIERSBOOTSMORETHANHALFTHEMENSBOOTSWEREINHOLESBUTTHISDEFECTWASNOTDUETOANYFAULTOFTHEREGIMENTALCOMMANDERFORINSPITEOFREPEATEDDEMANDSBOOTSHADNOTBEENISSUEDBYTHEAUSTRIANCOMMISSARIATANDTHEREGIMENTHADMARCHEDSOMESEVENHUNDREDMILES'
    #D = getD(txt)
    #E = getE()
    
    #print D[0:3,0:3],"\n"
    #swapColumns(D,0,1)
    #print D[0:3,0:3],"\n"
    #swapRows(D,0,1)
    #print D[0:3,0:3],"\n"

    #print scoreFunction(D,E)
    #np.savetxt('dp_matrix.txt',D,fmt='%2f')

#main()