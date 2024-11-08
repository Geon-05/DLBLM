from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/DOSOMETHING', methods=['POST'])
def perform_task():
    result = "Task completed successfully!"
    return jsonify(result=result)

if __name__ == '__main__':
    app.run(debug=True)