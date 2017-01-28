import alpha
# tools to turn a plaintext key into a numerical key. 
# used for columnar transposition 

class KeyChar(object):
    def __init__(self,l,pos,w):
        self.letter = l
        self.position = pos
        self.weight = w
    def setWeight(self,w):
        self.weight = w

def getRawKeyList(key):
    key_list = []
    key_weight_normalized = dict()
    i = 0
    for c in key:
        weight = alpha.giveAlphabet('u')[c]
        char = KeyChar(c,i,weight)
        i=i+1
        key_list.append(char)
    return key_list

def adjustKeyWeights(key_obj_list):
    #first sort based off weight
    kchar_sorted = sorted(key_obj_list, key = lambda kchar: (kchar.weight,kchar.position))
    i=0
    for k in kchar_sorted:
        #print k.letter, k.position,
        k.setWeight(i) #readjust weights based on weight
        #print  k.weight
        i=i+1

    return kchar_sorted 
    # sort off position and print new weight values
    #for k in sorted(kchar_sorted, key = lambda kchar: kchar.position):
        #print k.letter, k.position, k.weight
    #return sorted(kchar_sorted, key = lambda kchar: kchar.position)


    # return weighted key sorted by letter weight (smallest letter first)
def getWeightedKeyList(key):
    k_adjusted = adjustKeyWeights(getRawKeyList(key))
    final_key =  sorted(k_adjusted, key = lambda kchar: kchar.weight)
    key_list = getKeyAsList(final_key)
    return final_key,key_list

def getKeyAsList(kchar_objs):
    list = []
    for k in kchar_objs:
        list.append(k.position)
    return list

 ##DEBUGGING / TESTING
#kchar_objs,k_list = getWeightedKeyList('ZEBRAS')
#for k in kchar_objs:
#    print k.letter, k.position, k.weight

#print k_list