import mrrapi

mkey = 'YourKey'
msecret = 'YourSecret'

mapi = mrrapi.api(mkey, msecret)
debug = False

def calculateMaxIncome(rigs):
    global outcome, mhash
    mrrdevices = myrigs['data']['records']
    rentalfee = float(0.03)
    outcome = float(0)
    mhash = float(0)
    layout = "{0:>65}{1:>10}{2:>10}{3:>10}{4:>15}{5:>14}"
    print(layout.format("  Device Name  ", " Type ", " Speed ","Price  ", "Daily income", "Rented? "))
    for t in mrrdevices:
        if debug:
            print t
        rigstat = "available"
        mhashrate = float(float(t['hashrate'])/(1000000.0))
        mhash += mhashrate
        dailyprice = mhashrate * float(t['price_mhash']) * (1.0 - rentalfee)
        if (str(t['status']) == 'rented'):
            aih = float(t['available_in'])
            rigstat = "R "
            if 0.1 < aih < 10.0:
                rigstat += " "
            rigstat += str(aih) + " hrs"
        elif (str(t['status']) == 'disabled'):
            rigstat = "disabled"
        print(layout.format(str(t['name']),str(t['type']) ,str(mhashrate) + " MH",str(round(float(t['price_mhash']),6)) ,str(round(dailyprice,8)), rigstat))
        outcome += dailyprice

if __name__ == '__main__':
    myrigs = mapi.myrigs()
    if myrigs['success'] is not True:
        print "Error getting my rig listings"
        print "Make sure you fill in key and secret"
    else:
        calculateMaxIncome(myrigs)
