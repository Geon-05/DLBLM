from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data', methods=['POST'])
def perform_task():
    message = "성공적으로 파이썬 함수 호출!!"
    result = jsonify(result=message)
    return result

if __name__ == '__main__':
    app.run(debug=True)