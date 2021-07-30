from pop.AI import Linear_Regression

lr = Linear_Regression()

lr.X_data = [[173], [171], [162], [187], [157], [169], [177], [159], [182]]
lr.Y_data = [[270], [275], [245], [280], [230], [265], [270], [250], [275]]

lr.train(times=5000)

print(lr.run([[172]]))