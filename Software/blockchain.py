import csv
import webbrowser
import requests
import pathlib
from time import sleep
from datetime import datetime as dt
from selenium import webdriver
from common_functions import dictionary_from_csv
from api_data import CoinGecko


class Blockchain():
    other_information_filepath = '../CSV/OtherInformation/'
    pub_wallets_filepath = '../CSV/PubWallets/'
    blockchain_transactions_filepath = '../CSV/BlockchainTxReports/'
    explorer_dictionary = dictionary_from_csv(f'{other_information_filepath}/blockchain_explorers.csv')
    mining_address_dictionary = dictionary_from_csv(f'{other_information_filepath}/mining_pool_addresses.csv')
    mining_income_filepath = '../CSV/MiningIncome/'
    
    def __init__(self):
        pass


    def _get_list_from_csv_column(self, csv_file, column_name):

        with open(csv_file, 'r') as list_from_column_csv:
            data_object = csv.reader(list_from_column_csv)
            header_list = next(data_object)
            column_index = header_list.index(column_name)
            list_from_column = [row[column_index] for row in data_object]
        
        return list_from_column


    def _get_bridge_address_list(self):
        return _get_list_from_csv_column(f'{Blockchain.other_information_filepath}bridge_addresses.csv', 'value')


    def dl_tx_report(self, download_url, filepath_destination):

        with requests.Session() as tx_data:
            download = tx_data.get(download_url)
            decoded_tx_data = download.content.decode('utf-8')
            transaction_object = csv.reader(decoded_tx_data.splitlines(), delimiter = ',')
            transaction_header = next(transaction_object)


            with open(filepath_destination, 'w') as transaction_csv:
                writer = csv.writer(transaction_csv)
                writer.writerow(transaction_header)

                for row in transaction_object:
                    writer.writerow(row)

        return f'TX Report has been created in: {filepath_destination}'


    def dl_tx_report_link(self, download_url, filepath_destination):
        webbrowser.open(download_url)

        return f'The blockchain explorer has been loaded at {download_url} please finish the robot test to dl and set the destination directory for the download to {filepath_destination}'


    def _generate_8949c(self, filepath_destination, tax_data):

        #Date Acquired in MM/DD/YYYY format dt.strftime('%m-%d-%Y')
        with open(filepath_destination, 'w') as cap_gains_form:
            tax_form_object = csv.writer(cap_gains_form)
            header_list = ['Description Of Property', 'Date Acquired', 'Date Sold Or Disposed Of', 'Proceeds', 'Cost Or Other Basis', 'Code(s) From Instructions', 'Amount Of Adjustment', 'Gain Or Loss']
            tax_form_object.writerow(header_list)
            for data_row in tax_data:
                tax_form_object.writerow(data_row)
        return f'New 8949c tax form written in {filepath_destination}!'        


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


class DefiKingdoms(Blockchain):
    dfk_8949_filepath = '../CSV/8949c/'

    def __init__(self):
        super().__init__()
        self.wallet_address_dictionary = dictionary_from_csv(f'{DefiKingdoms.pub_wallets_filepath}ETH/pub_wallets.csv')
        self.blockchain_explorer_url = f"{DefiKingdoms.explorer_dictionary.get('dfk')}"
        self.dfk_transactions_filepath = f'{DefiKingdoms.blockchain_transactions_filepath}DFK/'


    def download_dfk_transactions(self):
        for item in self.wallet_address_dictionary:
            self.dl_tx_report_link(f'{self.blockchain_explorer_url}{self.wallet_address_dictionary.get(item)}', f'{self.dfk_transactions_filepath}DFK{self.wallet_address_dictionary.get(item)}')

        return f'Your default browser has been loaded with links to Lila\'s Ledger at dfkreport.cognifact.com. Choose your date range for the tax year you are downloading on the webpage, uncheck Harmony blockchain from included chains, then enter the 0xAddress in the Report Generation box then click Generate.' 


    def create_8949_from_transactions_csv(self):

        filepath_list = [item for item in pathlib.Path(self.dfk_transactions_filepath).iterdir() if item.is_file()]
        
        for path in filepath_list:
            
            with open(path, 'r') as tx_data_from_csv:
                tx_data_object = csv.reader(tx_data_from_csv)
                header_list = next(tx_data_object)
                header_index = {item: header_list.index(item) for item in header_list}
                cap_gains_check = lambda x: x[header_index.get('category')]  == 'gains'
                date_time_ternary = lambda x, column_name: '' if x[header_index.get(column_name)] == '' else dt.strptime(x[header_index.get(column_name)], '%Y-%m-%d').strftime('%m-%d-%Y')
                cap_gains_data = []

                for row in tx_data_object:
                    if cap_gains_check(row):
                        cap_gains_row = [
                                row[header_index.get('description')],
                                date_time_ternary(row, 'acquired date'),
                                date_time_ternary(row, 'sold date'),
                                float(row[header_index.get('proceeds')]),
                                float(row[header_index.get('costs')]),
                                '',
                                '',
                                float(row[header_index.get('gains')])
                                ]
                        cap_gains_data.append(cap_gains_row)
            
            self._generate_8949c(f'{DefiKingdoms.dfk_8949_filepath}{path.stem}.csv', cap_gains_data)
        return 'New 8949 form generated in {DefiKingdoms.dfk_8949_filepath}. Please check document for accuracy. Once accuracy check is complete, archive your records for safe keeping. Read instructions for a deep dive into the archival process. If you find mistakes or missing information fix those items in the Blockchain tx report that was used to generate this file, rerun this option and it will generate a new 8949 form overwriting the old file.' 


