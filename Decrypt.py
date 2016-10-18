# COLUMNAR TRANSPOSITION CIPHER DECRYPTION
import math
import numpy as np
import CryptMatrixTools as cmt
import KeyWeights as kw

# this function will build a decrypted matrix by ordering the cipher text
# into the correct columns.
# it can decrypt an RCT or an ICT ciphertext using provided key
# (ICT - irregular column transposition)
def buildDecryptMatrix(cipher_text,key):
    #set up matrix parameters
    rows = int(math.ceil(1.0*len(cipher_text) / len(key)))
    columns =  len(key)
    numOfLongColumns =  len(cipher_text) % len(key)
    numOfShortColumns = len(key) - numOfLongColumns
    shortColLength = rows

    if numOfLongColumns > 0: # only if non-nulls are used (ICT)
        longColLength = rows
        shortColLength = rows - 1

    dMat = np.chararray((rows,columns)) # decryption matrix
    dMat[:] =''
    # fill in the short columns first according to key order
    # then fill in the remaining long columns according to key order
    l = 0 # letter counter
    c = 0 # col counter
    while l < len(cipher_text): # main loop
        while c < columns: # col loop
            colIndex = key[c]
            #check if we are in a short or long column
            if colIndex >= (columns - numOfShortColumns): # we read from left to right, so the last (#cols-#shorts) columns are short
                for i in range(shortColLength):
                    dMat[i,colIndex] = cipher_text[l]
                    l = l+1
                c = c+1
            else:
                #this column is long
                for i in range(longColLength):
                    dMat[i,colIndex] = cipher_text[l]
                    l = l+1
                c = c+1
                
    return dMat

# turn into a single string by reading entire matrix
def getDecryptedText(dMat): 
    tmp=''
    r,c = dMat.shape
    for i in range(r):
        for j in range(c):
            tmp += dMat[i,j]
    return tmp


# enter a cipher text and key
# the key can be an alphabetical word such as 'ZEBRAS'
# or it can be a numerical list in the form [4, 2, 1, 3, 5, 0]
def decryptMyText(cipher_text,key,keyIsAlphabetical):
    cipher_text = cmt.cleanText(cipher_text,True) # remove spaces first
    key_list=key

    # translate an english word into a numerical ordered list
    if keyIsAlphabetical: 
        kobjs, key_list = kw.getWeightedKeyList(key) 

    decrypted_matrix =  buildDecryptMatrix(cipher_text,key_list)
    return getDecryptedText(decrypted_matrix)

