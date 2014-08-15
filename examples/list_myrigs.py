import mrrapi

mkey = 'YourKey'
msecret = 'YourSecret'

mapi = mrrapi.api(mkey,msecret)
debug = False

def parsemyrigs(rigs):
    """
    :param rigs: pass the raw api return from mrrapi.myrigs()
    :return: returns dict by algorithm
    """
    global mrrrigs
    mrrrigs = {}
    # I am not a python programmer, do you know a better way to do this?
    # first loop to create algo keys
    # second loop populates rigs in algo
    for x in myrigs['data']['records']:
        mrrrigs.update({str(x['type']): {}})
    for x in myrigs['data']['records']:
        mrrrigs[str(x['type'])][int(x['id'])] = str(x['name'])
    return mrrrigs

def calculateMaxIncomeAlgo(parsedrigs):
    global mhash
    rentalfee = float(0.03)
    outcome = float(0)
    mhash = float(0)

    namelen = 0

    # Pre-process loop
    for algo in parsedrigs:
        algorigs = parsedrigs[algo]
        for x in algorigs:
            nametmp = len(parsedrigs[algo][x])
            if nametmp > namelen:
                namelen = nametmp
            #print x, algo, namelen
    layout = "{0:>" + str(namelen) + "}{1:>10}{2:>10}{3:>12}{4:>15}{5:>14}"
    print(layout.format("  Device Name  ", " Type ", " Speed ","Price  ", "Daily income", "Rented? "))

    for algo in parsedrigs:
        algorigs = parsedrigs[algo]
        for x in algorigs:
            rig = mapi.rig_detail(x)
            t = rig['data']
            if debug:
                print t
            rigstat = "available"
            mhashrate = float(float(t['hashrate']['advertised'])/(1000000.0))
            mhash += mhashrate
            dailyprice = mhashrate * float(t['price']) * (1.0 - rentalfee)
            if (str(t['status']) == 'rented'):
                aih = float(t['available_in_hours'])
                rigstat = "R "
                if 0.1 < aih < 10.0:
                    rigstat += " "
                rigstat += str(aih) + " hrs"
            elif (str(t['status']) == 'unavailable'):
                rigstat = "disabled"
            print(layout.format(str(t['name']),str(t['type']),str(mhashrate) + " MH",str(round(float(t['price']),8)) ,str(round(dailyprice,8)), rigstat))
            outcome += dailyprice

    return outcome

if __name__ == '__main__':
    myrigs = mapi.myrigs()
    if myrigs['success'] is not True:
        print "Error getting my rig listings"
        print "Make sure you fill in key and secret"
    else:
        prigs = parsemyrigs(myrigs)
        #print prigs
        maxi = calculateMaxIncomeAlgo(prigs)
        print
        print "Max available daily income: " + str(round(maxi,8) - 0.002)

