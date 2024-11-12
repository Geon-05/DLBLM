import os, sys
from flask import Flask, render_template, jsonify, request, Response
import webbrowser
from threading import Timer
import neural_style_transfer

app = Flask(__name__)

def root_path():
	'''root 경로 유지'''
	real_path = os.path.dirname(os.path.realpath(__file__))
	sub_path = "\\".join(real_path.split("\\")[:-1])
	return os.chdir(sub_path)


@app.route('/')
def index():
    return render_template('index.html')

''' ConvNet info page '''
@app.route('/convnet_info')
def convnet_info():
	return render_template('convnet_info.html')

@app.route('/get_data', methods=['POST'])
def perform_task():
    result = "Task completed successfully!"
    return jsonify(result=result)


@app.route('/predict_sentiment', methods=['POST'])
def predict_sentiment():
    # result = "감성분석 함수 호출 준비 완료!!!"  
    data = request.get_json()  # JSON 형식으로 데이터 수신
    user_input = data['key']  # 유저 인풋 가져오기
    
    result = predict(user_input)
    label = get_label(user_input)    
    
    return jsonify(result=result, label=label)


import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline

tokenizer = AutoTokenizer.from_pretrained('skt/kogpt2-base-v2')
num_labels = 3
model = AutoModelForSequenceClassification.from_pretrained("skt/kogpt2-base-v2", num_labels=num_labels)
device = torch.device("cpu")
model.load_state_dict(torch.load("감성분석_model_checkpoint.pt", map_location=device))
pipe = pipeline("text-classification", model=model, tokenizer=tokenizer, device=device, max_length=512, return_all_scores=True, function_to_apply='softmax')
label_dict = {'LABEL_0' : '중립', 'LABEL_1' : '긍정', 'LABEL_2' : '부정'}

def get_label(text):
	result = pipe(text)
	top_label = max(result[0], key=lambda x:x['score'])['label']
 
	return label_dict[top_label]
		
def predict(user_input):	
    result = pipe(user_input)    
    return result    


''' Neural Style Transfer '''
@app.route('/nst_get')
def nst_get():
	return render_template('nst_get.html')

@app.route('/nst_post', methods=['GET','POST'])
def nst_post():
	if request.method == 'POST':
		root_path()
  
		print('request.form:', request.form)  # form 데이터 출력하여 확인

		# Reference Image
		refer_img = request.form['refer_img']
		refer_img_path = '/images/'+str(refer_img)

		# User Image (target image)
		user_img = request.files['user_img']
		image_directory  = '.\\static\\images'
  
  		# 이미지 저장 경로 생성
		image_directory = os.path.join(os.getcwd(), 'static', 'images')
		os.makedirs(image_directory, exist_ok=True)  # 디렉토리가 없으면 생성
  
		# user_img.save('./static/images/'+str(user_img.filename))
		user_img.save(os.path.join(image_directory, str(user_img.filename)))
		
		user_img_path = '/images/'+str(user_img.filename)

		# Neural Style Transfer 
		transfer_img = neural_style_transfer.main(refer_img_path, user_img_path)
		# transfer_img_path = '/images/'+str(transfer_img.split('/')[-1])
		transfer_img_path = '/images/'+str(transfer_img.split('\\')[-1])

		# transfer_img_path = os.path.join(os.getcwd(), f"static\\images\\{str(transfer_img.split('/')[-1])}") 
  
	return render_template('nst_post.html', 
					refer_img=refer_img_path, user_img=user_img_path, transfer_img=transfer_img_path)


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")


if __name__ == '__main__':
    Timer(1, open_browser).start()  # 서버 시작 후 1초 뒤에 브라우저 열기    
    app.run(debug=True, use_reloader=False)
