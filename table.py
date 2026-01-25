import random
def returning():
    a=random.random()*16
    a=int(a)
    a=hex(a)
    a=a[2:]
    return a
print( "\n\033c\033[40;37m\ngive the x value of the table ? ")
#x=input()
print( "\n\033[40;37m\ngive the y value of the table ? ")
#y=input()
x=10
y=10
for yy in range(y):
    print()
    for xx in range(x):
        print(returning(),end="")
print( "\n")