import json
import geopy.geocoders import Nominatim

class ParsingTwitterJson:
    def __init__(self, file):
        self.tweets = []
        try:
            for line in open(file, 'r'):
                self.tweets.append(json.loads(line))
        except FileNotFoundError:
            raise ('Error loading Twitter JSON file. Please double-check input.')

    def determine_location(self, latitude, longitude):
        '''
        Return an address, city, province and country based on coordinates
        '''
        geolocator = Nominatim()
        return geolocator.reverse(latitude, longitude)

    def clean_data(self, region, lang = ['en','fr']):
        '''
        Clean up data and filter by language, location and time
        '''
        for tweet in self.tweets:

            # Clean up by language
            if tweet.lang not in lang:
                self.tweets.remove(tweet)

            # Clean up by location
                if region:



    '''
    Valuable Tweet Info
    created_at
    coordinates
    entities()
    lang
    place
    text
    user.lang
    user.location
    '''