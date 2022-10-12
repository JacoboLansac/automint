import time
from brownie import network, accounts, config, Contract, MRCRYPTO
import json
import os
import web3
import dotenv
dotenv.load_dotenv()

# =============================== CONFIGURAITON =====================================
# ===================================================================================
NFTname = 'Renga Ape Yatch Club'  # This is irrelevant
contractAddress = ''
contractABI = '[{"inputs": ... paste abi here ...:"function"}]'
# ===================================================================================
MAX_TRANSACTIONS = 3
amount_per_tx = 10
maxFeePerGas = 50
maxPriorityFeePerGas = 10
PRICE_VARIABLE_NAME = 'publicSalePrice'
openSaleBoolean = 'publicSaleOpen'
# ===================================================================================


def get_contract():


    if network.show_active() == 'mainnet':
        return Contract.from_abi(
            NFTname,
            contractAddress,
            json.loads(contractABI)
        )
    else:
        raise ValueError("Not in mainnet")



def get_minting_account() -> str:
    pkey = os.getenv(f'DEV00_PRIVATE_KEY')
    assert pkey is not None, "No private key"
    account = accounts.add(private_key=pkey)
    assert account.balance() > 0, "No ether in wallet"
    print(f"account balance: {account.balance()} eth")
    return account



def main():
    print(f"Network: {network.show_active()}")

    contract = get_contract()
    account = get_minting_account()
    MINT_PRICE = getattr(contract, PRICE_VARIABLE_NAME)()

    while True:
        try:
            isSaleOpen = getattr(contract, openSaleBoolean)()
            if isSaleOpen:
                print(f"[{round(time.time())}]: Public sale not open")
                time.sleep(1)
            else:
                print(f"Sale is open!")

                for tx in range(MAX_TRANSACTIONS):
                    print(f"Minting tx #{tx}")
                    value = amount_per_tx * MINT_PRICE
                    contract.mint(amount_per_tx, {
                        "from": account,
                        'value': value,
                        'maxFeePerGas': web3.Web3.toWei(maxFeePerGas, 'gwei'),
                        'maxPriorityFeePerGas': web3.Web3.toWei(maxPriorityFeePerGas, 'gwei'),
                    })

                break

        except Exception as e:
            print(e)

    print(f"DONE")
