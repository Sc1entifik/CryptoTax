import csv
import webbrowser
import requests
import pathlib
from datetime import datetime as dt
from selenium import webdriver


#Needed to create dictionaries where there are key value pairs for multiple blockchains
def dictionary_from_csv(csv_file, key_description = 'key', value_description = 'value'):
    with open(csv_file, 'r') as csv_to_dict:
        data_object = csv.reader(csv_to_dict)
        header_list = next(data_object)
        key_index = header_list.index(key_description)
        value_index = header_list.index(value_description)
        data_dictionary = {row[key_index]: row[value_index] for row in data_object}

    return data_dictionary 
        

class Blockchain():
    other_information_filepath = '../CSV/OtherInformation/'
    pub_wallets_filepath = '../CSV/PubWallets/'
    blockchain_transactions_filepath = '../CSV/BlockchainTxReports/'
    explorer_dictionary = dictionary_from_csv(f'{other_information_filepath}/blockchain_explorers.csv')
    
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





dfk = DefiKingdoms()
print(dfk.create_8949_from_transactions_csv())
