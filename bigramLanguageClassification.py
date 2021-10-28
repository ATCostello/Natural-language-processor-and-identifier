# -*- coding: utf-8 -*-
"""
SCC 413 NLP Coursework 
Language Classification using bigrams
@author: Alf
"""

from nltk import ngrams, FreqDist
import os
import re

TrainingMaps = []
TrainingIndex = []
LanguageMaps = []

TestingMaps = []
TestingIndex = []
sampleNames = []

trainingdir = "trainingdata"
testdir = "sampledata"

"""
Generate Bigram Frequencies for training
"""
for filename in os.listdir(trainingdir):
    
    language = filename.split(".")
    LanguageMaps.append(language[0])
    
    path = trainingdir + "/" + filename

    file = open(path, errors="ignore")
    
    # read first 10000 characters
    text = file.read(10000)
    
    # remove text between <>
    text = re.sub(r"<[^>]+>", "", text)
    
    # generate all character bigrams
    bigram = list(ngrams(text, 2))
    
    # map bigrams to simpler format aa, ab, bc etc for printing
    #print(*map(''.join, bigram), sep=',')
    
    # Generate frequency for each bigram
    fdist = FreqDist(bigram)
    bgmap = {}
    for bg,count in fdist.items():
        #print(bg,count)
        # add bigram and count to dictionary
        if count > 0:
            bgmap[bg[0] + bg[1]] = count
            
    # Sort map by values
    bgmap = dict(sorted(bgmap.items(), key=lambda item: item[1], reverse = True))
    
    #Generate index for dict
    keys = list(bgmap.keys())
    
    #print(bgmap)
    
    TrainingMaps.append(bgmap)
    TrainingIndex.append(keys)
    
    file.close()

"""
List Training Languages with bigram Frequencies
"""
#x = 0
#while x < len(TrainingMaps):
#    print(LanguageMaps[x])
#    print(TrainingMaps[x])
#    print("")
#    x = x + 1
    
#print(TrainingIndex[0].index("a "))
    
"""
Generate Bigram Frequencies for sample data
"""
for filename in os.listdir(testdir):
    
    sampleNames.append(filename)
    
    path = testdir + "/" + filename

    file = open(path, errors="ignore")
    
    # read first 5000 characters
    text = file.read()
    
    # remove text between <>
    text = re.sub(r"<[^>]+>", "", text)
    
    # generate all character bigrams
    bigram = list(ngrams(text, 2))
    
    # map bigrams to simpler format aa, ab, bc etc for printing
    #print(*map(''.join, bigram), sep=',')
    
    # Generate frequency for each bigram
    fdist = FreqDist(bigram)
    bgmap = {}
    for bg,count in fdist.items():
        #print(bg,count)
        # add bigram and count to dictionary
        if count > 5:
            bgmap[bg[0] + bg[1]] = count
            
    # Sort map by values
    bgmap = dict(sorted(bgmap.items(), key=lambda item: item[1], reverse = True))

    #Generate index for dict
    keys = list(bgmap.keys())
    
    #print(bgmap)
    
    TestingMaps.append(bgmap)
    TestingIndex.append(keys)
    
    file.close()
    
"""
Compare sample bigram freq with training bigram freq
"""
# For each element in sample data map, compare the position of key with position in training map. 
# Sum the difference in positions, if not in training map, score 500 points. 
# Lowest total score is the predicted language

x = 0
# For each element in testing map
while x < len(TestingMaps):
    scores = []
    y = 0
    # for each element in the training map
    while y < len(TrainingMaps):
        score = 0
        # for each bigram in the test map
        for testbigram in TestingMaps[x]:
            # if the bigram is in the training set
            if testbigram in TrainingIndex[y]:
                # add the difference between the test bigram position and the training bigram position
                score = score + abs(TrainingIndex[y].index(testbigram) - TestingIndex[x].index(testbigram))
            else:
                score = score + 500
        y = y + 1
        scores.append(score)
        
    # Predict language of file by the lowest score   
    predictedLanguage = LanguageMaps[scores.index(min(scores))]
    print("Predicted that " + sampleNames[x] + " is using the language " + predictedLanguage)
    x = x + 1
    
'''
Used to output the bigrams and frequencies to export to the excel sheet for comparison
'''
'''
x = 0
while x < len(TrainingMaps):
    d = TrainingMaps[x]
    print(LanguageMaps[x])
    print(d.keys())
    print(d.values())
    #print(TrainingMaps[x])
    print("")
    x = x + 1
    
x = 0
while x < len(TestingMaps):
    d = TestingMaps[x]
    print(sampleNames[x])
    print(d.keys())
    print(d.values())
    #print(TestingMaps[x])
    print("")
    x = x + 1
'''