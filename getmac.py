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

        macs.append(af_link[0]['addr'])
    return macs

if __name__=="__main__":
    print("Active Interfaces:")
    print("==================")
    print(getmacs())
    print()
    print("All Interfaces:")
    print("===============")
    print(getmacs(False))