def num(n):
    nn=[]
    for n1 in range(n):
        nn=nn+[n1]
    return nn
def muls(m,j):
    nn=[]
    for n in m:
        mm=n*j
        nn=nn+[mm]
    return nn 
print("\x1bc\x1b[40;37m\nhello world...")
n=num(10)
print (n)
m=muls(n,2)
print(m)

