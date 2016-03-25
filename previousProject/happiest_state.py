#!/usr/bin/python
# Returns the happiest state based on tweets. Note that the current location categorization is fairly crude.
__author__ = 'Seqian Wang'

import sys, json

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}


def initializeAfinnFile(afinnfile):
    afinn = {} # initialize an empty dictionary
    for line in afinnfile:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        afinn[term] = int(score)
    return afinn


def parseSentiment(line, afinn):
    total_score = 0
    for word in line.split(' '):
        word = word.strip().lower()
        if word in afinn.keys():
            total_score += afinn[word]
    return total_score


def findCorrespondingState(info):
    info_state = None
    location = info['user']['location']
    for state in states.keys():
        if state.lower() in location.lower():
            info_state = state
    return info_state


def parseTweets(fp, afinn):
    masterDictionary = {}

    for line in fp:

        if 'text' not in line:  # Skip lines without tweets' text
            continue
        info = json.loads(line)

        sentiment_score = parseSentiment(info['text'], afinn)
        state = findCorrespondingState(info)

        if state in masterDictionary.keys():
            masterDictionary[state].append(sentiment_score)
        else:
            masterDictionary[state] = []

    # Perform the average of all tweets pertaining to a state
    for state in masterDictionary.keys():
        if sum(masterDictionary[state]) == 0:
            masterDictionary[state] = float(0)
        else:
            masterDictionary[state] = sum(masterDictionary[state]) / len(masterDictionary[state])

    return masterDictionary


def printStateHappiness(sentiment_per_state):
    for key in sorted(sentiment_per_state, key=sentiment_per_state.get, reverse=True):
        if key is None:
            continue
        print(key)
        break


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2]).readlines()
    afinn = initializeAfinnFile(sent_file)
    state_sentiment_dictionary = parseTweets(tweet_file, afinn)
    printStateHappiness(state_sentiment_dictionary)

if __name__ == '__main__':
    main()
