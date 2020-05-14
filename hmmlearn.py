from collections import Counter
from math import log
import collections
from collections import *
import sys
import codecs


POS = Counter()
POSList = []
InitialCount = Counter()
n = 0
i = 0
TransitionNumerator = Counter()
TransitionNumeratorpp = []
TransitionDenominator = Counter()
EmissionNumerator = Counter()
InitialProbabilities = dict()
TransitionProbabilities = dict()
EmissionProbabilities = dict()

# with open(sys.argv[1], mode="r",
#           encoding="utf-8") as f:
with open("/Users/parinita/PycharmProjects/hmm/venv/hmm-training-data/it_isdt_train_tagged.txt", mode="r",
          encoding="utf-8") as f:
    for line in f:
        n += 1
        line = line.strip("\n")
        content = line.split(" ")
        InitialCount.update([content[0].rsplit("/", 1)[1]])
        for current in content:
            tag1 = current.rsplit("/", 1)[1]
            word = current.rsplit("/", 1)[0]
            if content.index(current) <= (len(content) - 2):
                next = content[content.index(current) + 1]
                tag2 = next.rsplit("/", 1)[1]
                TransitionNumerator.update([tag1 + " " + tag2])
                TransitionDenominator.update([tag1])
            EmissionNumerator.update([word + " " + tag1])
            POS.update([tag1])

for key, value in POS.items():
    if InitialCount[key] != 0:
        InitialProbabilities[key] = log(InitialCount[key]) - log(n)

for key, value in POS.items():
    for key2, value2 in POS.items():
        TransitionProbabilities.setdefault(key, {})[key2] = 1.0

for key, value in TransitionNumerator.items():
    tag1, tag2 = key.split(" ")
    TransitionProbabilities[tag1][tag2] += value

for key, value in TransitionProbabilities.items():
    for key2, value2 in value.items():
        TransitionProbabilities[key][key2] = log(value2)

for key, value in TransitionProbabilities.items():
    for key2, value2 in value.items():
        TransitionProbabilities[key][key2] = value2 - log(TransitionDenominator[key] + len(POS))

# for key, value in EmissionNumerator.items():
#     word, tag = key.split(" ")
#     EmissionProbabilities.setdefault(tag, {})[word] = log(value)
#
# for key, value in EmissionProbabilities.items():
#     for key2, value2 in value.items():
#         if EmissionProbabilities[key][key2] != 0:
#             EmissionProbabilities[key][key2] = value2 - log(POS[key])
for key, value in EmissionNumerator.items():
    word, tag = key.split(" ")
    EmissionProbabilities.setdefault(tag, {})[word] = 1.0

for key, value in EmissionNumerator.items():
    word, tag = key.split(" ")
    EmissionProbabilities[tag][word] = log(value) - log(POS[tag])

# for key, value in EmissionProbabilities.items():
#     for key2, value2 in value.items():
#         if EmissionProbabilities[key][key2] != 0:
#             EmissionProbabilities[key][key2] = value2 - log(POS[key])

for key, value in POS.items():
    POSList.append(key)

with codecs.open("hmmmodel.txt", 'w', encoding='utf8') as f1:
    f1.write(str(InitialProbabilities))
    f1.write("\n")
    f1.write(str(TransitionProbabilities))
    f1.write("\n")
    f1.write(str(EmissionProbabilities))
    f1.write("\n")
    f1.write(str(POSList))
f1.close()
