from flask import Flask, render_template, jsonify
import webbrowser
from threading import Timer

app = Flask(__name__)

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

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == '__main__':
    Timer(1, open_browser).start()  # 서버 시작 후 1초 뒤에 브라우저 열기    
    app.run(debug=True, use_reloader=False)
