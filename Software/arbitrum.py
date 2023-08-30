from datetime import datetime as dt
from selenium import webdriver
from selenium.webdriver.common.by import By

from blockchain import *

class Arbitrum(Blockchain):

    def __init__(self):
        super().__init__()
        self.arb_transactions_filepath = f'{Arbitrum.blockchain_transactions_filepath}ARB/'
        self.mining_income_filepath = f'{Arbitrum.mining_income_filepath}ARB/'
        self.cost_basis_filepath = f'{Arbitrum.cost_basis_filepath}ETH/ARB/cost_basis.csv'
        self.wallet_address_dictionary = dictionary_from_csv(f'{Arbitrum.pub_wallets_filepath}ETH/pub_wallets.csv')
        self.tx_hash_url = Arbitrum.tx_hash_explorers.get('arb') 
        

    def _transaction_data_from_selenium_scraper(scraped_data):

        def swap_data_from_transaction_elements(transaction_elements):
            swapped_from = transaction_elements[0].split()
            swapped_to = transaction_elements[1].split()

            return (swapped_from, swapped_to)
            

        def wrapper(self, tx_hash):
            swapped_from_data, swapped_to_data = swap_data_from_transaction_elements(scraped_data(self, tx_hash))
            swapped_from_volume_and_ticker = (swapped_from_data[0], swapped_from_data[-1])
            swapped_to_volume_and_ticker = (swapped_to_data[0], swapped_to_data[-1])

            return f'swapped_from_data: {swapped_from_data}\nswapped_to_data: {swapped_to_data}\nfrom_volume_and_ticker: {swapped_from_volume_and_ticker}\nswapped_to_volume_and_ticker: {swapped_to_volume_and_ticker}'
        
        return(wrapper)


    @_transaction_data_from_selenium_scraper
    def selenium_tx_scraper(self, tx_hash): 
        fire_fox_options = webdriver.FirefoxOptions()
        fire_fox_options.add_argument("--headless")
        driver = webdriver.Firefox(options = fire_fox_options)
        driver.get(f'{self.tx_hash_url}{tx_hash}')
        transactions = [element.text for element in driver.find_elements(By.TAG_NAME, 'ul') if element.text.find('From Null:') != -1][0].split('\n')
        search_term_index_buffer = 3
        elements = [element[element.find('For') + search_term_index_buffer:] for element in transactions if element.find('From Null') == -1]
        driver.close()
        
        return elements


    def download_arb_transactions(self):
        
        for wallet in self.wallet_address_dictionary.values():
            download_url = f'{Arbitrum.explorer_dictionary.get("arb")}{wallet}'
            self.dl_tx_report_link(download_url, self.arb_transactions_filepath)
            print(f'Your default webbrowser has been loaded to {download_url}. Complete the robot tests there and then save your transactions file to {self.arb_transactions_filepath}arb{wallet}.csv.\n\n')
        
        return 'Make sure to follow the above directions for all your Arbitrum chain wallet addresses.' 


    def create_mining_income_reports(self):
        filepath_list = [item for item in pathlib.Path(self.arb_transactions_filepath).iterdir() if item.is_file()]
        
        for file in filepath_list:
            with open(file, 'r') as transactions_csv:
                mining_deposit_object = csv.reader(transactions_csv)
                header_list = next(mining_deposit_object)
                header_index = {header: header_list.index(header) for header in header_list}
                mining_header_list = ['mining_pool_address', 'datetime', 'historical_price', 'eth_deposited', 'value_deposited', 'transaction_fee', 'cost_basis']
                mining_income = []

                for row in mining_deposit_object:
                    if row[header_index.get('From')] in self.mining_address_dictionary.values():
                        mining_pool_address = row[header_index.get('From')]
                        date = row[header_index.get('DateTime')]
                        historical_price = row[header_index.get('Historical $Price/ETH')]
                        eth_deposited = row[header_index.get('Value_IN(ETH)')]
                        value_deposited = float(historical_price) * float(eth_deposited)
                        transaction_fee = row[header_index.get('TxnFee(USD)')]
                        cost_basis = value_deposited - float(transaction_fee)
                        mining_income_list = [mining_pool_address, date, historical_price, eth_deposited, value_deposited, transaction_fee, cost_basis]
                        mining_income.append(mining_income_list)

                with open(f'{self.mining_income_filepath}{file.stem}.csv', 'w') as mining_income_csv:
                    mining_pool_object = csv.writer(mining_income_csv)
                    mining_pool_object.writerow(mining_header_list)
                    mining_pool_object.writerows(mining_income)
                
        return f'Mining income reports created in {Arbitrum.mining_income_filepath}!'


    def add_mining_income_to_cost_basis(self):
        filepath_list = [item for item in pathlib.Path(self.mining_income_filepath).iterdir() if item.is_file()]

        for file in filepath_list:
            with open(file, 'r') as mining_income:
                mining_income_object = csv.reader(mining_income)
                mining_income_header = next(mining_income_object)
                header_index = {header: mining_income_header.index(header) for header in mining_income_header}
                mining_income_cost_basis = [[row[header_index.get('datetime')], row[header_index.get('historical_price')], row[header_index.get('eth_deposited')], row[header_index.get('cost_basis')]] for row in mining_income_object]

            with open(self.cost_basis_filepath, 'r') as cost_basis:
                cost_basis_object = csv.reader(cost_basis)
                cost_basis_header = next(cost_basis_object)
                current_cost_basis = [row for row in cost_basis_object] + mining_income_cost_basis
                current_cost_basis.sort(key = lambda row: dt.strptime(row[cost_basis_header.index('datetime')], '%Y-%m-%d %H:%M:%S'))

            with open(self.cost_basis_filepath, 'w') as cost_basis:
                cost_basis_object = csv.writer(cost_basis)
                cost_basis_object.writerow(cost_basis_header)
                cost_basis_object.writerows(current_cost_basis)

            return f'Mining Income cost basis added to {self.cost_basis_filepath}'


    
arb = Arbitrum()
#print(arb.download_arb_transactions())
#print(arb.create_mining_income_reports())
#print(arb.tx_hash_url)
print(arb.selenium_tx_scraper('0x4c09ebd1f737b73f769a529f89e80144635d1993bc83352854609e488e92f41d'))
