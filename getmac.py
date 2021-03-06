import platform
import netifaces as nif

def getmacs(active=True):
    macs=[]
    for i in nif.interfaces():
        if platform.system()=="Darwin" and i.startswith("awdl"): continue

        addrs=nif.ifaddresses(i)
        af_link=addrs.get(nif.AF_LINK)
        af_inet=addrs.get(nif.AF_INET)
        af_inet6=addrs.get(nif.AF_INET6)

        if not af_link: continue
        if active and not (af_inet or af_inet6): continue
        if af_inet and af_inet[0]['addr']=="127.0.0.1": continue
        if af_inet6 and af_inet6[0]['addr']=="::1": continue

        addr=af_link[0]['addr']
        if platform.system()=="Windows" and addr=="00:00:00:00:00:00:00:e0": continue

        macs.append(addr)
    return macs

def mac2Serial(mac):
    sum=0
    for i,c in enumerate(mac):
        if c.isdigit(): sum+=sum+int(c)*(2*i)
        elif c.isalpha(): sum+=sum+ord(c)*(2*i)
    return sum

def generateKey(serial):
    return int(serial*serial+53/serial+113*(serial/4))

def checkKey(serial,key):
    return key==generateKey(serial)

if __name__=="__main__":
    print("Active Interfaces:")
    print("==================")
    print(getmacs())
    print()
    print("All Interfaces:")
    print("===============")
    print(getmacs(False))
    print()
    print("Serial:")
    print("=======")
    serial=mac2Serial(getmacs()[0])
    print(serial)
    print()
    print("Key:")
    print("====")
    key=generateKey(serial)
    print(key)
    print()
    print("Activate:")
    print("=========")
    print(checkKey(serial, key))
    print()