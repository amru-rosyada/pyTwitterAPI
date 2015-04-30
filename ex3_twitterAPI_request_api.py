# call REST API
# call request api
# Returns a collection of the most recent Tweets posted by the user indicated by the screen_name or user_id parameters.
# read twitter rest api for more params optional
# ex: params = {'param':'value', 'param':'value'}
# api_type is key of api will called
# ex: api_type='api_statuses_mentions_timeline'
# def request_api(self, oauth_token, oauth_token_secret, api_type, params={}):

from twitterAPI import TwitterAPI
t_api = TwitterAPI('rUJ8MepSitKOYoSmaIJS', '49BcA9HPSaD')

# use api_type='api_statuses_user_timeline' for request https://api.twitter.com/1.1/statuses/user_timeline.json
# request_api(oauth_token, oauth_token_secret, api_type, params={})
# params in dictionary
# param key is same with twitter api
# ex i want to get user_timeline with user_id='299' and count='2'
# all parameter should be in string format
# in my case I will use this information from previous step {'oauth_token_secret': 'VN8gw5ESX8eBExLzS8pp', 'user_id': '299', 'oauth_token': '299-2cim9m4d630UKb', 'screen_name': 'sikilkuinc'}

params = {'user_id':'299', 'count':'2'}
print(t_api.request_api('299-2cim9m4d630UKb', 'VN8gw5ESX8eBExLzS8pp', 'api_statuses_mentions_timeline', params))

# output will be in json format