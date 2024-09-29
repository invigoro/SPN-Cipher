import sys

if(len(sys.argv) != 4):
    raise Exception("3 input parameters required: [-e | -d] [text] [key]")
operation = sys.argv[1] #-e or -d

if(operation != "-e" and operation != "-d"):
    raise Exception("First parameter must be either -e or -d.")

text_arg = sys.argv[2]
key_arg = sys.argv[3]


def quarterString(s): #get 4 equal sized blocks
    return [
        s[:4],
        s[4:8],
        s[8:12],
        s[12:]
    ]

def leftShift(s, shiftValue):
    for i in range(0, shiftValue):
        s = s[1:] + s[0]
    return s

def keyMix(subkey, subtext): # XOR 16 bit block with round key
    subkeyBin = int(subkey, base=2)
    subtextBin = int(subtext, base=2)
    result = subkeyBin ^ subtextBin
    return "{0:b}".format(result).zfill(16)

def substituteBits(text, sBox): #change values according to table
    result = []
    for block in text:
        sub = sBox[int(block, base=2)]
        result.append("{0:b}".format(sub).zfill(4))
    return "".join(result)

def permutateBits(text, pBox): #move around according to table
    result = [0] * len(text)
    for i in range(0, len(text)):
        result[pBox[i] - 1] = text[i]
    return "".join(result)

def cipher(key, text, encrypt):
    PERMUTATIONS = 4
    if (len(key) != 16 and len(text) != 16):
        raise Exception("Cipher input must be 16 bits")
    
    substitutionBox = [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7]
    permutationBox = [1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15, 4, 8, 12, 16]
    roundKey = key
    roundText = text

    #generate keys
    roundKeys = []
    for i in range(0, PERMUTATIONS + 1):
        shift = ((i + 1) % 2) + 1
        roundKey = leftShift(roundKey, shift)
        roundKeys.append(roundKey)

    if not encrypt: #Reverse keys and invert S-box for decryption
        roundKeys.reverse()
        sBoxInverted = [0] * len(substitutionBox)
        for i in range(0, len(sBoxInverted)):
            sBoxInverted[substitutionBox[i]] = i 
        substitutionBox = sBoxInverted


    #initial keying and substitution for decryption
    if(encrypt is False):
        roundText = keyMix(roundKeys[0], roundText)
        roundText = substituteBits(
            quarterString(roundText),
            substitutionBox
        )

    #apply all three steps
    for i in range(0, PERMUTATIONS):
        roundKey = roundKeys[i] if encrypt else roundKeys[i + 1]

        roundText = keyMix(roundKey, roundText)

        if(i == PERMUTATIONS - 1): #we don't want to permutate on the last iteration here
            break                  #if encrypting, we have one more sub + key step
                                    #if decrypting, this is the last application of a round key, then exit

        if(encrypt):
            roundText = substituteBits(
                quarterString(roundText),
                substitutionBox
            )
            roundText = permutateBits(roundText, permutationBox)
        else: #reverse the order for decrypt
            roundText = permutateBits(roundText, permutationBox)
            roundText = substituteBits(
                quarterString(roundText),
                substitutionBox
            )

    #one last substitution and application of subkey for Encryption
    if(encrypt is True):
        roundText = substituteBits(
            quarterString(roundText),
            substitutionBox
        )
        roundText = keyMix(roundKeys[-1], roundText)

    print("Ciphertext: " if encrypt else "Plaintext: ", roundText)
    return roundText


    

operation = True if operation == "-e" else False
result = cipher(key_arg, text_arg, operation)
