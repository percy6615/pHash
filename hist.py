import numpy as np
import matplotlib.pylab as plt
from PIL import Image
def hist(path):
    im = Image.open(path).convert('L')
    a=[]
    a=list(im.getdata())
    count=0
    for item in a:
        if item>=245:
            count=count+1
    #print(count)
    aaa=(count/a.__len__())
    return (count/a.__len__())