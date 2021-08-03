from pop import xnode

while True:
    try:
        for device in xnode.discover():
            print("NI : ", device['node_id'], ", rssi : ", device['rssi']")# ", ", DB : ",xnode.atcmd('DB'))
    except:
        pass