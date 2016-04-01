import datetime, urllib.parse, json, TwitterStream as TwitterStream

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