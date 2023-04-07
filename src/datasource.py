import random

def dataSource():
    h=random.randint(20,100)
    t=random.randint(20,40)
    rainfall=random.randint(100,300)
    moisture=random.randint(20,100)
    ph=random.randint(5,7)
    k='{"H": '+str(h)+',"T": '+str(t)+',"R": '+str(rainfall)+',"M": '+str(moisture)+',"pH": '+str(ph)+'}'
    print(k)
    return (k)