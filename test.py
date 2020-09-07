import numpy as np

def Hamming_distance(hash1,hash2):
    num = 0
    for index in range(len(hash1)):
        if hash1[index] != hash2[index]:
            num += 1
    return num


test000079 = '0xc000000080000080'
test108400 = '0x802f4d5618584060'

test000086 = '0x98d990b020420000'
test000669 = '0x98d990b020420000'

test000120 = '0x80c0808080000000'
test012945 = '0x8080808080000000'
test013698 = '0x80c0800080000000'

test000690= '0x8000000000000000'
test046806= '0xc2c600008c40500a'
bintest1 = bin(int(test000690,16))
bintest2 = bin(int(test046806,16))

print(bintest1+'\n')
print(bintest2+'\n')

print(Hamming_distance(bintest1,bintest2))