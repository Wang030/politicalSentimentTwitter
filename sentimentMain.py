from TwitterStream import TwitterStream
import json, datetime, urllib.parse
import config

def validateDate(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return("Incorrect data format, should be YYYY-MM-DD")

    daysDifference = abs((datetime.date.today() - datetime.datetime.strptime(date, "%Y-%m-%d").date()).days)
    if daysDifference > 30:
        return("Date greater than 30 days, Twitter API doesn't support it")
    else:
        return True

def availableTrendsLocation():
    # Parse Available Trends Information
    availableTrends = json.loads(TwitterStream.trends_available())
    for location in availableTrends:
        if location['countryCode'] is 'CA':
            canadianTrends = json.dumps(location)

def userInput():
    # Input: Date, api code, tag or keywords to search for
    keywords = ''
    while not keywords:
        keywords = input('Please enter desired Twitter search: ')

    ask_date_to = True
    while True:
        dateFrom = input('Please enter desired date in YYYY-MM-DD, from: ')
        if not dateFrom:
            ask_date_to = False
            dateTo = ''
            break

        response = validateDate(dateFrom)
        if response is True:
            dateFrom = " since:" + dateFrom
            break
        else:
            print(response)

    while ask_date_to:
        dateTo = input('to:')
        if not dateTo:
            break

        response = validateDate(dateTo)
        if response is True:
            dateTo = " until: " + dateTo
            break
        else:
            print(response)

    # Convert input to URL encoded query
    return urllib.parse.quote_plus(keywords + dateFrom + dateTo)

def main():
    # Set up Twitter api use
    print('User default API and authentications...')
    api = TwitterStream(config.api_key, config.api_secret,
                        config.access_token_key, config.access_token_secret)

    # Get user desired search
    query = userInput()

    f = {'q' : query, 'count': 100, }
    url = urllib.parse(f)

    # Return findings
    tweets = api.search(url)
    print(tweets)
    # Use since_id return for new max_id query, same idea

    # Parse Input, convert Unicode, etc.

    # Detect language (French and English for now)

    # Integrate NLTK, ask its opinion on topic

    # Present data visually

if __name__ == '__main__':
    main()