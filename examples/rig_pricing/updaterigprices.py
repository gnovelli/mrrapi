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
# Verbose displays useful info. Turn off if you do not want it displayed
verbose = True
# Turn debug on to see all info
debug = False

# your key and secret
mkey = 'YourKey'
msecret = 'YourSecret'

# you device id or list of devices, comma separated
mrrdevices = [7280]
ppalgo = 'SHA256'      # PoolPicker algo: Scrypt, ScryptN, X11, X13, X15, SHA256
mrralgo = 'sha256'     # MRR Algo Name  : scyrpt, scryptn, x11, x13, x15, sha256
# Multipliers to set you rig price by
ppa = 1.25  # When rig is available, add 25% above max poolpicker payout
ppr = 1.35  #    When rig is rented, add 35% above max poolpicker payout
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
    layout = "{0:>45}{1:>20}"
    url = "http://poolpicker.eu/api"
    res = requests.get(url, verify=False)
    if (requests.__version__.split('.')[0] > 0):    #Detect old version of requests used by distros
        tr = res.json()
    else:
        tr = res.json
    if verbose:
        print(layout.format(" Pool Name ", "Payout "))
    for x in tr['pools']:
        if x['profitability'].has_key(algo):
            if x['profitability'][algo][0]['btc']:
                if str(x['name']) not in PoolPickerIgnore:
                    if str(algo) == 'SHA256':
                        algobtc.append(float(x['profitability'][algo][0]['btc'])/10**6) #bring TH down to MH
                        if verbose:
                            print(layout.format(str(x['name']),str(round(float(x['profitability'][algo][0]['btc'])/10**6,12))))
                    else:
                        algobtc.append(float(x['profitability'][algo][0]['btc']))
                        if verbose:
                            print(layout.format(str(x['name']),str(round(float(x['profitability'][algo][0]['btc']),8))))
    if verbose:
        print(layout.format(" ---------------", "  ----------"))
    if len(algobtc) > 0:
        algobtc.sort()
        if verbose:
            print(layout.format(" Max Payout",round(max(algobtc),8) ))
        if debug:
            print algobtc
        return max(algobtc)
    else:
        print "No Pricing available"
        return 1

def getmrrlow(ignoreFirstrigs=0,min_price=0):
    global mrrrigs, mrrprices
    mrrpp = []
    # Get a list of rigs above 10MHs and above min_price of rig_type
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
                    elif debug:
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
            if verbose:
                print "Changing rig " + str(rigDetail['data']['id']) + " price from: " + str(float(rigDetail['data']['price'])) + " to " + str(setPrice)
            mapi.rig_update(str(rigDetail['data']['id']),price=str(setPrice))
        else:
            if verbose:
                print "Rig " + str(rigDetail['data']['id']) + " already at " + str(setPrice)
    else:
        if verbose:
            print "Setting Rig " + str(rigId) + " price: " + str(setPrice)
        mapi.rig_update(str(rigId),price=str(setPrice))

def updatemyRigsPrices(percenta,percentr,setPrice,ppPrice):
    """
    :param percenta: Multiplier for max PoolPicker Price when rig available
    :param percentr: Multiplier for max PoolPicker Price when rig is rented
    :param setPrice: Lowest setPrice to set rig. Lowest rate you will accept
    :param ppPrice: Price from poolpicker or other function. this will be multiplied by percent a and r
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
    layout = "{0:>65}{1:>10}{2:>10}{3:>15}{4:>14}"
    print(layout.format("  Device Name  ", " Speed ","Price  ", "Daily income", "Rented? "))
    for x in mrrdevices:
        t = mapi.rig_detail(x)
        rigstat = "available"
        if (t['success'] == True):
            mhashrate = float(float(t['data']['hashrate']['advertised'])/(1000000.0))
            mhash += mhashrate
            dailyprice = mhashrate * float(t['data']['price']) * (1.0 - rentalfee)
            if (str(t['data']['status']) == 'rented'):
                aih = float(t['data']['available_in_hours'])
                rigstat = "R "
                if 0.1 < aih < 10.0:
                    rigstat += " "
                rigstat += str(aih) + " hrs"
            elif (str(t['data']['status']) == 'unavailable'):
                rigstat = "disabled"
            print(layout.format(str(t['data']['name']),str(mhashrate) + " MH",str(round(float(t['data']['price']),6)) ,str(round(dailyprice,8)), rigstat))
            outcome += dailyprice
        if debug:
            print t

def printCalcs():
    btc_usd = getBTCValue()

    #get the max payout from poolpicker
    ppmax = getPoolPickerAlgo(ppalgo)
    # you can replace getPoolPicker with your own function that returns the highest paying pool price

    # the getmrrlow takes 2 arguments
    #  number of lowest prices to ignore
    #  poolpicker max payout
    mrrlow = getmrrlow(3,ppmax)

    #print "PoolPicker Max: " + str(ppmax)
    print "MRR Lowest    : " + str(mrrlow)
    #The following command triggers all of the work.
    # There are four main argument to updateMyRigsPrices
    #  ppa is set at top of file
    #  ppr is set at top of file
    #  Lowest price we will set
    #  Highest payout on poolpicker
    updatemyRigsPrices(ppa,ppr,mrrlow,ppmax)

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
    #read through printCalcs for explanation and where else to read