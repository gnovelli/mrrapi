============================================================
 miningrigrentals-api-python
============================================================
------------------------------------------------------------
MiningRigRentals.com API integration. Python sources.
------------------------------------------------------------

Intro
======
1. Download lib or pip install mrrapi
2. Get API key and API secret on https://www.miningrigrentals.com/account/apikey account
3. Run an example or create your own code
4. (Required if you want to run included console scripts) put a file called mrrapi.cfg in you home directory or ~/.mrrapi/

How to use
===========
1. Create your python project
2. Add "import mrrapi"
3. Create class

>>> mapi = mrrapi.api(mkey,msecret)

::

    mkey - your API key
    msecret - your API secret code

Methods and parameters
-----------------------
- myrigs
- rig_list
- rig_detail
- rig_update

myrigs
^^^^^^^^^^^^^^^^^^^^^
myrigs does not take any parameters, but must be authenticated with a valid API key

rig_list
^^^^^^^^^^^^^^^^^^^^^
rig_list(min_hash=0, max_hash=0, min_cost=0, max_cost=0, rig_type='scrypt', showoff='no', order=None, orderdir=None)

The parameters to rig_list can be either positional and named. The parameters have default arguments so you do not have to pass any in if you do not want to. 

rig_detail
^^^^^^^^^^^^^^^^^^^^^
rig_detail(rig_id)

This only takes one argument and that is the ID of the rig. 

rig_update
^^^^^^^^^^^^^^^^^^^^^
rig_update(rig_id=None, rig_name=None, rig_status=None, hashrate=None, hash_type=None, price=None,
 min_hours=None, max_hours=None)

rig_id is mandatory. One other argument is required. Must be authenticated with a valid API key. 


Simple Examples
=================

Be sure to change mkey and msecret to your API key/secret if you want to update or list your rigs. 

Get script rigs over 10 MH/s and under 0.00045
-----------------------------------------------

>>> import mrrapi
>>> mapi = mrrapi.api('mkey','msecret')
>>> print mapi.rig_list(10,0,0,0.00045)
{u'version': u'1', u'data': {u'info': {u'available': {u'rigs': u'182', u'hash': u'14135295000'}, u'rented': {u'rigs': u'57', u'hash': u'2858908800'}, u'start_num': 1, u'end_num': u'2', u'price': {u'lowest': u'0.00046', u'last_10': u'0.00047476', u'last': u'0.0005'}, u'total': u'2'}, u'records': [{u'price_hr': u'0.00050625', u'rating': u'4.97', u'maxhrs': u'720', u'hashrate_nice': u'27.00M', u'price': u'0.00045', u'minhrs': u'3', u'status': u'rented', u'available_in_hours': u'0.134', u'id': u'5466', u'hashrate': u'27000000', u'name': u'Zeus Thunder X3. Ancient god of hashrate.'}, {u'price_hr': u'0.00024375', u'rating': u'0.00', u'maxhrs': u'24', u'hashrate_nice': u'13.00M', u'price': u'0.00045', u'minhrs': u'3', u'status': u'rented', u'available_in_hours': u'15.449', u'id': u'7634', u'hashrate': u'13000000', u'name': u'Chi-Town BW'}]}, u'success': True}


Update rig 1000 to available and change price to 0.0009
---------------------------------------------------------
>>> import mrrapi
>>> mapi = mrrapi.api('mkey','msecret')
>>> print mapi.rig_update(1000,price=0.0009,rig_status='available')
{u'version': u'1', u'data': u'success', u'success': True}


