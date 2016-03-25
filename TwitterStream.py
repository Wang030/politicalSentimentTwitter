import oauth2 as oauth
import urllib.request as urllib


class TwitterStream:
    def __init__(self, api_key, api_secret, access_token_key, access_token_secret):
        # Input your own api credentials from Twitter API
        self.api_key = api_key  # <Enter api key>
        self.api_secret = api_secret  # <Enter api secret>"
        self.access_token_key = access_token_key  # <Enter your access token key here>"
        self.access_token_secret = access_token_secret  # <Enter your access token secret here>"

        _debug = 0

        self.oauth_token = oauth.Token(key=self.access_token_key, secret=self.access_token_secret)
        self.oauth_consumer = oauth.Consumer(key=self.api_key, secret=self.api_secret)

        self.signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

        self.http_handler = urllib.HTTPHandler(debuglevel=_debug)
        self.https_handler = urllib.HTTPSHandler(debuglevel=_debug)

    def _twitterreq(self, url, method, parameters):
        """
        Construct, sign, and open a twitter request
        using the hard-coded credentials above.
        """

        req = oauth.Request.from_consumer_and_token(self.oauth_consumer,
                                                    token=self.oauth_token,
                                                    http_method=method,
                                                    http_url=url,
                                                    parameters=parameters
                                                    )

        req.sign_request(self.signature_method_hmac_sha1, self.oauth_consumer, self.oauth_token)

        if method == "POST":
            encoded_post_data = req.to_postdata()
        else:
            encoded_post_data = None
            url = req.to_url()

        opener = urllib.OpenerDirector()
        opener.add_handler(self.http_handler)
        opener.add_handler(self.https_handler)

        response = opener.open(url, encoded_post_data)

        return response

    def fetch(self):
        url = "https://stream.twitter.com/1/statuses/sample.json"
        parameters = []
        response = self._twitterreq(url, "GET", parameters)
        return response
