#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import codecs,sys
import json
import urllib2
from datetime import datetime
import time
import os
import mrrapi
##############################################################################
##############################################################################
# Change settings here
debug = False
verbose = False

# your key and secret
mkey = 'YourKey'
msecret = 'YourSecret'

# you device id or list of devices, comma separated
mrrdevices = [7281]
ppalgo = 'X11'      #PoolPicker algo
mrralgo = 'x11'     #MRR Algo Name
# Pools to ignore from poolpicker
PoolPickerIgnore = ['AltMining.Farm','bobpool']
##############################################################################
##############################################################################
##############################################################################
mapi = mrrapi.api(mkey,msecret)
reload(sys)
sys.setdefaultencoding('utf-8')

mrrrigs = {}
mrrprices = []

def getBTCValue():
    # https://www.bitstamp.net/api/  BTC -> USD
    bitstampurl = "https://www.bitstamp.net/api/ticker/"
    bsjson = urllib2.urlopen(bitstampurl).read()
    dbstamp_params = json.loads(bsjson)
    btc_usd = float(dbstamp_params['last'])
    return btc_usd

def getPoolPickerAlgo(algo='ScryptN'):
    algobtc =[]
    layout = "{0:>25}{1:>15}"
    url = "http://poolpicker.eu/api"
    res = requests.get(url, verify=False)
    if (os.name == 'nt'):
        tr = res.json()
    else:
        tr = res.json
    for x in tr['pools']:
        if x['profitability'].has_key(algo):
            if x['profitability'][algo][0]['btc']:
                if str(x['name']) not in PoolPickerIgnore:
                    algobtc.append(float(x['profitability'][algo][0]['btc']))
                    print(layout.format(str(x['name']),str(round(float(x['profitability'][algo][0]['btc']),8))))
                else:
                    #Skip this pool
                    pass
    if len(algobtc) > 0:
        algobtc.sort()
        if debug:
            print algobtc
        return max(algobtc)
    else:
        return 1

def getmrrlow(ignoreFirstrigs=0,min_price=0):
    global mrrrigs, mrrprices
    mrrpp = []
    # Get a list of rigs above 10MHs and above the max poolpicker payout
    mrrp = mapi.rig_list(10,0,min_price,rig_type=mrralgo)
    if (str(mrrp['success'] == 'True') and len(mrrp['data']['records']) > 0):   #make sure we have valid data
        for x in mrrp['data']['records']:
            if int(x['id']) not in mrrdevices:                                  #make sure it is not my rig
                if debug:
                    print x
                if str(x['status']).lower() == 'available':                     #only compare available rigs
                    if float(x['rating']) > 4.0:                                #only compare highly rated rigs
                        mrrrigs.update({int(x['id']): {'hashrate': float(x['hashrate']), 'price': float(x['price_mhash'])}})
                        mrrpp.append(float(x['price_mhash']))
                    elif verbose:
                        print "Ignoring rig: " + str(x['id']) + " With a rating of " + str(x['rating']) + " for " + str(x['name'])
        for e in mrrpp:
            if e not in mrrprices:
               mrrprices.append(e)
        mrrprices.sort()
        if len(mrrprices) > ignoreFirstrigs:
            if debug:
                print mrrprices[ignoreFirstrigs - 1]
            return mrrprices[ignoreFirstrigs - 1]
        elif len(mrrprices) > 0:
            print "WARNING: " + str(len(mrrprices)) + " prices instead of " + str(ignoreFirstrigs) + " asked for. "
            ignoreFirstrigs = len(mrrprices) - 1
            if debug:
                print mrrprices[ignoreFirstrigs]
            return mrrprices[ignoreFirstrigs]
        else:
            print "Problem with pricing length"
            return 1
    else:
        print "MRR Data failure or no rigs in specs"
        return 1

def setRigPrice(rigId,setPrice,rigDetail=None):
    if rigDetail is not None:
        if float(rigDetail['data']['price']) != float(setPrice):
            print "Changing rig price from: " + str(float(rigDetail['data']['price'])) + " to " + str(setPrice)
            mapi.rig_update(str(rigDetail['data']['id']),price=str(setPrice))
        else:
            if verbose:
                print "Rig " + str(rigDetail['data']['id']) + " already at " + str(setPrice)
    else:
        print "Setting Rig " + str(rigId) + " price: " + str(setPrice)
        mapi.rig_update(str(rigId),price=str(setPrice))

def updatemyRigsPrices(percenta,percentr,setPrice,ppPrice):
    """
    :param percenta: Multiplier for max PoolPicker Price when rig available
    :param percentr: Multiplier for max PoolPicker Price when rig is rented
    :param setPrice: Lowest setPrice to set rig
    :return:
    """
    for x in mrrdevices:
        t = mapi.rig_detail(x)
        if debug:
            print t
        if str(t['data']['status']) == 'available':
            if setPrice > (ppPrice * percenta):
                setRigPrice(x,setPrice,t)
            else:
                setRigPrice(x,(ppPrice * percenta),t)
        elif str(t['data']['status']) == 'rented':
            if setPrice > (ppPrice * percentr):
                setRigPrice(x,setPrice,t)
            else:
                setRigPrice(x,(ppPrice * percentr),t)
        else:
            if setPrice > (ppPrice * percentr):
                setRigPrice(x,setPrice,t)
            else:
                setRigPrice(x,(ppPrice * percentr),t)


def calculateMaxIncomeA():
    global outcome, mhash
    rentalfee = float(0.035)
    outcome = float(0)
    mhash = float(0)
    layout = "{0:>65}{1:>10}{2:>10}{3:>15}{4:>12}"
    print(layout.format("  Device Name  ", " Speed","Price", "Daily income", "Rented?"))
    for x in mrrdevices:
        t = mapi.rig_detail(x)
        if (t['success'] == True):
            mhashrate = float(float(t['data']['hashrate']['advertised'])/(1000000.0))
            mhash += mhashrate
            dailyprice = mhashrate * float(t['data']['price']) * (1.0 - rentalfee)
            print(layout.format(str(t['data']['name']),str(mhashrate) + " MH",str(round(float(t['data']['price']),6)) ,str(dailyprice), str(t['data']['status'])))
            outcome += dailyprice

def printCalcs():
    btc_usd = getBTCValue()

    #get the max payout from poolpicker
    ppmax = getPoolPickerAlgo(ppalgo)

    # the getmrrlow takes 2 arguments
    #  number of lowest prices to ignore
    #  poolpicker max payout
    mrrlow = getmrrlow(3,ppmax)

    print "PoolPicker Max: " + str(ppmax)
    print "MRR Lowest    : " + str(mrrlow)
    #The following command triggers all of the work.
    # There are four main argument to updateMyRigsPrices
    #  We want to rent our rig by at least 25% above the highest paying pool on poolpicker
    #  We will raise our price to 40% over poolpicker while our rig is rented
    #  Lowest price we will set
    #  Highest payout on poolpicker
    updatemyRigsPrices(1.25,1.4,mrrlow,ppmax)

    calculateMaxIncomeA()
    mrrdaily = outcome - 0.0002

    print "Total Hashing power: " + str(mhash)
    print "MRR BTC: " + str(mrrdaily) + " USD: " + str(mrrdaily * btc_usd)
    #print "Max weekly perfect conditions: ",
    #print (outcome - 0.0002) * btc_usd * 7
    #print "Likely weekly rentals (90%): " + str((0.9 * outcome - 0.0002) * btc_usd * 7)
    #print "CM Weekly: " + str(cmdaily * btc_usd * 7)


if __name__ == '__main__':
    printCalcs()
