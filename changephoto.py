import os
keywordName = []
filename= []
lena=[]
valid_images = [".jpg"]
for root, dirs, files in os.walk("C:\\untitled"):
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

print(lena)
print(filename)