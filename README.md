miningrigrentals-api-python
=================

MiningRigRentals.com API integration. Python sources.

##Intro

1. Download lib
2. Get API key and API secret on https://www.miningrigrentals.com/account/apikey account

At the moment you can use the ```python setup.py install``` method or just copy mrrapi.py into your project directory.

##How to use?

###1. Create your python project

###2. Add "import mrrapi"

###3. Create class 
```python
  mapi = mrrapi.api(mkey,msecret)
```

mkey - your API key

msecret - your API secret code


###4. Methods and parameters:

- rig_list
- rig_detail
- rig_update

####a) API method parameters
      
####b) API methods

rig_detail(rigID)

rig_list(min_hash=0, max_hash=0, min_cost=0, max_cost=0, rig_type='scrypt', showoff='no', order=None, orderdir=None)

rig_update(rig_id=None, rig_name=None, rig_status=None, hashrate=None, hash_type=None, price=None, min_hours=None, max_hours=None)

## Examples ##

Be sure to change mkey and msecret to your API key/secret if you want to update a rig. 

### Get script rigs over 10 MH/s and under 0.0008

    import mrrapi
    mapi = mrrapi.api('mkey','msecret')
    print mapi.rig_list(10,0,0,0.0008)
    
### Update rig 1000 to available and change price to 0.0009

    import mrrapi
    mapi = mrrapi.api('mkey','msecret')
    print mapi.rig_update(1000,price=0.0009,rig_status='available')



##TODO: 

- Add future example



