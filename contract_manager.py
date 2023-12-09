import web3
from web3 import Web3
from solcx import compile_standard, install_solc
import os

import json
class Contract_Manager:

    _chain_id = 1337

    _lottery_contract = None

    compiled_sol = None

    _bytecode = None
    _abi = None

    _w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))

    _owner_address = "0x9Ab6658D147dDAe41e44DebDdf74a5316579E7DE"
    _owner_private_key = "0x0bd2be5dc90f74adbcc73dd0c1d0fe4ccb010e1f08e59f82f3e37714f3614d19"

    _instance = None

    def __new__(cls, compiled_sol):
        if cls._instance is None:
            cls._instance = super(Contract_Manager, cls).__new__(cls)
            cls._instance.compiled_sol = compiled_sol
            cls._instance.init()
        return cls._instance

    def getPlayers(self):
        client_address = "0xCD2267e5E64A3c22901Bb1fBf4D1545Fb19fe072"
        client_private_key = "0x9efb2793d5842e9d1cca0cb2e3a5f802110451ae132d5a650c2effe104799289"
        #
        nonce = self._w3.eth.get_transaction_count(client_address)

        contract = self._w3.eth.contract(address=self._owner_address, abi=self._abi)

        amount_in_wei = self._w3.to_wei(0.0000001, 'ether')
        transaction = contract.functions.getPlayers().build_transaction(
            {
                'from': client_address,
                'value': amount_in_wei,
                'gasPrice': self._w3.eth.gas_price,
                'nonce': nonce,
            }
        )

        signed_txn = self._w3.eth.account.sign_transaction(transaction, private_key=client_private_key)
        tx_hash = self._w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        tx_receipt = self._w3.eth.wait_for_transaction_receipt(tx_hash)

        print(tx_receipt)

    def init(self):
        with open("compiled_code.json", "w") as file:
            json.dump(self.compiled_sol, file)

        # get bytecode
        self._bytecode = self.compiled_sol["contracts"]["MyLottery.sol"]["MyLottery"]["evm"]["bytecode"]["object"]

        #  get abi
        self._abi = self.compiled_sol["contracts"]["MyLottery.sol"]["MyLottery"]["abi"]

        self._lottery_contract = self._w3.eth.contract(abi=self._abi, bytecode=self._bytecode)

        nonce = self._w3.eth.get_transaction_count(self._owner_address)

        transaction = self._lottery_contract.constructor().build_transaction({
            "chainId": self._chain_id,
            "gasPrice": self._w3.eth.gas_price,
            "from": self._owner_address,
            "nonce": nonce,
        })

        signed_txn = self._w3.eth.account.sign_transaction(
            transaction,
            private_key=self._owner_private_key
        )

        print("Deploying Contract!")

    def perform(self):
        client_address = "0xCD2267e5E64A3c22901Bb1fBf4D1545Fb19fe072"
        client_private_key = "0x9efb2793d5842e9d1cca0cb2e3a5f802110451ae132d5a650c2effe104799289"
        #
        nonce = self._w3.eth.get_transaction_count(client_address)

        contract = self._w3.eth.contract(address=client_address, abi=self._abi)

        amount_in_wei = self._w3.to_wei(0.01, 'ether')
        transaction = contract.functions.enter().build_transaction(
            {
                'from': client_address,
                'value': amount_in_wei,
                'gasPrice': self._w3.eth.gas_price,
                'nonce': nonce,
            }
        )

        signed_txn = self._w3.eth.account.sign_transaction(transaction, private_key=client_private_key)
        tx_hash = self._w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        tx_receipt = self._w3.eth.wait_for_transaction_receipt(tx_hash)

        print(tx_receipt)

        return True