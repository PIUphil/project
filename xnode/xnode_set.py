from pop import xnode

NI = "SBCood"
CE = 0x01           # 0x00 or 0x01
ID = 0x70

xnode.atcmd('NI', NI)
xnode.atcmd('CE', CE)
xnode.atcmd('ID', ID)

if CE == 0x00:
    xnode.atcmd('JV', 0x01)
    
xnode.atcmd('WR')   # eeprom - 전원이 꺼져도 지워지지 않음