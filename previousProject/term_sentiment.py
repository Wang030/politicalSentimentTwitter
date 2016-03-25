import sys, json, re
# Determining the sentiment for terms that do not appear in the AFINN-111.txt reference file

def importAfinnFile(afinnfile):
    afinn = {} # initialize an empty dictionary
    for line in afinnfile:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        afinn[term] = int(score)
    return afinn


def parseTweets(fp, afinn):
    newAfinn = {}
    for line in fp: # Per line

        if 'text' not in line:  # Skip lines without tweets' text
            continue
        info = json.loads(line)  # Load json and parse it

        line_list_of_words = info['text'].split(' ')
        line_sentiment_score = 0
        newAfinn_words_to_update = []   # For holding a list of words which:
                                        # 1) appears in the tweet/line,
                                        # 2) was not in the original afinn file, and
                                        # 3) needs change to its sentiment value
        for word in line_list_of_words:  # Per word
            word = word.strip().lower()
            word = re.sub(r'\W+', '', word)  # Removing all non-alphanumeric characters as they tend to cause problems
            if word in afinn.keys():
                line_sentiment_score += afinn[word]
            elif word in newAfinn.keys():
                newAfinn_words_to_update.append(word)
            else:
                newAfinn[word] = 0
                newAfinn_words_to_update.append(word)

        for word in newAfinn_words_to_update:
            newAfinn[word] += 0.25 * line_sentiment_score   # Only affect the new series of words' sentiment value by
                                                            # a quarter of the total sentence sentiment score

    return newAfinn


def printNewAfinnWords(afinn):
    for key in afinn.keys():
        if key is '':
            continue  # Skip empty key string
        try:
            print('%s %f' % (key, afinn[key]))
        except UnicodeEncodeError:
            continue


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2]).readlines()
    afinn = importAfinnFile(sent_file)
    newAfinn = parseTweets(tweet_file, afinn)
    printNewAfinnWords(newAfinn)

if __name__ == '__main__':
    main()