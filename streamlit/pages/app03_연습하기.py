# 준비하기. import library

import streamlit as st
import torch
import torch.nn as nn
import torch.optim as optim
import re

# 1. 데이터셋만들기 / 불러오기
st.markdown("# Plotting Demo")
st.sidebar.header("Plotting Demo")

# 제목 및 설명
st.title('딥러닝 스타터')
st.text('1. 데이터셋 만들기 / 불러오기')
st.code('''
sentence = """
In the heart of a bustling city, where skyscrapers tower above and
people from all walks of life converge, there exists a small, unassuming
coffee shop that has become a beloved sanctuary for artists, writers, and
thinkers alike; a place where time seems to slow down, and the aroma of freshly
brewed coffee mingles with the gentle hum of conversation, inviting patrons
to linger a little longer, lost in thought or inspiration, while outside,
the world continues at its relentless pace, oblivious to the quiet magic brewing within.
"""

# 테스트 텍스트
"""
안녕하세요. 반갑습니다. 전처리가 확실하게 되었는지 확인해 볼까요?
"""

"""
도시의 번잡한 거리 한가운데, 높은 빌딩들이 하늘을 찌를 듯 솟아 있는 곳에
사람들의 발길이 끊이지 않는 작은 서점이 하나 있습니다. 이 서점은 독서와
휴식을 사랑하는 이들에게 편안한 안식처가 되어주며, 곳곳에 배치된 아늑한
의자와 잔잔한 음악은 방문자들로 하여금 조금 더 머물러 책장을 넘기게 만듭니다.
그렇게 서점 안에서는 시간이 멈춘 듯 고요한 평화가 흐르고 있지만, 문 밖 세상은
여전히 빠르게 돌아가고 있습니다.
"""
        ''',
        language='python')

# 데이터 입력
sentence_user = st.text_area('데이터를 입력하세요.')
sentence_user = re.sub("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "", sentence_user)
sentence_user = sentence_user.split()
st.text(f'전처리 후 테스트용 샘플의 개수 : {len(sentence_user)}')
st.text(sentence_user)

# 사전 생성
vocab = list(set(sentence_user))
word2index = {tkn: i for i, tkn in enumerate(vocab, 1)}
word2index['<unk>'] = 0

# 수치화된 데이터를 단어로 바꾸기 위한 사전
index2word = {v: k for k, v in word2index.items()}

# 데이터 변환
def build_data(sentence, word2index):
    encoded = [word2index.get(token, 0) for token in sentence]
    input_seq, label_seq = encoded[:-1], encoded[1:]
    input_seq = torch.LongTensor(input_seq).unsqueeze(0)
    label_seq = torch.LongTensor(label_seq).unsqueeze(0)
    return input_seq, label_seq

X, Y = build_data(sentence_user, word2index)

# 네트워크 클래스 정의
class Net(nn.Module):
    def __init__(self, vocab_size, input_size, hidden_size, batch_first=True):
        super(Net, self).__init__()
        self.embedding_layer = nn.Embedding(num_embeddings=vocab_size, embedding_dim=input_size)
        self.rnn_layer = nn.RNN(input_size, hidden_size, batch_first=batch_first)
        self.linear = nn.Linear(hidden_size, vocab_size)

    def forward(self, x):
        output = self.embedding_layer(x)
        output, hidden = self.rnn_layer(output)
        output = self.linear(output)
        return output.view(-1, output.size(2))

# 하이퍼 파라미터 설정
vocab_size = len(word2index)
input_size = st.text_input('input_size 입력', max_chars=5, placeholder='input_size')
hidden_size = st.text_input('hidden_size 입력', max_chars=5, placeholder='hidden_size')
input_size = int(input_size) if input_size else 10
hidden_size = int(hidden_size) if hidden_size else 20

# 모델 생성 및 학습 설정
if 'model' not in st.session_state:
    st.session_state.model = None

if st.button('입력'):
    st.text('모델을 생성합니다.')
    # 모델을 세션 상태에 저장하여 유지
    st.session_state.model = Net(vocab_size, input_size, hidden_size, batch_first=True)
    st.session_state.loss_function = nn.CrossEntropyLoss()
    st.session_state.optimizer = optim.Adam(params=st.session_state.model.parameters())
    st.success("모델이 생성되었습니다.")

# 예측 버튼 기능
if st.button('예측'):
    if st.session_state.model is not None:
        st.text('임의예측을 시행합니다.')
        output = st.session_state.model(X)
        st.write("예측 결과 텐서:", output[0])
        st.write("예측 결과 개수:", len(output))
        st.write("예측 결과 형태:", output.shape)
        # 수치화된 데이터를 단어로 전환하는 함수
        st.session_state.decode = lambda y: [index2word.get(x) for x in y]
        st.write(st.session_state.decode)
    else:
        st.warning("먼저 모델을 생성하세요.")

# 훈련 버튼 기능
if st.button('훈련'):
    if st.session_state.model is not None:
        # 훈련 시작
        st.text('머신러닝을 시행합니다.')
        for step in range(201):
            # 경사 초기화
            st.session_state.optimizer.zero_grad()
            # 순방향 전파
            output = st.session_state.model(X)
            # 손실값 계산
            loss = st.session_state.loss_function(output, Y.view(-1))
            # 역방향 전파
            loss.backward()
            # 매개변수 업데이트
            st.session_state.optimizer.step()
            # 기록
            if step % 40 == 0:
                st.write(f"[{step+1}/201] {loss} ")
                pred = output.softmax(-1).argmax(-1).tolist()
                st.write(" ".join(["Repeat"] + st.session_state.decode(pred)))
                st.write()
    else:
        st.warning("먼저 모델을 생성하세요.")