# testing the main functionality here
def main():
    key = 'FLOWER'
    cipher_text = 'EVLNW IREEE SEAAC DTDEE CROFO'
    #print 'decrypted text: ', decryptMyText(cipher_text,key,True)
    #key = 'ZEBRAS'
    #cipher_text = 'EVLNA CDTES EAROF ODEEC WIREE'
    #cipher_text = 'ENEAC DBCTE NCOSH MTCGO TENAE EOEHT OTESO AGOTC TUOEB IMSSE EARTN TIYEW WOOGE EENEW PICNI NOSES TUAPM RUAKN RHMSF RNRCT ESAEF EDODO HDCOH CIHRO VRLDW EENYN ANBIS CDHLD UMUEO YLIIY AATBR SALEE TAOCN CGNOA IHESR SHFNS NBSTT ALEEO ENOAM ODEEE IMITI AHEHD TNTTA OARET MIFIT GOAOE ORRLT ILNDE AHTOE NIETD DNTTH AOERT INEOR LIWTB LNWOT DFWIC KNNNL LTLTY LDTOC DLEED MGGID SLSLD BITTB PTLRA OAEWE LDTVT DSNAN CINNE YLEAE HANTU HOWAN EASNE PHIUF LSDTD AELIT OICEB SSAHI OEAMO EEHEN TATIL NRTPD SHBST TOANE TROER ENEFS MNHNV TMRED CETMH HSOEC OGAAN UNWRO RIHDO SEOAE TTCDP TGIDR PPTLE OOAON OLATM REEAA LTICG EIANC YNATR EYNET AEGIR WDNSH YENEE RWSNF NPNUE UNYIE OHLAO TLLDH LTMIF KTFEH UVNNA VATON OCLNS LSRNC SCNIN DAATT DORHE ORLTF SEFFG AAOIE DDSTS YSCSA RNASV DLHIH DRRDE DHANW NTINR UWFDE EHMCD TSREH PTMNR IEASI WELMR EHMPO NIETA TOONL UHITE LHEDD INOHO HEEJS MOECD CAOTI NOTIO YIETM HEREL EYTNA HWAHY ETETP NELND LRWIR DAENC ONERO VDRCH DRSEN MAEOA HIYWY RANNH CEETT EETTL ETISI COOUH MCDIE EEBAE UHRMR DGHCM NESEG LYHEE EHCDH UPEEH HHRHR ORRNM REISH TWBRO RWIAL NEAOA TERNR DHCHS SRTTT WHSRR TMETN LGGGU IIWHT NAMSL NODNE ETTAG DRHNL RDOSA RAFOM HMIES AYNEA ASIAS OEASO UTEOE IOENS LFNME RNKCP EETAP LSRHS NUCEW OUTTE OOSMA TSWHU DWDNT RNMRS FTAON NDAAI AHMDE SUMOV OASAR EIAOE ILERN ETTDE WTTET MAQOE EREEC RNADC TBNTN NONET AEEIA ABTOH BESOS AYARM GEAHW TNRHE ADNAC ADNBI RNEHG DEOAO ACARE WDRTU EOKSA DDBAR PCHTN STXLA RTPDM REORI HDOEA ATENK PDRIW AAOSE OEMER HOLEW SFLBO NHBEO TEAUY OETMF PRENT OIBUN STEEM DENI'
    #cipher_text = 'ENEAC DBCTE NCOSH MTCGO TENAE EOEHT OTESO AGOTC TUOEB IMSSE EARTN TIYEW WOOGE EENEW PICNI NOSES TUAPM RUAKN RHMSF RNRCT ESAEF EDODO HDCOH CIHRO VRLDW EENYN ANBIS CDHLD UMUEO YLIIY AATBR SALEE TAOCN CGNOA IHESR SHFNS NBSTT ALEEO ENOAM ODEEE IMITI AHEHD TNTTA OARET MIFIT GOAOE ORRLT ILNDE AHTOE NIETD DNTTH AOERT INEOR LIWTB LNWOT DFWIC KNNNL LTLTY LDTOC DLEED MGGID SLSLD BITTB PTLRA OAEWE LDTVT DSNAN CINNE YLEAE HANTU HOWAN EASNE PHIUF LSDTD AELIT OICEB SSAHI OEAMO EEHEN TATIL NRTPD SHBST TOANE TROER ENEFS MNHNV TMRED CETMH HSOEC OGAAN UNWRO RIHDO SEOAE TTCDP TGIDR PPTLE OOAON OLATM REEAA LTICG EIANC YNATR EYNET AEGIR WDNSH YENEE RWSNF NPNUE UNYIE OHLAO TLLDH LTMIF KTFEH UVNNA VATON OCLNS LSRNC SCNIN DAATT DORHE ORLTF SEFFG AAOIE DDSTS YSCSA RNASV DLHIH DRRDE DHANW NTINR UWFDE EHMCD TSREH PTMNR IEASI WELMR EHMPO NIETA TOONL UHITE LHEDD INOHO HEEJS MOECD CAOTI NOTIO YIETM HEREL EYTNA HWAHY ETETP NELND LRWIR DAENC ONERO VDRCH DRSEN MAEOA HIYWY RANNH CEETT EETTL ETISI COOUH MCDIE EEBAE UHRMR DGHCM NESEG LYHEE EHCDH UPEEH HHRHR ORRNM REISH TWBRO RWIAL NEAOA TERNR DHCHS SRTTT WHSRR TMETN LGGGU IIWHT NAMSL NODNE ETTAG DRHNL RDOSA RAFOM HMIES AYNEA ASIAS OEASO UTEOE IOENS LFNME RNKCP EETAP LSRHS NUCEW OUTTE OOSMA TSWHU DWDNT RNMRS FTAON NDAAI AHMDE SUMOV OASAR EIAOE ILERN ETTDE WTTET MAQOE EREEC RNADC TBNTN NONET AEEIA ABTOH BESOS AYARM GEAHW TNRHE ADNAC ADNBI RNEHG DEOAO ACARE WDRTU EOKSA DDBAR PCHTN STXLA RTPDM REORI HDOEA ATENK PDRIW AAOSE OEMER HOLEW SFLBO NHBEO TEAUY OETMF PRENT OIBUN STEEM DENI'

    #cipher_text = 'EVLN& ACDT& ESEA& ROFO& DEEC& WIREE'
    #print decryptMyText(cipher_text,key,True)

    #key = [4,2,1,3,5,0]
    
#main()
