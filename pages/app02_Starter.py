import streamlit as st
import time
import numpy as np
from PIL import Image

# 커스텀 함수 가져오기
import sys
sys.path.append('../myLib/')
                
import test as func

# main()
if st.button('버튼클릭') :
        func.test_c()


st.markdown("# Plotting Demo")
st.sidebar.header("Plotting Demo")

st.title('딥러닝 스타터')
st.text('1. 준비하기')
st.code('''
        import matplotlib.pyplot as plt
        ''',
        language='python')

st.text('2. 데이터셋준비하기')
st.code('''
        X = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        Y = [1, 1, 2, 4, 5, 7, 8, 9, 9, 10]

        plt.scatter(X, Y)
        plt.show()
        ''',
        language='python')

st.text('3. 모델생성하기')
st.code('''
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
        ''',
        language='python')

st.text('4. 실험하기')
st.code('''
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
        ''',
        language='python')


img = Image.open('img/test01.png')
st.image(img)