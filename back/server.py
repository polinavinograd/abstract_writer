from flask import Flask, request, jsonify
from flask_cors import CORS
from document import Document

app = Flask(__name__)
CORS(app)

@app.route('/create_abstract', methods=['POST'])
def create_abstract():
    pass


if __name__ == '__main__':
    app.run()
