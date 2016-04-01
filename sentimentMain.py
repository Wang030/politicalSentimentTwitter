from TwitterStream import TwitterStream
from ParsingTwitterJson import ParsingTwitterJson
import UserInteraction
import config

def main():
    # Set up Twitter api use
    print('User default API and authentications...')
    api = TwitterStream(config.api_key, config.api_secret,
                        config.access_token_key, config.access_token_secret)

    # Get user desired search
    query = UserInteraction.userInput()

    # Save tweets to file
    tweet_file = api.search(query, config.twitterFile)

    # Load data
    tweets = ParsingTwitterJson(tweet_file)

    # Parse Input, convert Unicode, etc.
    tweets.clean_data()

    # Detect language (French and English for now)

    # Integrate NLTK, ask its opinion on topic

    # Present data visually

if __name__ == '__main__':
    main()