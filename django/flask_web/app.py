from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data', methods=['POST'])
def perform_task():
    message = "성공적으로 파이썬 함수 호출!!"
    result = jsonify(result=message)
    return result

@app.route('/get_square_data', methods=['POST'])
def perform_task2():
    data = request.get_json()  # JSON 데이터를 가져옵니다
    square_value = data.get('square_value', 0)  # 'square_value' 값을 가져옵니다
    result_value = square_value ** 2  # 제곱 계산
    result = jsonify(result=result_value)  # 결과 반환
    return result

if __name__ == '__main__':
    app.run(debug=True)