import tweepy, sys, jsonpickle, time

class TwitterStream:
    def __init__(self, api_key, api_secret, access_token_key, access_token_secret):
        # Reference page: http://www.karambelkar.info/2015/01/how-to-use-twitters-search-rest-api-most-effectively./

        # Input your own api credentials from Twitter API
        auth = tweepy.AppAuthHandler(api_key, api_secret)
        # auth.set_access_token(access_token_key, access_token_secret)

        # Create API handler
        self.api = tweepy.API(auth, wait_on_rate_limit=True,
                              wait_on_rate_limit_notify=True)

        if not self.api:
            print("Can't Authenticate")
            sys.exit(-1)

    # Return a list of locations IDs where Twitter has trending information
    def trends_available(self):
        return self.api.trends_available()

    # Return tweets for specific query
    def old_search(self, query):
        count = 100
        return self.api.search(q=query)

    def extract_original_tweets(self, tweetJson, fName):
        # Store all downloaded tweets in a set (say set A)
        # From this set filter out the retweets & extract the original tweet from these retweets (say set B)
        # Insert in set A all unique tweets from set B that are not already in set A
        if tweetJson.retweeted_status:
            with open(fName, 'a') as f:
                f.write(tweetJson.retweeted_status)
        pass

    def search(self, searchQuery, fName, maxTweets = 45000):
        tweetsPerQry = 100  # this is the max the API permits
        # fName = 'tweets.txt' # We'll store the tweets in a text file.

        # If results from a specific ID onwards are read, set since_id to that ID.
        # else default to no lower limit, go as far back as API allows
        # Useful with ID from first line to catch new tweets since.
        sinceId = None

        # If results only below a specific ID are, set max_id to that ID.
        # else default to no upper limit, start from the most recent tweet matching the search query.
        # Useful with ID from last line to continue catching older tweets
        max_id = -1

        tweetCount = 0
        print("Downloading max {0} tweets".format(maxTweets))
        with open(fName, 'w') as f:
            while tweetCount < maxTweets:
                try:
                    if (max_id <= 0):
                        if (not sinceId):
                            new_tweets = self.api.search(q=searchQuery, count=tweetsPerQry)
                        else:
                            new_tweets = self.api.search(q=searchQuery, count=tweetsPerQry,
                                                    since_id=sinceId)
                    else:
                        if (not sinceId):
                            new_tweets = self.api.search(q=searchQuery, count=tweetsPerQry,
                                                    max_id=str(max_id - 1))
                        else:
                            new_tweets = self.api.search(q=searchQuery, count=tweetsPerQry,
                                                    max_id=str(max_id - 1),
                                                    since_id=sinceId)
                    if not new_tweets:
                        print("No more tweets found")
                        break
                    for tweet in new_tweets:
                        f.write(jsonpickle.encode(tweet._json, unpicklable=False) +
                                '\n')
                    tweetCount += len(new_tweets)
                    print("Downloaded {0} tweets".format(tweetCount))
                    max_id = new_tweets[-1].id
                except ConnectionResetError:
                    try:
                        print("Will wait 15 minutes to reset connection and continue download. Press Ctrl-C to ignore wait and continue analysis.")
                        time.sleep(15 * 60 + 3)
                    except KeyboardInterrupt:
                        print("Tweet Extraction terminated. Proceeding to analysis.")
                        break
                    else:
                        continue
                        print("Back to extracting tweets...")

                except tweepy.TweepError as e:
                    # Just exit if any other error
                    print("some error : " + str(e))
                    break

        print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))
        return fName