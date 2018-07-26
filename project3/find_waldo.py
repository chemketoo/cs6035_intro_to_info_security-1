#!/usr/bin/python
import json, sys, hashlib

def usage():
    print """Usage:
    python find_waldo.py student_id (i.e., qchenxiong3)"""
    sys.exit(1)

#TODO -- n1 and n2 share p or q?
def is_waldo(n1, n2):

    #your code start here
    index = 2
    if n1>n2 :
        r_temp = n1 % n2
        r = [n1,n2]
    else :
        r_temp = n2 % n1
        r = [n2,n1]

    while(r_temp != 0):
        r_temp = r[index-2] % r[index-1]
        r.append(r_temp)
        index = index + 1
    result=(r[index-2]!=1)
    # your code ends here
    return result


def get_private_key(n1, n2, e):

    index = 2
    if n1>n2 :
        r_temp = n1 % n2
        r = [n1,n2]
    else :
        r_temp = n2 % n1
        r = [n2,n1]

    while(r_temp != 0):
        r_temp = r[index-2] % r[index-1]
        r.append(r_temp)
        index = index + 1
    p = r[index-2]
    mod_n = (p-1)*(n1/p-1)
    k=1
    temp = (mod_n * k +1)% e
    result = (mod_n * k +1)/e
    while( temp !=0 and result < mod_n ):
        k = k+1
        temp = (mod_n * k +1)% e
    result = (mod_n * k +1)/e
    d = result    
    #your code ends here

    return d

def main():
    if len(sys.argv) != 2:
        usage()

    all_keys = None
    with open("keys4student.json", 'r') as f:
        all_keys = json.load(f)

    name = hashlib.sha224(sys.argv[1].strip()).hexdigest()
    if name not in all_keys:
        print sys.argv[1], "not in keylist"
        usage()

    pub_key = all_keys[name]
    n1 = int(pub_key['N'], 16)
    e = int(pub_key['e'], 16)
    d = 0
    waldo = "dolores"

    print "your public key: (", hex(n1).rstrip("L"), ",", hex(e).rstrip("L"), ")"

    for classmate in all_keys:
        if classmate == name:
            continue
        n2 = int(all_keys[classmate]['N'], 16)
        

        if is_waldo(n1, n2):
            waldo = classmate
            d = get_private_key(n1, n2, e)
            break
    
    print "your private key: ", hex(d).rstrip("L")
    print "your waldo: ", waldo


if __name__ == "__main__":
    main()
