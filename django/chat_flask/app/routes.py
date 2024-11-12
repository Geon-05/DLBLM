from flask import Blueprint, render_template, send_from_directory, current_app, jsonify, request
from langchain.schema import Document
from app.emotion import emotion_chk
from app.chat import subject_chk


main = Blueprint('main', __name__)

# ico위치 명시
@main.route('/favicon.ico')
def favicon():
    return send_from_directory(current_app.static_folder, 'favicon.ico')

# index 앱으로 이동
@main.route('/')
def index():
    return render_template('index.html')

# chat봇 앱으로 이동
@main.route('/chat')
def chat():
    return render_template('chat.html')

# emotion 앱으로 이동
@main.route('/emotion')
def emotion():
    return render_template('emotion.html')


@main.route('/post_sentence', methods=['POST'])
def post_sentence():
    data = request.get_json()
    sentence = data.get('sentence', '')
    emotion_result = emotion_chk(sentence)
    return jsonify(emotion_result=emotion_result)

@main.route('/get_subject', methods=['GET'])
def get_subject():
    gametitle = request.args.get('gameTitle', '')
    
    if not gametitle:
        return jsonify({"error": "Game title parameter is missing"}), 400

    try:
        # subject_chk 함수 호출 및 결과 저장
        subject_results = subject_chk(gametitle)
        
        # 모든 Document 객체를 JSON 직렬화 가능한 딕셔너리로 변환
        result_list = []
        for doc in subject_results:
            if isinstance(doc, Document):
                result_list.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata
                })
        
        return jsonify(subject_result=result_list, gametitle=gametitle)
    except Exception as e:
        print(f"서버 오류: {e}")
        return jsonify({"error": "Internal Server Error"}), 500