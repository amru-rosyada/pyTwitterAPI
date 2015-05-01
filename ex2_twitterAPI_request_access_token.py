# import twitter api

from twitterAPI import TwitterAPI

# create object
# input your oauth_token, oauth_token_secret (from previous step) and oauth_verifier from callback url to request access token

t_api = TwitterAPI('rUJ8MepSitKOYoSmaIJS', '49BcA9HPSaD')

# request_access_token('oauth_token', 'oauth_token_secret', 'oauth_verifier')

print(t_api.request_access_token('b0BbomV1nZzFqr8O', 'M1XwCvmMffnTD', 'QTLTHWAF52trN07q1'))

# in my case it will give an output
# {'oauth_token_secret': 'VN8gw5ESX8eBExLzS8pp', 'user_id': '299', 'oauth_token': '299-2cim9m4d630UKb', 'screen_name': 'sikilkuinc'}
# save it and store it in text file or database, because we can use oauth_token_secret and oauth_token for request an api
# no need step step 1 and step 2 if you already have oauth_token and oauth_token_secret