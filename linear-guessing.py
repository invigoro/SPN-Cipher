import sys


# USAGE
# [filename]
# text and key must be 16 bits


#get arg vals
if(len(sys.argv) != 2):
    raise Exception("Known keypair filename required")
filename = sys.argv[1] 

file = open(filename)


content = file.readlines()[1:]

pairs = {}
for i in range(len(content)):
    pair = content[i].strip().split("\t\t")
    pairs[pair[0]] = pair[1]

file.close()

#reverse this guy
substitutionBox = [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9]
sBoxInverted = [0] * len(substitutionBox)
for i in range(0, len(sBoxInverted)):
    sBoxInverted[substitutionBox[i]] = i 
substitutionBox = sBoxInverted

def lin_equation(plaintext, roundtext):
    plain = int(plaintext[5]) ^ int(plaintext[7])
    round1 = int(roundtext[0]) ^ int(roundtext[1]) ^ int(roundtext[3]) # 0 - 3
    round2 = int(roundtext[4]) ^ int(roundtext[5]) ^ int(roundtext[7]) # 4 - 7
    round4 = int(roundtext[12]) ^ int(roundtext[13]) ^ int(roundtext[15]) # 12 - 15
    return plain ^ round1 ^ round2 ^ round4

    #U4,1 ^ U4,5 ^ U4,13 * U4,2 * U4,6 * U4,14 * U4,4 * U4,8 * U4,16


def quarterString(s): #get 4 equal sized blocks
    return [
        s[:4],
        s[4:8],
        s[8:12],
        s[12:]
    ]


def applyKey(subkey, subtext): # XOR 16 bit block with round key
    subkeyBin = subkey #int(subkey, base=2)
    subtextBin = int(subtext, base=2)
    result = subkeyBin ^ subtextBin
    return "{0:b}".format(result).zfill(16)

keyresults = {}
#because of the chosen equations, we need three keys
for key1 in range(0, 16):
    for key2 in range(0, 16):
        for key4 in range(0, 16):
            key_combo = hex(key1)[-1] + hex(key2)[-1] + hex(key4)[-1]
            keyresults[key_combo] = 0
            for plain, cipher in pairs.items():
                cipher_split = quarterString(cipher)
                roundtext = applyKey(key1, cipher_split[0]) + applyKey(key2, cipher_split[1]) + "0000" + applyKey(key4, cipher_split[3]) #0000 because they won't be used

                holds = lin_equation(plain, roundtext)
                if(holds):
                    keyresults[key_combo] += 1
            keyresults[key_combo] = float(keyresults[key_combo] - 5000) / int(10_000)
            #print("Total matches: " + key_combo + " ", keyresults[key_combo])

#expected bias is 1/32
BIAS = float(1)/float(32)

best = [None, 10000]

print("Table: ")
iterations = 0
for key, val in keyresults.items():
    
    iterations += 1
    if(iterations < 100 and iterations < 600):
        print(key, val)

    if(abs(val - BIAS) < abs(best[1] - BIAS)):
        best[0] = key
        best[1] = val

print("Closest match: ", best[0], best[1])




