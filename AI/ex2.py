import numpy as np
#from random import random
import time

# x_data = np.array([173., 171., 162., 187., 157., 169., 177., 159., 182.])     # train_set
# y_data = np.array([270., 275., 245., 280., 230., 265., 270., 250., 275.])
x_data = np.array([1., 2., 3.])
y_data = np.array([2., 4., 6.])

W = 1.0#random()
b = 0.0#random()

n_data = len(x_data)

epochs = 417       # 반복횟수  # (0.0,0.0) = 433
learning_rate = 17/99

start = time.time()

for i in range(epochs):
    hypothesis = x_data * W + b
    cost = np.sum((hypothesis-y_data)**2) / n_data      # 평균제곱
    gradient_W = np.sum((W*x_data - y_data + b)*2*x_data) / n_data
    gradient_b = np.sum((W*x_data - y_data + b)*2) / n_data

    W -= learning_rate * gradient_W
    b -= learning_rate * gradient_b

    if i%100==0 :
        print('Epoch ({:10d}/{:10d}) cost: {:10f}. W: {:10f}. b:{:10}'.format(
            i, epochs, cost, W, b))

print('W: {:10}'.format(W))
print('b: {:10}'.format(b))
print('result:', x_data*W+b)        # 예측

print (time.time()-start)