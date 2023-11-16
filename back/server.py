from flask import Flask, request
from flask_cors import CORS
from main import keyword_based_abstract, machine_learning_abstract

from document import Document

app = Flask(__name__)
CORS(app)


@app.route('/kwabstract', methods=['POST'])
def kwabstract():
    return keyword_based_abstract(Document('', request.json["text"]))


@app.route('/mlabstract', methods=['POST'])
def mlabstract():
    return machine_learning_abstract(Document('', request.json["text"]))


if __name__ == '__main__':
    app.run()
