from math import pow

POSTCODE_DATA = \
    {
        "SG4 9QX": (1,3),
        "SG5 1NR": (8,2)
    }

CLAIM_DATA = \
    [
        ("SG4 9QX", 3.32),
        ("SG4 9QX", 0.17),
        ("SG5 1NR", 0.52)
    ]

THRESHOLD = 50

def crowflies_distance(a,b):
    (ax,ay),(bx,by) = a,b
    return pow(pow(ax-bx,2) + pow(ay-by,2),0.5)

def calc_crosspostcode_smoosh(postcodes,claims):

    claimscore = { p:0.0 for p in postcodes.keys() }

    # add the claims
    for p,s in claims:
        claimscore[p] += s

    smoothedclaims = claimscore.copy()

    for (p,(x,y)) in postcodes.items():
        othercodes = postcodes.copy()
        del othercodes[p]

        distanced = []
        for (oc,(ocx,ocy)) in othercodes.items():
            dist = crowflies_distance((x,y),(ocx,ocy))
            if dist < THRESHOLD:
                distanced.append( (oc,dist) )

        for oc,d in distanced:
            smoothedclaims[oc] += smoothedclaims[p] * 1.0 / pow(dist,2)
        
    return smoothedclaims

def calc_claim_smoosh(postcodes,claims):

    smoothedclaims = { p:0.0 for p in postcodes.keys() }

    # add the claims
    for p,s in claims:
        othercodes = postcodes.copy()
        (x,y) = postcodes[p]
        del othercodes[p]

        distanced = []
        for (oc,(ocx,ocy)) in othercodes.items():
            dist = crowflies_distance((x,y),(ocx,ocy))
            if dist < THRESHOLD:
                distanced.append( (oc,dist) )

        for oc,d in distanced:
            smoothedclaims[oc] += smoothedclaims[p] * 1.0 / pow(dist,2)
        
    return smoothedclaims

if __name__ == '__main__':
    if len(CLAIM_DATA) < len(POSTCODE_DATA):
        answer = calc_claim_smoosh(POSCODE_DATA,CLAIM_DATA)
    else:
        answer = calc_crosspostcode_smoosh(POSTCODE_DATA,CLAIM_DATA)

    for p,s in answer.items():
        print(str.ljust(p,10),s)
