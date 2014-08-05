# -*- coding: utf-8 -*-
# Based off of https://github.com/matveyco/cex.io-api-python
# Modified for MiningRigRentals.com purposes
# Licensed The MIT License

import hmac
import hashlib
import time
import urllib
import urllib2
import json
import os,sys
debug = False

class api:
    __api_key = ''
    __api_secret = ''
    __nonce_v = ''

    # #Init class##
    def __init__(self, api_key, api_secret):
        self.__api_key = api_key
        self.__api_secret = api_secret

    ##get timestamp as nonce
    def __nonce(self):
        self.__nonce_v = '{:.10f}'.format(time.time() * 1000).split('.')[0]

    ##generate signature
    def __signature(self, post_data):
        string = urllib.urlencode(post_data)  ##create string
        signature = hmac.new(self.__api_secret, string, digestmod=hashlib.sha1).hexdigest().upper()  ##create signature
        if debug:
            print "\n __signature"
            print string
            print signature
            print "\n"
        return signature

    def __post(self, url, param):  ##Post Request (Low Level API call)
        params = urllib.urlencode(param)
        sign = self.__signature(param)
        req = urllib2.Request(url, params, {'User-agent': 'Mozilla/4.0 (compatible; MRR API Python client; ' + str(sys.platform) + '; ' + str(sys.version) + ')',
                                            'x-api-key': self.__api_key, 'x-api-sign': sign})
        page = urllib2.urlopen(req).read()
        return page

    def api_call(self, method, param={}):  ## api call (Middle level)
        url = 'https://www.miningrigrentals.com/api/v1/' + method  ##generate url
        self.__nonce()
        param.update({'nonce': self.__nonce_v})
        answer = self.__post(url, param);  ##Post Request
        return json.loads(answer)  ## generate dict and return

    def rig_detail(self, rigID=6900):
        return self.api_call('rigs', {'method': 'detail', 'id': str(rigID)})
    def rig_list(self, minhash, maxhash, mincost, maxcost, rigtype='scrypt', showoff='no',):
        params = {'method': 'list', 'type': str(rigtype), 'showoff': str(showoff)}
        if (float(minhash) > 0):
            params.update({'min_hash': str(minhash)})
        if (float(maxhash) > 0):
            params.update({'max_hash': str(maxhash)})
        if (float(mincost) > 0):
            params.update({'min_cost': str(mincost)})
        if (float(maxcost) > 0):
            params.update({'max_cost': str(maxcost)})
        return self.api_call('rigs', params)