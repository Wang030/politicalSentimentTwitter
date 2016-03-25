# Coursera_TwitterSentiment
Scripts for analyzing Twitter feed using sentiment scores

Used within the following Coursera course: Data Manipulation at Scale: Systems and Algorithms, from the University of Washington, https://www.coursera.org/learn/data-manipulation

Note that you will have to enter your own Twitter API Code in twitterstream.py before proceeding, specifically

`api_key = "<Enter api key>"
api_secret = "<Enter api secret>"
access_token_key = "<Enter your access token key here>"
access_token_secret = "<Enter your access token secret here>"`

In addition, there is still a lot of refinement needed in:

1. including unicode characters and non-alphanumeric ones,
2. words parsing and separation, and 
3. calculating sentiment beyond just words (but considering phrases and structures as well).
