from collections import Counter
import collections
import ast
import sys
import codecs

def viterbialgo(observation, states):
    Viterbi = dict()
    Backpointer = dict()
    for tag in states:
        for word in observation:
            Viterbi.setdefault(tag, {})[word] = -999
            Backpointer.setdefault(tag, {})[word] = ''
    for tag in states:
        Backpointer[tag]['end'] = ""
        Viterbi[tag]['end'] = -999
    word = observation[0]

    for s in states:
            if s not in InitialProbabilities.keys():
                Viterbi[s][word] = -999
            elif word not in EmissionProbabilities[s].keys():
                Viterbi[s][word] = InitialProbabilities[s]
            else:
                Viterbi[s][word] = InitialProbabilities[s] + EmissionProbabilities[s][word]

    currentword = observation[0]


    # for current in states:
    #     for prev in states:
    #         if currentword not in EmissionProbabilities[current].keys():
    #             flag = true

    for currentword in observation[1:]:
        flag = False
        for current in states:
            if currentword in EmissionProbabilities[current].keys():
                flag = True
        prevword = observation[observation.index(currentword)-1]
        for current in states:
            max = -9999
            maxstate = ""
            for prev in states:
                if flag == True:
                    if currentword not in EmissionProbabilities[current].keys():
                        EmissionProbabilities[current][currentword] = -9999
                    if Viterbi[prev][prevword] + TransitionProbabilities[prev][current] > max:
                        max = Viterbi[prev][prevword] + TransitionProbabilities[prev][current] + EmissionProbabilities[current][currentword]
                        maxstate = prev
                if flag == False:
                    if Viterbi[prev][prevword] + TransitionProbabilities[prev][current] > max:
                        max = Viterbi[prev][prevword] + TransitionProbabilities[prev][current]
                        maxstate = prev
            Viterbi[current][currentword] = max
            Backpointer[current][currentword] = maxstate
    max = -9999
    maxstate = ""
    BestPath = []
    bestpathpointer = ""
    for tag in states:
        if Viterbi[tag][currentword] > max:
            max = Viterbi[tag][currentword]
            maxstate = tag
    Viterbi[maxstate]['end'] = max
    Backpointer[maxstate]['end'] = maxstate
    bestpathpointer = Backpointer[maxstate]['end']
    observation = observation[::-1]
    BestPath.append(bestpathpointer)
    for word in observation:
        bestpathpointer = Backpointer[bestpathpointer][word]
        BestPath.append(bestpathpointer)
    BestPath.pop()
    return BestPath[::-1]

dics = []
i = 0
j = 0

with open("hmmmodel.txt", 'r') as model:
    for line in model:
        dics.append(line)
    InitialProbabilities = ast.literal_eval(dics[0])
    TransitionProbabilities = ast.literal_eval(dics[1])
    EmissionProbabilities = ast.literal_eval(dics[2])
    States = ast.literal_eval(dics[3])

with codecs.open("hmmoutput.txt", 'w', encoding='utf8') as file:
    with open("/Users/parinita/PycharmProjects/hmm/venv/hmm-training-data/it_isdt_dev_raw.txt", mode="r",
              encoding="utf-8") as f:
    # with open(sys.argv[1], mode="r",
    #           encoding="utf-8") as f:
        for line in f:
            line = line.strip("\n")
            Observations = line.split(" ")
            BestPath = viterbialgo(Observations, States)
            i = 0
            for word in Observations:
                file.write(word + "/" + BestPath[i] + " ")
                i += 1
            file.write("\n")

file.close()









