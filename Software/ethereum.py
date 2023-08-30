from blockchain import *

class Ethereum(Blockchain):

    def __init__(self):
        super().__init__()
        self.wallet_address_dictionary = dictionary_from_csv(f'{Blockchain.pub_wallets_filepath}ETH/pub_wallets.csv')
        self.blockchain_explorer_url = f"{Blockchain.explorer_dictionary.get('eth')}"
        self.eth_transactions_filepath = f'{Blockchain.blockchain_transactions_filepath}ETH/'


    def download_eth_transactions(self):
        for item in self.wallet_address_dictionary:
            self.dl_tx_report_link(f'{self.blockchain_explorer_url}{self.wallet_address_dictionary.get(item)}', f'{self.eth_transactions_filepath}ETH{self.wallet_address_dictionary.get(item)}')

        return f'Your default browser has been loaded with links to Etherscan.io for your wallet addresses. Set the date range on the webpage for the tax year you wish to download, complete the robot tests, and dl your files to {self.eth_transactions_filepath}ETH0xAddress.csv where you replace 0xAddress with the public address of your wallet.'


