"""Finds the minhash value of the dna for a k-shingle using random permutation"""

import numpy

"""
params: dna string, k int
returns: set of k-shingle created from the dna
"""
def dna_shingle(dna, k):
    count, lastIndex = 0, k
    shingle_set = set()
    
    # checks to procceed if and only if value of k > 0 and k is an integer
    if(k <= 0 or type(k) != int):
        raise Exception("The value of k(%f) should be positive integer" %(k))
    # checks to procceed if and only if dna is non-empty and length of dna > k
    elif len(dna) == 0 or k > len(dna):
        raise Exception("The dna(%s) should have length greater than the value of k(%d)" %(dna, k))
    
    #loops through all the characters in a dna string to form k-shingle
    while(lastIndex <= len(dna)):
         # froms a k-shingle 
         shingle = dna[count:lastIndex]
         # creates a list of bits indicating if the k-shingle contains character other than A, C, G or T; if it contains character other than 'A', 'C', 'G' and 'T' then True is inserted else False
         flagUnwantedChar = list(x not in ["A", "C", "G", "T"] for x in shingle.upper())
         # checks if the 'flagUnwantedChar' list contains any True bit (i.e. the shingle contains character other than 'A', 'C', 'G' and 'T') and warns the user accordingly
         if any(flagUnwantedChar):
             raise Exception("The provided DNA sample contains unwanted character: '%s' at Position %d" %(shingle[flagUnwantedChar.index(True)], count+flagUnwantedChar.index(True)+1))
         #  adds the k-shingle to the set of k-shingle
         else:
             shingle_set.add(dna[count:lastIndex])
             count += 1
             lastIndex = count+k
    
    # returns the set containing all possible k-shingle of the dna
    return shingle_set


"""
params: dna string
returns: the decimal equivalent of the k-shingle of a dna
"""
def shingle2decimal(dna):
    try:
        # Turns all the characters of the dna string to upper-case and replaces all 'A' as 0, 'C' as 1, 'G' as 2 and 'T' as 3 for base 4 representation of the dna string
        base4Shingle = dna.upper().replace("A", "0").replace("C", "1").replace("G", "2").replace("T", "3")
        # converts the base 4 shingle to its equivalent decimal representation
        return(int(base4Shingle, 4))
    except:
        # throws an exception if the dna shingle contains character other than 'A', 'C', 'G' or 'T'
        raise Exception("The dna contains unwanted character. Hence it cannot be converted to decimal.")


"""
params: dna string, k int
returns: list for the vector representation of each k-shingle of the dna
"""
def dna_vector(dna, k):
    try:
        # get the set containing all possible k-shingle of the dna
        shingle=dna_shingle(dna, k)
        # creates a zero vector with 4^k dimensions
        dnaVector = [0]*(4**k)
        # replaces 0 with 1 in dna vector at index = (decimal value of the shingle)
        for s in shingle:
            dnaVector[shingle2decimal(s)]=1
        return dnaVector
    except Exception as ex:
        # throws exception to the calling function if generated while executing dna_shingle(dna, k) or shingle2decimal(s)
        raise Exception(ex)


"""
params: k int
returns: list for the permutation vector of size 4^k
"""
def permute(k):
    # performs permutation using 'numpy' module to shuffle a list containing numbers 0 to 4^k
    permutation = list(range(4**k))
    numpy.random.shuffle(permutation)
    return permutation

"""
params: permutation function, dna string, k int
returns: int minhash value of the dna string for k-shingle using permutation
"""
def minhash_dna(permutation, dna, k):
    # return a number that is a minhash of dna
    # if all dimensions of the dna vector is zero or some error occurs then it returns None
    try:
        # gets the vector representation of the input dna string
        dnaVector = dna_vector(dna, k)
        # gets the permuted vector to perform hash operation
        permutedVector = permutation(k)
        # returns the value of permuted vector for which the first value of dna vector at index = (value of the permuted vector) is 1
        for index in permutedVector:
            if dnaVector[index] == 1:
                return index
    except Exception as ex:
        print(ex)

# to print the minhash value   
print("The minhash value is %s" %(minhash_dna(permute, "AAAAACGTACCATGCAGTACGATCAGTTGCA", 4)))
      