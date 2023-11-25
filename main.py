from flask import Flask, render_template
import requests
import json
from contract_manager import Contract_Manager

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def perform():
    manager = Contract_Manager()

    result = manager.perform()

    data = {"result": result}
    json_data = json.dumps(data)
    return json_data

@app.route('/instagram', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()


    url = 'http://127.0.0.1:5000'
    app.logger.warning("123")
    print("123")
    print('Hi', flush=True)
    r = requests.get(url)
    json = r.json()

    print(r.status_code)
    print(json)
