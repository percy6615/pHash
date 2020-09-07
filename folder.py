import os.path
import cv2
from phash import *
from dhash import *
from PIL import Image
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from hist import *


def readImageFromFolder(path="C:\\Users\mlgo\PycharmProjects\\untitled\googleTreeFallDown"):  # 輸入路徑
    imgs = []
    filepath = []
    valid_images = [".jpg"]  # 讀取檔案類型

    for f in os.listdir(path):
        split_ext = os.path.splitext(f)  # 1為副檔名 0為檔名
        ext1 = split_ext[1]
        ext0 = split_ext[0]

        if ext1.lower() not in valid_images:  # 把大寫轉為小寫
            continue
        # a=ext0
        imgs.append(os.path.join(path, f))
        filepath.append(ext0 + ext1)
        # imgs.append(Image.open(os.path.join(path, f)))
    filepath.sort()
    return filepath


def testPath():
    valid_images = [".jpg"]
    keywordName = []
    filename = []
    lena = []
    for root, dirs, files in os.walk("C:\\ImageSequence"):
        # C:\\Users\\mlgo\\PycharmProjects\\untitled   C:\\photo\\icrawlerImageDownloader\\Google
        for f in files:
            # print(root)
            ext = os.path.splitext(f)  # 1為副檔名 0為檔名
            ext1 = ext[1]
            ext0 = ext[0]
            if ext1.lower() not in valid_images:  # 把大寫轉為小寫
                keywordName.append(f)
                continue
            # print(os.path.join(root, f))
            filename.append(ext0 + ext1)
            lena.append(os.path.join(root, f))
    # print(filename)
    # print(lena)
    fff = 0
    fout = open('phashcode.txt', 'a')
    countitem = 0
    countcorrect = 0
    for item in lena:
        countitem = countitem + 1
        try:
            fff = hist(item)
            if fff < 0.45:
                degree = classify_pHash(item)
                fout.write(item + "\t" + degree + "\n")
            else:
                im = Image.open(item)
                im.save("C:\\untitled\\white\\%s" % (filename[countitem]))
                os.remove(item)
            countcorrect = countcorrect + 1
        except Exception as e:
            continue
    print("correct:%s" % (countcorrect))
    fout.close()


def caculatePhashCode(directoryPath, keywordName):
    imagename = readImageFromFolder("%s\\%s" % (directoryPath, keywordName))
    fout = open('phashcode.txt', 'a')
    for i in range(0, imagename.__len__()):
        try:
            img1 = cv2.imread("%s\\%s\\%s" % (directoryPath, keywordName, imagename[i]))
            degree = classify_pHash(img1)
            fout.write(keywordName + "\\" + imagename[i] + "\t" + degree + "\n")
        except:
            continue

    fout.close()


def caculateDhashCode(directoryPath, keywordName):
    imagename = readImageFromFolder("%s\\%s" % (directoryPath, keywordName))
    fout = open('dhashcode.txt', 'a')
    for i in range(0, imagename.__len__()):
        try:
            img1 = cv2.imread("%s\\%s\\%s" % (directoryPath, keywordName, imagename[i]))
            degree = dhash(img1)
            fout.write(keywordName + "\\" + imagename[i] + "\t" + degree + "\n")
        except:
            continue

    fout.close()

# 下方為 TEST 有無讀到檔名之code
# a=readImageFromFolder()
# for f in range (a.__len__()):
# print (a[f])
# testPath()
