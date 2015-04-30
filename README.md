# pyTwitterAPI
python wrapper for simplify twitter rest API (I code using Python v3.4, if it's not working on older python release you can modify this code and commit to this repository :-))

This software is GPLV3
You can modify and redistribute free of charge :-)
This is python code to simplify access using twitter REST API https://dev.twitter.com/rest/public
Implementation using oauth and browser callback for authentication grant access

How to use this twitterAPI?

#A. authentication process
<pre>
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
</pre>

#B. grant access to the application and get access token
After open link in browser in my case i use https://api.twitter.com/oauth/authenticate?oauth_token=b0BbomV1nZzFqr8O
After granting access it will be redirect to your callback url in my case i use http://127.0.0.1:8888/p/authenticate/twitter
If valid it will automatically redirect to your callback url with oauth_token and oauth_verifier, in my case it will be redirect to http://127.0.0.1:8888/p/authenticate/twitter?oauth_token=b0BbomV1nZzFqr8Oc&oauth_verifier=QTLTHWAF52trN07q1

then user oauth_token and oauth_verifier to get access token
<pre>
# import twitter api

from twitterAPI import TwitterAPI

# create object
# input your oauth_token and oauth_verifier from callback url to request access token

t_api = TwitterAPI('rUJ8MepSitKOYoSmaIJS', '49BcA9HPSaD')

# request_access_token('oauth_token', 'oauth_verifier')

print(t_api.request_access_token('b0BbomV1nZzFqr8O', 'QTLTHWAF52trN07q1'))

# in my case it will give an output
# {'oauth_token_secret': 'VN8gw5ESX8eBExLzS8pp', 'user_id': '299', 'oauth_token': '299-2cim9m4d630UKb', 'screen_name': 'sikilkuinc'}
# save it and store it in text file or database, because we can use oauth_token_secret and oauth_token for request an api
# no need step step 1 and step 2 if you already have oauth_token and oauth_token_secret
</pre>

#C. request api with token and token secret
in my case I use my token and token secret
if i want call request to https://api.twitter.com/1.1/statuses/user_timeline.json twitter REST API
just use this code:
<pre>
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
</pre>

#D. API Type and Paramter
All url request already encapsulated in my code you only need call the name of url type, for parameter when request you need refer to twitter REST API https://dev.twitter.com/rest/public

