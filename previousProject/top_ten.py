#!/usr/bin/python
# Identifying the ten most frequently occuring hashtags
__author__ = 'Seqian Wang'

import sys, json, operator, re

def parseTweets(fp):
    frequencyTable = {}

    for line in fp:

        if 'text' not in line:  # Skip lines without tweets' text
            continue
        info = json.loads(line)

        for hashtag in info['entities']['hashtags']:
            hashtag = hashtag['text']
            hashtag = re.sub(r'\W+', '', hashtag).strip().lower()  # Removing all non-alphanumeric characters as they tend to cause problems
            if hashtag in frequencyTable.keys():
                frequencyTable[hashtag] += 1
            else:
                frequencyTable[hashtag] = 1

    return frequencyTable


def printFrequencyTable(frequencyDict):
    maxPrint = 10
    try:
        for key in sorted(frequencyDict, key=frequencyDict.get, reverse=True):
            if maxPrint > 0:
                print('%s %f' % (key, frequencyDict[key]))
                maxPrint -= 1
    except UnicodeEncodeError:
        pass
    return 1


def main():
    tweet_file = open(sys.argv[1]).readlines()
    frequencyDict = parseTweets(tweet_file)
    printFrequencyTable(frequencyDict)

if __name__ == '__main__':
    main()