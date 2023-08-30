import csv
import webbrowser
import requests
import pathlib

from common_functions import dictionary_from_csv
from api_data import CoinGecko


class Blockchain():
    other_information_filepath = '../CSV/OtherInformation/'
    pub_wallets_filepath = '../CSV/PubWallets/'
    blockchain_transactions_filepath = '../CSV/BlockchainTxReports/'
    mining_income_filepath = '../CSV/MiningIncome/'
    cost_basis_filepath = '../CSV/CostBasis/'
    explorer_dictionary = dictionary_from_csv(f'{other_information_filepath}/blockchain_explorers.csv')
    mining_address_dictionary = dictionary_from_csv(f'{other_information_filepath}/mining_pool_addresses.csv')
    tx_hash_explorers = dictionary_from_csv(f'{other_information_filepath}tx_hash_explorers.csv')
    
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








       




