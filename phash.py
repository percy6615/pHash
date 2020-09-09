# -*- coding: utf-8 -*-
# feimengjuan
# 利用python实现多种方法来实现图像识别
import numpy as np
import cv2
from hash_Hamming_distance import *
import time
from folder import *
from PIL import Image

basedirs = os.path.abspath(os.path.dirname(__file__))


def classify_pHash(imageName):
    img1 = cv2.imread(imageName)
    image1 = cv2.resize(img1, (32, 32))
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    # 将灰度图转为浮点型，再进行dct变换
    dct1 = cv2.dct(np.float32(gray1))
    # 取左上角的8*8，这些代表图片的最低频率
    # 这个操作等价于c++中利用opencv实现的掩码操作
    # 在python中进行掩码操作，可以直接这样取出图像矩阵的某一部分
    dct1_roi = dct1[0:8, 0:8]
    hash1 = getHash(dct1_roi)
    # print(hash1)
    decimal_value = 0
    hash1 = magic(hash1)
    hash1 = hex(int(hash1, 2))
    return hash1


def magic(numList):  # [1,2,3]
    s = map(str, numList)  # ['1','2','3']
    s = ''.join(s)  # '123'
    return s


if __name__ == '__main__':

    t0 = time.clock()

    ###
    # caculatePhashCode("C:\\Users\mlgo\PycharmProjects\\untitled","googleTreeFallDown")
    # caculatePhashCode("C:\\Users\mlgo\PycharmProjects\\untitled","tree collapsed down")
    #
    testPath()

    ###
    x = []
    y = []
    k = []
    ppp = []
    fin = open('phashcode.txt', 'r')
    f16biterror = open('16biterror.txt', 'w')
    while 1:
        data = fin.readline().split('\t')
        if data[0] == '':
            break  # 讀到檔尾
        x.append((os.path.split(data[0]))[1])
        ppp.append(data[0])
        # print(os.path.split(data[0]))
        y.append(data[1].rstrip())
    fin.close()

    count = 0

    for item in y:
        count = count + 1
        if len(item) == 18:
            z = bin(int(item, 16))
            k.append(z)
        else:
            print(ppp[count - 1])
            f16biterror.write(ppp[count - 1] + '\n')
            # im16biterror = cv2.imread(ppp[count - 1])
            # cv2.imwrite('C:\\untitled\\16bitError\\' + x[count - 1], im16biterror)
            # os.remove(ppp[count - 1])

    f16biterror.close()

    ext = []
    for item in x:
        ext.append(os.path.splitext(item)[-1])  # 1為副檔名 0為檔名
    # print(ext)
    # print(z)
    print(k.__len__())
    countphash = 0
    fout2 = open('phashcode_hamming_distance.txt', 'w')
    for i in range(0, k.__len__()):
        print(i)
        for j in range(i + 1, k.__len__()):
            # print(Hamming_distance(k[i], k[j]))
            hd = Hamming_distance(k[i], k[j])
            print(hd)
            if hd <= 0:  # 判斷Hamming_distance距離小於多少
                # print("%r和%r的距離為 %r"%(x[i],x[j],Hamming_distance(k[i],k[j])))
                try:
                    countphash = countphash + 1
                    # im1=Image.open(open(ppp[i],'rb'))
                    im1 = Image.open(ppp[i])
                    im1.save("C:\\untitled\\phashphoto\\%s__%s___1.%s" % (x[i], x[j], ext[i]))
                    im2 = Image.open(ppp[j])
                    im2.save("C:\\untitled\\phashphoto\\%s__%s___2.%s" % (x[i], x[j], ext[j]))
                    fout2.write(str(x[i]) + "\t" + str(x[j]) + "\t" + str(Hamming_distance(k[i], k[j])) + "\t")
                    os.remove(ppp[j])
                except Exception as e:
                    continue
    fout2.close()
    print("phash:%s" % countphash)
    print(time.clock() - t0, "seconds process time")
