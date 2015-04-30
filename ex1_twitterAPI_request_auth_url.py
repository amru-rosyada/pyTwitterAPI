# example using python twitter API
#
# for testing only, in your case you need to handle callback url and grab oauth_token and oauth_verifier
# for get access token
#
# for authentication grant access
# will return authentication url for grant access

from twitterAPI import TwitterAPI

# create object
# TwitterAPI('CONSUMER SECRET', 'CONSUMER KEY')

t_api = TwitterAPI('rUJ8MepSitKOYoSmaIJS', '49BcA9HPSaD')

# request token
# need callback parameter
# callback is must same with your application callback in twitter apps

request_token = t_api.request_token('http://127.0.0.1:8888/p/authenticate/twitter')

# return token will give dictionary output if operation success
# example output in my case {'oauth_callback_confirmed': 'true', 'oauth_token': 'ITL82qNEmWkh3Uze', 'oauth_token_secret': 'M1XwCvmMffnTD'}

# then use oauth_token for get authentication url
# request authentication url
# use oauth_token as parameter

print(t_api.request_authenticate_url(request_token.get('oauth_token')))

# in my case will give output
# https://api.twitter.com/oauth/authenticate?oauth_token=b0BbomV1nZzFqr8O
# this token only available for 300 second after that you need to regenerate new one

# will give you output grant access url
# open on the browser, in my case output will be like this
# https://api.twitter.com/oauth/authenticate?oauth_token=b0BbomV1nZzFqr8O
# open on the browser and grant access to application