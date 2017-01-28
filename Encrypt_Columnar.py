# COLUMNAR TRANSPOSITION CIPHER ENCRYPTION
import numpy as np
from math import ceil
import KeyWeights
import CryptMatrixTools as cmt

def cipher(key_obj_list,ch_matrix):
    r,c = ch_matrix.shape # read in the decryption matrix shape
    str_to_return ='' #build an empty string
    for k in key_obj_list: # iterate through the key list
        tCol = k.position # read one column at a time, depending on key sequence
        for i in range(0,r):
            str_to_return += ch_matrix[i,tCol] # read downwards columnwise
    return str_to_return

def putInGroupsOfFive(cipher_text,useNullChar):
    if useNullChar == False: #if using ICT, we remove the nulls
        cipher_text = cmt.cleanText(cipher_text,False)
    i=0
    tmp=''
    for l in cipher_text:
        tmp += l
        i=i+1
        if i %5 == 0:
            tmp += ' '    
    return tmp

#encrypt by ordering the plaintext into a indexible matrix
def buildTransMatrix(key,plain_text):
    msg_len = len(plain_text)
    # put the plaintext into an array based on keysize
    columns = len(key) # find how many columns 
    rows = int(ceil(1.0*msg_len/len(key))) # how many rows are needed
    f_array = np.chararray((rows,columns)) #build blank matrix
    flag = False
    k=0 # plaintext index
    i=0 # row index
    while True:
        if flag == True:
            break
        for j in range(0,len(key)): #iterate through the entire row
            if k >= msg_len: #if we've run out of text for that row, put a null character
                flag = True #this means we're done building the matrix
                f_array[i,j]='Z' # null character 
            else:
                f_array[i,j]=plain_text[k]
                k=k+1
        i=i+1

    return f_array

def encryptPlaintext(plain_text,key,useNull):
    #prepare text
    plain_text = cmt.cleanText(plain_text,False)
    plain_text = plain_text.upper()

    # build the key parameters
    key_len = len(key) 
    key_obj_list,key_list = KeyWeights.getWeightedKeyList(key.upper())

    # ecnrypt the message
    f_array = buildTransMatrix(key,plain_text)
    encoded_msg = cipher(key_obj_list,f_array)

    # return encrypted text
    if useNull:
        return putInGroupsOfFive(encoded_msg,True)
    else:
        return putInGroupsOfFive(encoded_msg,False)

# main starting point
def main():

    plain_text = 'The goalkeepers are the only players allowed to touch the ball with their hands or arms while it is in play and only in their penalty area'
    #plain_text = 'WE ARE DISCOVERED. FLEE AT ONCE'

    key = 'LONGKEYLEN'

    fromFile = False
    filename = r"C:\Users\Charl\Dropbox\Graduate School\SJSU 2016\Fall 2016\CS 265\project\scripts\text files\my_text2.txt"


    if fromFile:
        with open(filename,'r') as f:
            plain_text = f.read()
   
    print plain_text
    print key
    print encryptPlaintext(plain_text,key,True)
#execute main
main()
