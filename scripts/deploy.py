from unittest import mock
from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS



def deploy_fund_me():
    account = get_account()

    # pass the price feed address to our fundme contract
    # if we are on a persisent network like rinkeby, use the associated address
    #  else deploy mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
        

    fundme = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fundme.address}")
    return fundme


def main():
    deploy_fund_me()
