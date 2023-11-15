from flask import Flask, request
from flask_cors import CORS
from main import create_abstract

app = Flask(__name__)
CORS(app)

@app.route('/kwabstract', methods=['POST'])
def kwabstract():
    return create_abstract(request.json["text"])

@app.route('/mlabstract', methods=['POST'])
def mlabstract():
    return create_abstract(request.json["text"])

if __name__ == '__main__':
    app.run()