here the list of mapping REST api url:
<pre>
{'api_oauth_authenticate':('https://api.twitter.com/oauth/authenticate', 'GET'),
'api_oauth_request_token':('https://api.twitter.com/oauth/request_token', 'POST'),
'api_oauth_access_token':('https://api.twitter.com/oauth/access_token', 'POST'),
'api_statuses_mentions_timeline':('https://api.twitter.com/1.1/statuses/mentions_timeline.json', 'GET'),
'api_statuses_user_timeline':('https://api.twitter.com/1.1/statuses/user_timeline.json', 'GET'),
'api_statuses_home_timeline':('https://api.twitter.com/1.1/statuses/home_timeline.json', 'GET'),
'api_statuses_retweets_of_me':('https://api.twitter.com/1.1/statuses/retweets_of_me.json', 'GET'),
'api_statuses_retweets_id':('https://api.twitter.com/1.1/statuses/retweets/:id.json', 'GET'),
'api_statuses_show':('https://api.twitter.com/1.1/statuses/show.json', 'GET'),
'api_statuses_destroy_id':('https://api.twitter.com/1.1/statuses/destroy/:id.json', 'GET'),
'api_statuses_update':('https://api.twitter.com/1.1/statuses/update.json', 'POST'),
'api_statuses_retweet':('https://api.twitter.com/1.1/statuses/retweet/:id.json', 'POST'),
'api_statuses_oembed':('https://api.twitter.com/1.1/statuses/oembed.json', 'GET'),
'api_statuses_retweeters_ids':('https://api.twitter.com/1.1/statuses/retweeters/ids.json', 'GET'),
'api_statuses_lookup':('https://api.twitter.com/1.1/statuses/lookup.json', 'GET'),
'api_media_upload':('https://upload.twitter.com/1.1/media/upload.json', 'POST'),
'api_direct_messages_sent':('https://api.twitter.com/1.1/direct_messages/sent.json', 'GET'),
'api_direct_messages_show':('https://api.twitter.com/1.1/direct_messages/show.json', 'GET'),
'api_search_tweets':('https://api.twitter.com/1.1/search/tweets.json', 'GET'),
'api_direct_messages':('https://api.twitter.com/1.1/direct_messages.json', 'GET'),
'api_direct_messages_destroy':('https://api.twitter.com/1.1/direct_messages/destroy.json', 'POST'),
'api_direct_messages_new':('https://api.twitter.com/1.1/direct_messages/new.json', 'POST'),
'api_friendships_no_retweets_ids':('https://api.twitter.com/1.1/friendships/no_retweets/ids.json', 'GET'),
'api_friends_ids':('https://api.twitter.com/1.1/friends/ids.json', 'GET'),
'api_followers_ids':('https://api.twitter.com/1.1/followers/ids.json', 'GET'),
'api_friendships_incoming':('https://api.twitter.com/1.1/friendships/incoming.json', 'GET'),
'api_friendships_outgoing':('https://api.twitter.com/1.1/friendships/outgoing.json', 'GET'),
'api_friendships_create':('https://api.twitter.com/1.1/friendships/create.json', 'POST'),
'api_friendships_destroy':('https://api.twitter.com/1.1/friendships/destroy.json', 'POST'),
'api_friendships_update':('https://api.twitter.com/1.1/friendships/update.json', 'POST'),
'api_friendships_show':('https://api.twitter.com/1.1/friendships/show.json', 'GET'),
'api_friends_list':('https://api.twitter.com/1.1/friends/list.json', 'GET'),
'api_followers_list':('https://api.twitter.com/1.1/followers/list.json', 'GET'),
'api_friendships_lookup':('https://api.twitter.com/1.1/friendships/lookup.json', 'GET'),
'api_account_get_settings':('https://api.twitter.com/1.1/account/settings.json', 'GET'),
'api_account_verify_credentials':('https://api.twitter.com/1.1/account/verify_credentials.json', 'GET'),
'api_account_post_settings':('https://api.twitter.com/1.1/account/settings.json', 'POST'),
'api_account_update_delivery_device':('https://api.twitter.com/1.1/account/update_delivery_device.json', 'POST'),
'api_account_update_profile':('https://api.twitter.com/1.1/account/update_profile.json', 'POST'),
'api_account_update_profile_background_image':('https://api.twitter.com/1.1/account/update_profile_background_image.json', 'POST'),
'api_account_update_profile_image':('https://api.twitter.com/1.1/account/update_profile_image.json?image=:image', 'POST'),
'api_blocks_list':('https://api.twitter.com/1.1/blocks/list.json', 'GET'),
'api_blocks_ids':('https://api.twitter.com/1.1/blocks/ids.json', 'GET'),
'api_blocks_create':('https://api.twitter.com/1.1/blocks/create.json', 'POST'),
'api_blocks_destroy':('https://api.twitter.com/1.1/blocks/destroy.json', 'POST'),
'api_users_lookup':('https://api.twitter.com/1.1/users/lookup.json', 'GET'),
'api_users_show':('https://api.twitter.com/1.1/users/show.json', 'GET'),
'api_users_search':('https://api.twitter.com/1.1/users/search.json', 'GET'),
'api_account_remove_profile_banner':('https://api.twitter.com/1.1/account/remove_profile_banner.json', 'POST'),
'api_account_update_profile_banner':('https://api.twitter.com/1.1/account/update_profile_banner.json', 'POST'),
'api_users_profile_banner':('https://api.twitter.com/1.1/users/profile_banner.json', 'GET'),
'api_mutes_users_create':('https://api.twitter.com/1.1/mutes/users/create.json', 'POST'),
'api_mutes_users_destroy':('https://api.twitter.com/1.1/mutes/users/destroy.json', 'POST'),
'api_mutes_users_ids':('https://api.twitter.com/1.1/mutes/users/ids.json', 'GET'),
'api_mutes_users_list':('https://api.twitter.com/1.1/mutes/users/list.json', 'GET'),
'api_users_suggestions_slug':('https://api.twitter.com/1.1/users/suggestions/:slug.json', 'GET'),
'api_users_suggestions':('https://api.twitter.com/1.1/users/suggestions.json', 'GET'),
'api_users_suggestions_slug_members':('https://api.twitter.com/1.1/users/suggestions/:slug/members.json', 'GET'),
'api_favorites_list':('https://api.twitter.com/1.1/favorites/list.json', 'GET'),
'api_favorites_destroy':('https://api.twitter.com/1.1/favorites/destroy.json', 'POST'),
'api_favorites_create':('https://api.twitter.com/1.1/favorites/create.json', 'POST'),
'api_lists_list':('https://api.twitter.com/1.1/lists/list.json', 'GET'),
'api_lists_statuses':('https://api.twitter.com/1.1/lists/statuses.json', 'GET'),
'api_lists_members_destroy':('https://api.twitter.com/1.1/lists/members/destroy.json', 'POST'),
'api_lists_memberships':('https://api.twitter.com/1.1/lists/memberships.json', 'GET'),
'api_lists_subscribers':('https://api.twitter.com/1.1/lists/subscribers.json', 'GET'),
'api_lists_subscribers_create':('https://api.twitter.com/1.1/lists/subscribers/create.json', 'POST'),
'api_lists_subscribers_show':('https://api.twitter.com/1.1/lists/subscribers/show.json ', 'GET'),
'api_lists_subscribers_destroy':('https://api.twitter.com/1.1/lists/subscribers/destroy.json ', 'POST'),
'api_lists_members_create_all':('https://api.twitter.com/1.1/lists/members/create_all.json ', 'POST'),
'api_lists_members_show':('https://api.twitter.com/1.1/lists/members/show.json ', 'GET'),
'api_lists_members':('https://api.twitter.com/1.1/lists/members.json', 'GET'),
'api_lists_members_create':('https://api.twitter.com/1.1/lists/members/create.json', 'POST'),
'api_lists_destroy':('https://api.twitter.com/1.1/lists/destroy.json ', 'POST'),
'api_lists_update':('https://api.twitter.com/1.1/lists/update.json', 'POST'),
'api_lists_create':('https://api.twitter.com/1.1/lists/create.json', 'POST'),
'api_lists_show':('https://api.twitter.com/1.1/lists/show.json', 'GET'),
'api_lists_subscriptions':('https://api.twitter.com/1.1/lists/subscriptions.json', 'GET'),
'api_lists_members_destroy_all':('https://api.twitter.com/1.1/lists/members/destroy_all.json ', 'POST'),
'api_lists_ownerships':('https://api.twitter.com/1.1/lists/ownerships.json', 'GET'),
'api_saved_searches_list':('https://api.twitter.com/1.1/saved_searches/list.json', 'GET'),
'api_saved_searches_show':('https://api.twitter.com/1.1/saved_searches/show/:id.json', 'GET'),
'api_saved_searches_create':('https://api.twitter.com/1.1/saved_searches/create.json', 'POST'),
'api_saved_searches_destroy':('https://api.twitter.com/1.1/saved_searches/destroy/:id.json', 'POST'),
'api_geo_id_place_id':('https://api.twitter.com/1.1/geo/id/:place_id.json', 'GET'),
'api_geo_reverse_geocode':('https://api.twitter.com/1.1/geo/reverse_geocode.json', 'GET'),
'api_geo_search':('https://api.twitter.com/1.1/geo/search.json', 'GET'),
'api_geo_place':('https://api.twitter.com/1.1/geo/place.json', 'POST'),
'api_trends_place':('https://api.twitter.com/1.1/trends/place.json', 'GET'),
'api_trends_available':('https://api.twitter.com/1.1/trends/available.json', 'GET'),
'api_application_rate_limit_status':('https://api.twitter.com/1.1/application/rate_limit_status.json', 'GET'),
'api_help_configuration':('https://api.twitter.com/1.1/help/configuration.json', 'GET'),
'api_help_languages':('https://api.twitter.com/1.1/help/languages.json', 'GET'),
'api_help_privacy':('https://api.twitter.com/1.1/help/privacy.json', 'GET'),
'api_help_tos':('https://api.twitter.com/1.1/help/tos.json', 'GET'),
'api_trends_closest':('https://api.twitter.com/1.1/trends/closest.json', 'GET'),
'api_users_report_spam':('https://api.twitter.com/1.1/users/report_spam.json', 'POST')}
</pre>

api_type='api_users_report_spam' or api_type='api_trends_closest' etc.

ex:
params = {'param_1':'xxx', 'param_2':'xxx'}
print(t_api.request_api('299-2cim9m4d630UKb', 'VN8gw5ESX8eBExLzS8pp', 'api_trends_closest', params))

params should be refer to twitter REST API,
