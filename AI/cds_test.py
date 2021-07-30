from pop.AI import Linear_Regression
from pop import Cds, delay

cds = Cds(7)        # 7번에 연결되어있음

value = cds.readAverage()
#print(value)


lr = Linear_Regression()

print(lr.run([value]))