class ThorChain(Blockchain):

    def __init__(self):
        super().__init__()
        self.wallet_address_dictionary = dictionary_from_csv(f'{ThorChain.pub_wallets_filepath}THOR/pub_wallets.csv')
        self.blockchain_explorer_url = f"{ThorChain.explorer_dictionary.get('thor')}{self.wallet_address_dictionary.get('thor_keystore')}?network=mainnet"
        self.thor_transactions_filepath = f'{ThorChain.blockchain_transactions_filepath}THOR/{self.wallet_address_dictionary.get("thor_keystore")}.csv'


    def _datarows_list_from_tx_object(self, data_object):
        header_list = next(data_object)
        header_index = {header: header_list.index(header) for header in header_list}
        value_column_splitter = lambda row, header, split_index: row[header_index.get(header)].split()[split_index]
        #fees column needs to be split differently because of an annoying semicoln which is not always present butvery annoying
        fees_column_splitter = lambda indexed_row: indexed_row.split() if len(indexed_row.split()) != 4 else f'{indexed_row[:indexed_row.find(";")]}{indexed_row[indexed_row.find(";") + 1:]}'.split()
        currency_ticker = lambda string: string[string.find('.') + 1: string.find('-')] if string.find('-') != -1 else string[string.find('.') + 1:]
        fee_discovery_price = lambda ticker: '' if ticker == '' else (tx_discovery_price if ticker == tx_ticker else CoinGecko(ticker, dt.strptime(time.split()[0], '%d/%m/%Y')).return_historical_price())
        data_row_list = []
        
        for row in data_object:
            tx_hash = row[header_index.get('hash')]
            timestamp = row[header_index.get('timestamp')]
            time = row[header_index.get('time')]
            direction = row[header_index.get('direction')]
            tx_volume = float(value_column_splitter(row, 'value', 0))
            tx_ticker = currency_ticker(value_column_splitter(row, 'value', 1))
            tx_discovery_price = CoinGecko(tx_ticker, dt.strptime(time.split()[0], '%d/%m/%Y')).return_historical_price()
            tx_value = tx_volume * tx_discovery_price
            from_address = row[header_index.get('from')]
            to_address = row[header_index.get('to')]
            fees_split = fees_column_splitter(row[header_index.get('fees')])
            fee_1_volume = '' if len(fees_split) == 0 else float(fees_split[0])
            fee_1_ticker = '' if len(fees_split) == 0 else currency_ticker(fees_split[1])
            fee_1_discovery_price = fee_discovery_price(fee_1_ticker) 
            fee_1_value = '' if fee_1_discovery_price == '' else fee_1_discovery_price * fee_1_volume
            fee_2_volume = '' if len(fees_split) < 4 else float(fees_split[2])
            fee_2_ticker = '' if len(fees_split) < 4 else currency_ticker(fees_split[3])
            fee_2_discovery_price = fee_discovery_price(fee_2_ticker)
            fee_2_value = '' if fee_2_discovery_price == '' else fee_2_discovery_price * fee_2_volume
            tx_type = row[header_index.get('type')]
            row_list = [tx_hash, timestamp, time, direction, tx_type, tx_volume, tx_ticker, tx_discovery_price, tx_value,from_address, to_address, fee_1_volume, fee_1_ticker, fee_1_discovery_price, fee_1_value, fee_2_volume, fee_2_ticker, fee_2_discovery_price, fee_2_value]
            data_row_list.append(row_list)

        return data_row_list


    def download_thor_transactions(self):
        self.dl_tx_report_link(self.blockchain_explorer_url, self.thor_transactions_filepath) 

        return f'Your default webbrowser has been loaded to {self.blockchain_explorer_url}. Complete the robot tests there and then save your transactions file to {self.thor_transactions_filepath}.'


    def format_thor_transactions(self):
        
        with open(self.thor_transactions_filepath, 'r') as transactions:
            thor_transactions_object = csv.reader(transactions)
            data_row_list = self._datarows_list_from_tx_object(thor_transactions_object)
        
        new_header_list = ['tx_hash', 'timestamp', 'time', 'direction', 'tx_type','tx_volume', 'tx_ticker', 'coin_gecko_tx_discovery_price', 'tx_value_in_USD', 'from_address', 'to_address', 'fee_1_volume', 'fee_1_ticker', 'coin_gecko_fee_1_discovery_price', 'fee_1_value_in_USD', 'fee_2_volume', 'fee_2_ticker', 'coin_gecko_fee_2_discovery_price', 'fee_2_value_in_USD']

        with open(self.thor_transactions_filepath, 'w') as formatted_transactions:
            tx_data_object = csv.writer(formatted_transactions)
            tx_data_object.writerow(new_header_list)

            for row in data_row_list:
                tx_data_object.writerow(row)

        return f'{self.thor_transactions_filepath} has been modified!' 


class Arbitrum(Blockchain):

    def __init__(self):
        super().__init__()
        self.wallet_address_dictionary = dictionary_from_csv(f'{Arbitrum.pub_wallets_filepath}ETH/pub_wallets.csv')
        self.arb_transactions_filepath = f'{Arbitrum.blockchain_transactions_filepath}ARB/'
        self.mining_income_filepath = f'{Arbitrum.mining_income_filepath}ARB/'


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
                mining_header_list = ['mining_pool_address', 'datetime', 'historcal_price', 'eth_deposited', 'value_deposited', 'transaction_fee', 'cost_basis']
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


arb = Arbitrum()
#print(arb.download_arb_transactions())
print(arb.create_mining_income_reports())
