import numpy as np

x_data = np.array([1., 2., 3.])     # train_set
y_data = np.array([2., 4., 6.])

W = .0
b = 0.0

n_data = len(x_data)

epochs = 1000       # 반복횟수
learning_rate = 0.1

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
print('result:', x_data*W+b)


'''
from pop.AI import Linear_Regression    # 선형회귀

lr = Linear_Regression()

lr.X_data = [[1],[2],[3]]      # 학습할 데이터(샘플)
lr.Y_data = [[2],[4],[6]]      # 목표값(정답지)

lr.train()  #  내부루트를 돌면서 w,b값을 초기화하고 x를 대입하고 y와 비교하여 오차 계산.. 반복
'''