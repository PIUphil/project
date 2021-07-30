from pop.AI import Linear_Regression
from pop import Cds, delay

cds = Cds(7)        # 7번에 연결되어있음

x_cds = []
y_lx = []

for i in range(10):
    x_cds.append(cds.readAverage())
    y_lx.append(int(input('lux: ')))

lr = Linear_Regression()
lr.X_data = x_cds
lr.Y_data = y_lx

lr.train(times=10000)

print(y_lx)
print(lr.run())