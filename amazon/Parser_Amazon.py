# Download "amazon-meta.txt" raw dataset from "https://snap.stanford.edu/data/amazon-meta.html"

# import string
import re
from collections import Counter
import csv
# import nltk.corpus import stopwords
# from stemming.porter2 import stem
# import networkx

amazonProducts = {}
count = 0
allNodesRelated = set()
allFeatures = []
noFeatures = []
asinToIDMap = {}
featToIDMap = {}

fhr = open("amazon-meta.txt", "r", encoding="utf-8", errors="ignore")
print ("Start processing dataset")

for line in fhr:
    line = line.strip()
    if(line.startswith("ASIN")):
        asin = line[5:].strip()
    elif(line.startswith("similar")):
        ls = line.split()
        related = [c for c in ls[2:]]
        # for x in related:
        #     allNodesRelated.add(x)
    elif(line.startswith("categories")):
        features = set()
        ls = line.split()
        categories = [fhr.readline().split('|')[1:] for i in range(int(ls[1].strip()))];
        for j in categories:
            for x in j:
                x = re.sub(r"[^a-zA-Z&']", " ", str(x)).strip()
                if (len(x) > 3):
                    features.add(x)
        if (len(features)==0):
            noFeatures.append(count+1)
        allFeatures.extend(features)
    elif(line==""):
        try:
            count = count+ 1
            MetaData = {}
            MetaData['asin'] = asin
        
            MetaData['categories'] = features
            MetaData['related'] = related
            amazonProducts[asin] = MetaData
        except NameError:
            continue
fhr.close()
featureCountDict = Counter(allFeatures)
print (len(amazonProducts))

# with open('test.csv', 'w') as f:
#     for key in featureCountDict.keys():
#         f.write("%s,%s\n"%(key,featureCountDict[key]))

print ("Done")
print ("This many do not have features : " + str(len(noFeatures)))
# print (len(allNodesRelated))
#print (amazonProducts)

num = 0
selectedFeatures = []

for k,v in featureCountDict.items():
    if (k != "General" and k != "Subjects" and k != "Amazon com Stores" and k != "Categories" and v>2886):
    #if (k != "General" and k != "Subjects" and k != "Amazon com Stores" and k != "Categories"): 
        selectedFeatures.append(k)
        featToIDMap[k] = num
        num = num + 1

allFeatures.clear()
featureCountDict.clear()

with open('featureMapLatest.csv', 'w') as f:
    for key in featToIDMap.keys():
        f.write("%s,%s\n"%(key,featToIDMap[key])) 


listofzeros = [0] * len(featToIDMap)
edges = []
edgeDict = {}
vertices = set()
featuresOfEachVertex = {}

#attFile = open("attributesNew.txt",'w')
cnt =0
for dic in amazonProducts.values():
    featVector = []
    asin = ""
    feat = ""
    related = ""
    for key,value in dic.items():
        if key == "asin":
            asin = value
            #print (asin)
        elif key == "categories":
            feat = value
            for x in feat:
                if (x in selectedFeatures):
                    featVector.append(x)
            featuresOfEachVertex[asin] = featVector
        elif (key == "related"):
            related = value
            for node in related:
                if node in amazonProducts:
                    if (asin not in asinToIDMap):
                        asinToIDMap[asin] = cnt
                        cnt = cnt+1
                    if (node not in asinToIDMap):
                        asinToIDMap[node] = cnt
                        cnt = cnt+1
                    vertices.add(asin)
                    vertices.add(node)
                    ky = min(asinToIDMap[asin],asinToIDMap[node])
                    other = max(asinToIDMap[asin],asinToIDMap[node])
                    if (ky in edgeDict):
                        edgeDict[ky].append(other)
                    else:
                        edgeDict[ky] = [other]

    
#attFile = open("attributesNew.txt",'w')

# for dic in amazonProducts.values():
#     featVector = listofzeros
#     for key,value in dic.items():
#         if key == "asin":
#             asin = value
#             attFile.write("%s\t"%(asinToIDMap[asin]))
#         elif key == "categories":
#             feat = value
#             for x in feat:
#                 if (x in selectedFeatures):
#                     featVector[featToIDMap[x]] = 1
#             for i in featVector:
#                 attFile.write(str(i)+"\t")
#             attFile.write("\n")
#         elif (key == "related"):
#             related = value
#             for node in related:
#                 if (node in asinToIDMap.keys()):
#                     edges.append(str(asinToIDMap[asin])+" "+str(asinToIDMap[node]))

# attFile.close()
#print (featuresOfEachVertex)
edgeset = set()
e=0

for start,ends in edgeDict.items():
    for end in ends:
        edgeString = str(start)+"\t"+str(end)
        edgeset.add(edgeString)

with open('outputFiles/edgeListFinal.txt', 'w') as edgeFile:
    for ends in edgeset:
        e = e+1
        edgeFile.write("%s\n"%(ends))

with open('outputFiles/attributesFinal.txt', 'w') as atFile:
    for v in vertices:
        featVector = listofzeros
        atFile.write("%s\t"%(asinToIDMap[v]))
        if (v in featuresOfEachVertex.keys()):
            for f in featuresOfEachVertex[v]:
                featVector[featToIDMap[f]] = 1
        #print(featToIDMap[f])
        for i in featVector:
            atFile.write(str(i)+"\t")
        atFile.write("\n")

print ("Edges : " + str(e))