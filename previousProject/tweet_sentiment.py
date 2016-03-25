import sys, json
# Calculate a sentiment score per tweet

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


def parseTweets(fp, afinn):
    for line in fp:
        if 'text' not in line:  # Skip lines without tweets' text
            continue
        info = json.loads(line)
        sentiment_score = parseSentiment(info['text'], afinn)
        print(sentiment_score)


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2]).readlines()
    afinn = initializeAfinnFile(sent_file)
    parseTweets(tweet_file, afinn)

if __name__ == '__main__':
    main()
