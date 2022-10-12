import os
import web3
from brownie import MRCRYPTO, accounts, network
from dotenv import load_dotenv

load_dotenv()


PRICE_VARIABLE_NAME = 'MINT_PRICE'


def get_account(i):
    if network.show_active() == 'development':
        return accounts[i]
    else:
        return accounts.add(os.getenv(f'DEV0{i}_PRIVATE_KEY'))


def main():
    dev = get_account(0)
    user = get_account(1)

    contract = MRCRYPTO.deploy(
        "name",
        "symbol",
        "initBaseURI",
        "initNotRevealedUri",
        {"from": dev}
    )

    price = getattr(contract, PRICE_VARIABLE_NAME)()

    amount = 10
    value = amount * price
    contract.mint(amount, {
        "from": user,
        'value': value,
        'maxFeePerGas': web3.Web3.toWei(50, 'gwei'),
        'maxPriorityFeePerGas': web3.Web3.toWei(5, 'gwei'),
    })

    print(f"Balance of user: {contract.balanceOf(user)}")
    assert contract.balanceOf(user) == amount
