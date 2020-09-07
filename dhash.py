from PIL import Image
import time
from hash_Hamming_distance import *
from folder import *
def dhash(image, hash_size = 8):

    # Grayscale and shrink the image in one step.

    image = image.convert('L').resize(

        (hash_size + 1, hash_size),

        Image.ANTIALIAS,

    )

    pixels = list(image.getdata())

    # Compare adjacent pixels.

    difference = []

    for row in range(hash_size):

        for col in range(hash_size):

            pixel_left = image.getpixel((col, row))

            pixel_right = image.getpixel((col + 1, row))

            difference.append(pixel_left > pixel_right)

    # Convert the binary array to a hexadecimal string.

    decimal_value = 0

    hex_string = []

    for index, value in enumerate(difference):

        if value:

            decimal_value += 2**(index % 8)

        if (index % 8) == 7:

            hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))

            decimal_value = 0

    return ''.join(hex_string)

if __name__ == '__main__':

 t0 = time.clock()
 caculateDhashCode("C:\\Users\mlgo\PycharmProjects\\untitled","googleTreeFallDown")
 caculateDhashCode("C:\\Users\mlgo\PycharmProjects\\untitled","tree collapsed down")
 x = []
 y = []
 k = []

 fin = open('dhashcode.txt','r')
 while 1:
    data = fin.readline().split('\t')
    if data[0] == '': break  # 讀到檔尾
    x.append(data[0])
    y.append(data[1].rstrip())
 fin.close()
 for item in y:
    z= bin(int('1' + item, 16))[3:]
    #z = bin(int(item,16))
    k.append(z)
 #print(x)
 #print(y)
 #print(z)
 print(k)
 fout2 = open('dhashcode_hamming_distance.txt', 'w')
 for i in range(0,k.__len__()):
     for j in range(i+1,k.__len__()):
         #print(Hamming_distance(k[i], k[j]))
        hd=Hamming_distance(k[i],k[j])
        #print(i)
        #print(j)
        if(hd<=8):   #判斷Hamming_distance距離小於多少
            print("%r和%r的距離為 %r"%(x[i],x[j],Hamming_distance(k[i],k[j])))
            fout2.write( str(x[i]) + "\t" + str(x[j]) + "\t"+str(Hamming_distance(k[i],k[j]))+"\t")
 fout2.close()
 print(time.clock() - t0, "seconds process time")
