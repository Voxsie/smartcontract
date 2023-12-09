from flask import Flask, render_template
import requests
import json
from solcx import compile_standard, install_solc
from contract_manager import Contract_Manager
import time

manager = None
def init_contract():
    with open("MyLottery.sol", "r") as file:
        smart_contract_demo_file = file.read()

    install_solc("0.6.0")

    # Solidity source code
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"MyLottery.sol": {"content": smart_contract_demo_file}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                    }
                }
            }
        },
        solc_version="0.6.0",
    )

    return compiled_sol


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def perform():
    manager.perform()

    data = {"result": True}
    json_data = json.dumps(data)

    time.sleep(5)

    # manager.getPlayers()
    return json_data

@app.route('/players', methods=['GET', 'POST'])
def getPlayer():
    manager.perform()

    players = manager.getPlayers()
    data = {"result": players}
    json_data = json.dumps(data)

    return json_data


@app.route('/instagram', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


if __name__ == '__main__':
    code = init_contract()
    manager = Contract_Manager(compiled_sol=code)
    app.run()

