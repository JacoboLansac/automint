import web3.eth
from brownie import network, accounts, config, Contract, chain
from web3 import Web3
import time
import json
import os


def main():

    # ===================================================================================
    timestamp = 1641932161
    # ===================================================================================

    print(f"timestamp: {timestamp}")
    print(f"Network: {network.show_active()}")

    while True:
        print(f"timestamp: {chain[-1].timestamp}")
        if chain[-1].timestamp > timestamp:
            print(f"Taking action")
        time.sleep(1)


    # account = accounts.add(os.getenv("BURNACCOUNT1_PRIVATE_KEY"))
    account = accounts.add(os.getenv("DEV_PRIVATE_KEY"))
    print(f"balance={Web3.fromWei(account.balance(), 'ether')} ether")

    if account.balance() == 0:
        raise ValueError("Balance is zero!!!")

    contract = Contract.from_abi(
        'AOmetaverse',
        '0x...',
        json.loads(
            '[{...}]'
        )
    )

    print(f"price()={contract.price()}")
    print(f"Trying to mint (should fail as they are sold out)")
    amount = 1
    payable = 70000000000000000
    tx = contract.mint(amount, {"from": account, "value": payable})
    tx.wait()


