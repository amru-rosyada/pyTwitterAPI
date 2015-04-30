# TwitterAPI
#
# this document is GPLV3
# you can changes or modify and redistribute for free
# author : amru rosyada
# email : amru.rosyada@gmail.com
# twitter : @_mru_
# skype : amru.rosyada
#
# usage :
# oauth = TwitterAPI(consumer_secret, consumer_key)
# oauth.request_token() # for request token
# oauth.do_request() # if you want to implement other request just use this one and wrap arround
# twitter using header based authorization when using post method
# we need care about Authorization header payload
# this is implementation wrapper for twitter api version 1.1 with oauth 1.0
import time
from base64 import b64encode
from urllib.parse import quote, parse_qs
from urllib.request import Request, urlopen
from hmac import new as hmac
from hashlib import sha1

class TwitterAPI():
    
    # constructor init parameter is consumer secret and consumer key
    def __init__(self, consumer_secret, consumer_key):
        self.consumer_secret = consumer_secret
        self.consumer_key = consumer_key
        
        # list of dictionary of twitter rest api url
        # access via dicionary get will return url of rest api
        # ex: twitter_rest_api.get('api_authenticate')
        self.twitter_rest_api = {'api_oauth_authenticate':('https://api.twitter.com/oauth/authenticate', 'GET'),
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

    # parameter
    # url_request : api url for request ex https://api.twitter.com/oauth/request_token
    # oauth_token : access token for accessing api this step should be after request granting from user to application
    # oauth_token_secret : access token will concate with consumer secret for generating signing key
    # oauth_callback : required if request oauth token and oauth token sercret, this callback should be same with application callback on api provider
    # request_method can be POST/GET
    # use_headers_auth False/True, depend on provider restriction
    # if use_headers_auth True headers will send with Authorization payload
    # additional_params should be pair key and val as dictionary and will put on payload request
    def do_request(self, url_request='', request_method='GET',
        oauth_token='', oauth_token_secret='',
        oauth_callback='', use_headers_auth=False, additional_params={}):

        oauth_nonce = str(time.time()).replace('.', '')
        oauth_timestamp = str(int(time.time()))

        params = {'oauth_consumer_key':self.consumer_key,
            'oauth_nonce':oauth_nonce,
            'oauth_signature_method':'HMAC-SHA1',
            'oauth_timestamp':oauth_timestamp,
            'oauth_version':'1.0'}

        # if validate callback
        # and request token and token secret
        if(oauth_callback != ''):
            params['oauth_callback'] = oauth_callback

        # if request with token
        if(oauth_token != ''):
            params['oauth_token'] = oauth_token
            
        # if additional parameter exist
        # append to parameter
        for k in additional_params:
            params[k] = additional_params.get(k)

        # create signing key
        # generate oauth_signature
        # key structure oauth standard is [POST/GET]&url_request&parameter_in_alphabetical_order
        params_str = '&'.join(['%s=%s' % (self.percent_quote(k), self.percent_quote(params[k])) for k in sorted(params)])
        message = '&'.join([request_method, self.percent_quote(url_request), self.percent_quote(params_str)])

        # Create a HMAC-SHA1 signature of the message.
        # Concat consumer secret with oauth token secret if token secret available
        # if token secret not available it's mean request token and token secret
        key = '%s&%s' % (self.percent_quote(self.consumer_secret), self.percent_quote(oauth_token_secret)) # Note compulsory "&".
        signature = hmac(key.encode('UTF-8'), message.encode('UTF-8'), sha1)
        digest_base64 = b64encode(signature.digest()).decode('UTF-8')
        params["oauth_signature"] = digest_base64

        # if use_headers_auth
        headers_payload = {}
        if use_headers_auth:
            headers_str_payload = 'OAuth ' + ', '.join(['%s="%s"' % (self.percent_quote(k), self.percent_quote(params[k])) for k in sorted(params)])
            headers_payload['Authorization'] = headers_str_payload

            # if POST method add urlencoded
            if request_method == 'POST':
                headers_payload['Content-Type'] = 'application/x-www-form-urlencoded'
                
            headers_payload['User-Agent'] = 'HTTP Client'
            
        # generate param to be passed into url
        params_str = '&'.join(['%s=%s' % (k, self.percent_quote(params[k])) for k in sorted(params)])
        
        # if method GET append parameter to url_request with ? params_request_str
        # and set params_request_str to None
        # if using get method
        # all parameter should be exposed into get parameter in alphabetical order
        if request_method == 'GET':
            url_request += '?' + params_str
            params_str = None
            
        # if method POST encode data to standard iso
        # post using header based method
        elif request_method == 'POST':
            # encode to standard iso for post method
            params_str = params_str.encode('ISO-8859-1')
        
        # request to provider with
        # return result
        try:
            req = Request(url_request, data=params_str, headers=headers_payload, method=request_method)
            res = urlopen(req)
            return res.readall()
        except Exception as e:
            print(e)
            return None

    # parse query string into dictionary
    # parameter is query string key=valuy&key2=value2
    def qs_to_dict(self, qs_string):
        res = parse_qs(qs_string)
        data_out = {}
        for k in res:
            data_out[k] = res[k][0]
        
        return data_out
        
    # simplify request token
    # get request token
    # required oauth_callback
    def request_token(self, oauth_callback):
        url, method = self.twitter_rest_api.get('api_oauth_request_token')
        
        res = self.do_request(url_request=url,
            request_method=method,
            oauth_callback=oauth_callback,
            use_headers_auth=True)

        # mapping to dictionary
        # return result as dictioanary
        if res:
            return self.qs_to_dict(res.decode('UTF-8'))
            

        # default return is None
        return None

    # request authentication url
    # requred parameter is oauth_token
    # will return request_auth_url for granting permission
    def request_authenticate_url(self, oauth_token):
        url, method = self.twitter_rest_api.get('api_oauth_authenticate')
        
        if oauth_token:
            return '?'.join((url, '='.join(('oauth_token', self.percent_quote(oauth_token)))))
            
        # default value is None
        return None
        
    # request access token
    # parameter oauth_verifier and oauth_token is required 
    def request_access_token(self, oauth_token, oauth_verifier):
        url, method = self.twitter_rest_api.get('api_oauth_access_token')
        
        if oauth_token and oauth_verifier:
            res = self.do_request(url_request=url,
                request_method=method,
                oauth_token=oauth_token,
                oauth_token_secret='',
                oauth_callback='',
                use_headers_auth=True,
                additional_params={'oauth_verifier':oauth_verifier})
                
            # mapping to dictionary
            # return result as dictioanary
            if res:
                return self.qs_to_dict(res.decode('UTF-8'))
                
        # default return none
        return None
        
    # call request api
    # Returns a collection of the most recent Tweets posted by the user indicated by the screen_name or user_id parameters.
    # read twitter rest api for more params optional
    # ex: params = {'param':'value', 'param':'value'}
    # api_type is key of api will called
    # ex: api_type='api_statuses_mentions_timeline'
    def request_api(self, oauth_token, oauth_token_secret, api_type, params={}):
        url, method = self.twitter_rest_api.get(api_type)
        
        # if contain :id then replace with params.get('id')
        if url.find(':id') != -1:
            url = url.replace(':id', params.get('id'))
            
        # if contain :image then replace with params.get('image')
        if url.find(':image') != -1:
            url = url.replace(':image', params.get('image'))
            
        # if contain :slug then replace with params.get('slug')
        if url.find(':slug') != -1:
            url = url.replace(':slug', params.get('slug'))
            
        # if contain :place_id then replace with params.get('place_id')
        if url.find(':place_id') != -1:
            url = url.replace(':place_id', params.get('place_id'))
            
        res = self.do_request(url_request=url,
                request_method=method,
                oauth_token=oauth_token,
                oauth_token_secret=oauth_token_secret,
                oauth_callback='',
                use_headers_auth=True,
                additional_params=params)
                
        return res.decode('UTF-8')

    # percent_quote
    # quote url as percent quote
    def percent_quote(self, text):
        return quote(text, '~')
        