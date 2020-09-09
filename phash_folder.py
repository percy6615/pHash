import os
import cv2
import numpy as np
from PIL import Image

basedirs = os.path.abspath(os.path.dirname(__file__))

class PhashInfomation:
    def __init__(self, file16hexCode, file2bitCode, filename, fileAllPath):
        self.file16hexCode = file16hexCode
        self.file2bitCode = file2bitCode
        self.filename = filename
        self.fileAllPath = fileAllPath

    def getfile16hexCode(self):
        return self.file16hexCode

    def getfile2bitCode(self):
        return self.file2bitCode

    def getfilename(self):
        return self.filename

    def getfileAllPath(self):
        return self.fileAllPath

    def getext(self):
        return os.path.splitext(self.filename)[-1]

def Hamming_distance(hash1, hash2):
    num = 0
    for index in range(len(hash1)):
        if hash1[index] != hash2[index]:
            num += 1
    return num


def getPicWritePercent(path):
    grayImage = Image.open(path).convert('L')
    pixList = list(grayImage.getdata())
    count = 0
    for pix in pixList:
        if pix >= 245:
            count = count + 1
    return count / pixList.__len__()


def classify_pHash(imagePath):
    img1 = cv2.imread(imagePath)
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


def getHash(image):
    avreage = np.mean(image)
    hash = []
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i, j] > avreage:
                hash.append(1)
            else:
                hash.append(0)
    return hash


def magic(numList):  # [1,2,3]
    s = map(str, numList)  # ['1','2','3']
    s = ''.join(s)  # '123'
    return s


def phashCodeFile(localPathName='train'):
    valid_images_ext = [".jpg"]
    keywordName = []
    filenames = []
    filesAllPath = []
    trainPath = basedirs + '\\' + localPathName
    phashcodeFile = basedirs + '\\' + 'phashcode'+"_"+localPathName+'.txt'
    for root, dirs, files in os.walk(trainPath):
        for file in files:
            fileSplit = os.path.splitext(file)
            fileName = fileSplit[0]
            fileExt = fileSplit[1]
            if fileExt.lower() not in valid_images_ext:
                keywordName.append(file)
            filenames.append(fileName + fileExt)
            filesAllPath.append(os.path.join(root, file))
    fout = open(phashcodeFile, 'a')
    fout.truncate(0)
    countitem = 0
    countcorrect = 0
    writePath = basedirs + '\\' + "white_"+localPathName
    if not os.path.isdir(writePath):
        os.mkdir(writePath)
    for fileAllPath in filesAllPath:
        countitem = countitem + 1
        try:
            picWritePerVal = getPicWritePercent(fileAllPath)
            if picWritePerVal < 0.45:
                degree = classify_pHash(fileAllPath)
                fout.write(fileAllPath + "\t" + degree + "\n")
            else:
                im = Image.open(fileAllPath)
                filePath, fileName = os.path.split(fileAllPath)
                im.save(writePath + "\\%s" % fileName)
                os.remove(fileAllPath)
            countcorrect = countcorrect + 1
        except Exception as e:
            print(e)
            continue
    print("correct:%s" % countcorrect)
    print('non-except' + str(countcorrect / countitem))
    fout.close()
    return phashcodeFile, localPathName


def phashProcess(localPathName='train'):
    fileNames = []
    file16hexCode = []
    file2bitCode = []
    filesAllPath = []
    phashInfomations = []
    phashcodePath = basedirs + "\\" + 'phashcode'+"_"+localPathName+'txt'
    phash16errorPath = basedirs + "\\" + '16biterror'+"_"+localPathName+'txt'
    phashhammingdistancePath = basedirs + "\\" + 'phashcode_hamming_distance'+"_"+localPathName+'txt'
    fphashcodefile = open(phashcodePath, 'r')
    # 變數 lines 會儲存 filename.txt 的內容
    lines = fphashcodefile.readlines()
    # close file
    fphashcodefile.close()

    f16biterrorfile = open(phash16errorPath, 'w')
    f16biterrorfile.truncate(0)
    error16bit = basedirs + '\\' + "error16bit_"+localPathName
    if not os.path.isdir(error16bit):
        os.mkdir(error16bit)
    fhammingdisfile = open(phashhammingdistancePath, 'w')
    fhammingdisfile.truncate(0)
    photophash = basedirs + '\\' + "phashphoto_"+localPathName
    if not os.path.isdir(photophash):
        os.mkdir(photophash)
    # print content
    for i in range(len(lines)):
        fileAllPath, hexCode = lines[i].split('\t')
        if fileAllPath == '':
            break  # 讀到檔尾
        filename = (os.path.split(fileAllPath))[1]
        hexCode = hexCode.rstrip()
        if len(hexCode) == 18:
            file16hexCode.append(hexCode)
            binCode = bin(int(hexCode, 16))
            file2bitCode.append(binCode)
            fileNames.append(filename)
            filesAllPath.append(fileAllPath)
            phashInfomations.append(PhashInfomation(hexCode, binCode, filename, fileAllPath))
        else:
            f16biterrorfile.write(fileAllPath + '\n')
            im16biterror = cv2.imread(fileAllPath)
            cv2.imwrite(error16bit + '\\' + filename, im16biterror)
            os.remove(fileAllPath)
    f16biterrorfile.close()
    deletePhashInfo = []
    for i in range(0, phashInfomations.__len__()):
        for j in range(i+1, phashInfomations.__len__()):
            if j in deletePhashInfo:
                continue
            hd = Hamming_distance(phashInfomations[i].getfile2bitCode(), phashInfomations[j].getfile2bitCode())
            if(hd<=0):
                # im1 = Image.open(phashInfomations[i].getfileAllPath(),'rb')
                deletePhashInfo.append(j)
                fhammingdisfile.write(phashInfomations[i].getfilename()+"\t"+phashInfomations[j].getfilename()+"\t"+str(hd) +"\n")
    for j in deletePhashInfo:
        if os.path.isfile(phashInfomations[j].getfileAllPath()):
            im1 = Image.open(phashInfomations[j].getfileAllPath())
            im1.save(photophash+"\\"+phashInfomations[j].getfilename())
            os.remove(phashInfomations[j].getfileAllPath())
phashcodeFile, localPathName = phashCodeFile()
phashProcess(localPathName)
