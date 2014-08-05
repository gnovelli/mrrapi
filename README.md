miningrigrentals-api-python
=================

MiningRigRentals.com API integration. Python sources.

##Intro

1. Download lib
2. Get API key and API secret on https://www.miningrigrentals.com/account/apikey account

##How to use?

###1. Create your python project

###2. Add "import mrrapi"

###3. Create class 
```python
  api = mrrapi.api(api_key,api_secret)
```
api_key - your API key
api_secret - your API secret code

###4. Methods and parameters:

####a) API method parametrs
      
####b) API methods

rig_detail(rigID)

rig_list(minhash, maxhash, mincost, maxcost, rigtype='scrypt', showoff='no',)

##TODO: 



- Update a rig
- Add future example
- clean up usage



