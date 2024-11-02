def test_c():
    print('테스트'*50)

def test_s():
    import streamlit as st
    st.title('딥러닝 스타터')
    st.text('1. 준비하기')


def test_f():

    import matplotlib.pyplot as plt

    X = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    Y = [1, 1, 2, 4, 5, 7, 8, 9, 9, 10]

    plt.scatter(X, Y)
    plt.show()

    class H():
        def __init__(self, w): 
            self.w = w
        
        def forward(self, x):
            return self.w * x

    # W = 4인 모델 생성
    h = H(4)

    # h라는 모델은 5라는 예상값을 넣었을때 20이라는 예측값을 내놓을 것이다.
    pred_y = h.forward(5)

    print('value of w :', h.w)
    print('value of f(5) :', pred_y)

    def cost(h, X, Y):
        error = 0
        for i in range(len(X)):
            error += (h.forward(X[i]) - Y[i])**2
        error = error / len(X)
        return error

    h = H(4)
    print('cost value when w = 4 :', cost(h, X, Y))

    def better_cost(pred_y, true_y):
        error = 0
        for i in range(len(X)):
            error += (pred_y[i] - true_y[i])**2
        error = error / len(X)
        return error

    pred_y = [ h.forward(X[i]) for i in range(len(X)) ]
    print('cost value with better code structure :', better_cost(pred_y, Y))

    # 실험1
    list_w = []
    list_c = []
    for i in range(-100, 100):
        w = i * 0.05
        h = H(w)
        c = cost(h, X, Y)
        list_w.append(w)
        list_c.append(c)
        
    print(list_w)
    print(list_c)

    plt.figure(figsize=(10,5))
    plt.xlabel('w')
    plt.ylabel('cost')
    plt.scatter(list_w, list_c, s=3)

    # 실험2
    list_w = []
    list_c = []
    for i in range(-20, 20):
        w = i * 0.5
        h = H(w)
        c = cost(h, X, Y)
        list_w.append(w)
        list_c.append(c)
        
    print(list_w)
    print(list_c)

    plt.figure(figsize=(10,5))
    plt.xlabel('w')
    plt.ylabel('cost')
    plt.scatter(list_w, list_c, s=3)

    def cal_grad(w, cost):
        h = H(w)
        cost1 = cost(h, X, Y)
        eps = 0.00001 
        h = H(w+eps)
        cost2 = cost(h, X, Y)
        dcost = cost2 - cost1
        dw = eps
        grad = dcost / dw
        return grad, (cost1+cost2)*0.5

    def cal_grad2(w, cost):
        h = H(w)
        grad = 0
        for i in range(len(X)):
            grad += 2 * (h.forward(X[i]) - Y[i]) * X[i]
        grad = grad / len(X)
        c = cost(h, X, Y)
        return grad, c

    w1 = 1.4
    w2 = 1.4
    lr = 0.01

    list_w1 = []
    list_c1 = []
    list_w2 = []
    list_c2 = []

    for i in range(100):
        grad, mean_cost = cal_grad(w1, cost)
        grad2, mean_cost2 = cal_grad2(w2, cost)

        w1 -= lr * grad
        w2 -= lr * grad2
        list_w1.append(w1)
        list_w2.append(w2)
        list_c1.append(mean_cost)
        list_c2.append(mean_cost2)
        
    print(w1, mean_cost, w2, mean_cost2)

    plt.scatter(list_w1, list_c1, label='analytic', marker='*')
    plt.scatter(list_w2, list_c2, label='formula')

    w1 = 1.4
    w2 = 1.1
    lr = 0.01

    list_w1 = []
    list_c1 = []
    list_w2 = []
    list_c2 = []

    for i in range(100):
        grad, mean_cost = cal_grad2(w1, cost)
        grad2, mean_cost2 = cal_grad2(w2, cost)

        w1 -= lr * grad
        w2 -= lr * grad2
        list_w1.append(w1)
        list_w2.append(w2)
        list_c1.append(mean_cost)
        list_c2.append(mean_cost2)
        
    print(w1, mean_cost, w2, mean_cost2)

    plt.scatter(list_w1, list_c1, label='start from w=1.4', marker='*')
    plt.scatter(list_w2, list_c2, label='start from w=1.1')
    plt.legend()