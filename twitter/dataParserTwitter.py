# Download raw dataset from "https://snap.stanford.edu/data/ego-Twitter.html"

import networkx as nx
import glob
from collections import Counter
from nltk.corpus import stopwords

vertexIDMap = {}
featureList = []
featureCounter = 0
vertexCounter = 0
attributeDict = {}

fh = open("twitter_combined.txt", 'rb')
graph = nx.read_edgelist(fh)
fh.close()
edges = graph.edges()
vertices = graph.nodes()

for v in vertices:
    if (v not in vertexIDMap.keys()):
        vertexIDMap[v] = vertexCounter
        vertexCounter = vertexCounter+1
    attributeDict[vertexIDMap[v]] = [str(0)] * 1007

featNameFileList = [f for f in glob.glob("twitter/*.featnames")]
featuresInEachFile = {}
for f in featNameFileList:
    featureDictPerFile = {}
    lineCout = 0;
    fh1 = open(str(f), 'r')
    for line in fh1:
        featureName = line.strip().split(' ',1)[-1]
        term = featureName.split(':', 1)[-1]
        if (term in set(stopwords.words("english"))):
            continue
            # print(featureName)
        else:
            featureList.append(featureName)
            featureDictPerFile[lineCout]=featureName
        lineCout = lineCout+1
    featuresInEachFile[f] = featureDictPerFile

print (featuresInEachFile)


featureCounts = Counter(featureList)
# print ((featureCounts))
print (len(featNameFileList))
print (len(featureCounts))

c = 0
selectedFeatures = {}
for feat,cnt in featureCounts.items():
    if cnt > 50:
        selectedFeatures[feat] = c
        print (feat +" -- " +str(featureCounts[feat]))
        c = c + 1
print (c)

featFileList = [f for f in glob.glob("twitter/*.feat")]

for f in featFileList:
    fh1 = open(str(f), 'r')
    for line in fh1:
        extracted = line.strip().split(' ')
        index = vertexIDMap[extracted[0]]
        extractedFeatures = extracted[1:]
        #print (f)
        name = "twitter/"+str(f[f.index("/")+1:f.index(".")])+".featnames"
        #print (name)
        correspondingFeatureDict = featuresInEachFile[name]
        #print (f+" ---> "+str(correspondingFeatureDict))
        for k,v in correspondingFeatureDict.items():
            if (v in selectedFeatures):
                attributeDict[index][selectedFeatures[v]] = str(extractedFeatures[k])

attFile = open("attributesTwitterTestDinix.txt", 'w')

for attr in selectedFeatures.keys():
    print (attr)

for k,v in attributeDict.items():
    attFile.write(str(k))
    for i in v:
        attFile.write("\t" + i)
    attFile.write("\n")
    # print (str(k) + " ----> " + str(v))
    # print (str(len(v)))

edgeFile = open("edgeListTwitterTEstDinix.txt", 'w')

for edge in edges:
    edgeFile.write(str(vertexIDMap[edge[0]])+"\t"+str(vertexIDMap[edge[1]]))
    edgeFile.write("\n")
