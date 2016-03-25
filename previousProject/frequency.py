#!/usr/bin/python
# Compute the term frequency histogram (#term occurence / #all terms occurences)
__author__ = 'Seqian Wang'

import sys, json, re


def parseTweets(fp):
    frequencyTable = {}
    totalNumberOfWords = 0

    for line in fp:

        if 'text' not in line:  # Skip lines without tweets' text
            continue
        info = json.loads(line)

        for word in info['text'].split(' '):
            word = re.sub(r'\W+', '', word).strip().lower()  # Removing all non-alphanumeric characters as they tend to cause problems
            totalNumberOfWords += 1
            if word in frequencyTable.keys():
                frequencyTable[word] += 1
            else:
                frequencyTable[word] = 1

    return frequencyTable, totalNumberOfWords


def printFrequencyTable(frequencyDict, total):
    for term in frequencyDict.keys():
        if term is '':
            continue  # Skip empty key string
        try:
            print('%s %f' % (term, frequencyDict[term]/total))
        except UnicodeEncodeError:
            continue


def main():
    tweet_file = open(sys.argv[1]).readlines()
    frequencyDict, total = parseTweets(tweet_file)
    printFrequencyTable(frequencyDict, total)

if __name__ == '__main__':
    main()
