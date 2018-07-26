#!/usr/bin/python
import json, sys, hashlib
from decimal import *
import gmpy2

def usage():
    print """Usage:
    python recover.py student_id (i.e., qchenxiong3)"""
    sys.exit(1)

#TODO
def recover_msg(N1, N2, N3, C1, C2, C3):

    N = N1*N2*N3
    y1 = N/N1
    y2 = N/N2
    y3 = N/N3

    s1=[1,0]
    r1=[y1,N1]
    index = 2
    r_temp = y1%N1
    while (r_temp > 0):
        r_temp = r1[index-2] % r1[index-1]
        q_temp = r1[index-2]/r1[index-1]
        s_temp = s1[index-2]-q_temp*s1[index-1] 
        r1.append(r_temp)
        s1.append(s_temp)
        index = index + 1
#        print(r_temp)    
    z1=s1[index-2]
    if z1 < 0: z1 += N1
#    print(z1)    

    s2=[1,0]
    r2=[y2,N2]
    index = 2
    r_temp = y2%N2
    while (r_temp > 0):
        r_temp = r2[index-2] % r2[index-1]
        q_temp = r2[index-2]/r2[index-1]
        s_temp = s2[index-2]-q_temp*s2[index-1] 
        r2.append(r_temp)
        s2.append(s_temp)
        index = index + 1
#        print(r_temp)    
    z2=s2[index-2]
    if z2 < 0: z2 += N2
#    print(z2)    

    s3=[1,0]
    r3=[y3,N3]
    index = 2
    r_temp = y3%N3
    while (r_temp > 0):
        r_temp = r3[index-2] % r3[index-1]
        q_temp = r3[index-2]/r3[index-1]
        s_temp = s3[index-2]-q_temp*s3[index-1] 
        r3.append(r_temp)
        s3.append(s_temp)
        index = index + 1
#        print(r_temp)    
    z3=s3[index-2]
    if z3 < 0: z3 += N3
#    print(z3)    
    x=(z1*C1*y1+z2*C2*y2+z3*C3*y3)%N 

    k=0
    gmpy2.set_context(gmpy2.context())
    gmpy2.get_context().precision=1000000
    m_temp=gmpy2.cbrt(x)
#    m_temp = Decimal((k*N + x))**Decimal(1.0/3.0)
#    print("m_temp",int(m_temp))

 #   while(Decimal(int(m_temp))!=m_temp):
#        k=k+1
#        print("k: m_temp")
#        m_temp = Decimal(N*k + x)**Decimal(1.0/3.0)

    # your code ends here
    
    # convert the int to message string
    m=int(m_temp)
    msg = hex(m).rstrip('L')[2:].decode('hex')
    return msg

def main():
    if len(sys.argv) != 2:
        usage()

    all_keys = None
    with open('keys4student.json', 'r') as f:
        all_keys = json.load(f)

    name = hashlib.sha224(sys.argv[1].strip()).hexdigest()
    if name not in all_keys:
        print sys.argv[1], "not in keylist"
        usage()

    data = all_keys[name]
    N1 = int(data['N0'], 16)
    N2 = int(data['N1'], 16)
    N3 = int(data['N2'], 16)
    C1 = int(data['C0'], 16)
    C2 = int(data['C1'], 16)
    C3 = int(data['C2'], 16)
    
    msg = recover_msg(N1, N2, N3, C1, C2, C3)
    print msg
    
if __name__ == "__main__":
    main()
