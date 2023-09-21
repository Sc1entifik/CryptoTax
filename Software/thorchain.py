from blockchain import *
from api_data import CoinGecko

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
        #fees column needs to be split differently because of an annoying semicoln which is not always present but very annoying
        fees_column_splitter = lambda indexed_row: indexed_row.split() if len(indexed_row.split()) != 4 else f'{indexed_row[:indexed_row.find(";")]}{indexed_row[indexed_row.find(";") + 1:]}'.split()
        currency_ticker = lambda string: string[string.find('.') + 1: string.find('-')] if string.find('-') != -1 else string[string.find('.') + 1:]
        fee_discovery_price = lambda ticker: '' if ticker == '' else (tx_discovery_price if ticker == tx_ticker else CoinGecko(ticker, dt.strptime(time, '%d/%m/%Y %H:%M:%S')).return_historic_price())
        data_row_list = []
        
        for row in data_object:
            tx_hash = row[header_index.get('hash')]
            timestamp = row[header_index.get('timestamp')]
            time = row[header_index.get('time')]
            direction = row[header_index.get('direction')]
            tx_volume = float(value_column_splitter(row, 'value', 0))
            tx_ticker = currency_ticker(value_column_splitter(row, 'value', 1))
            tx_discovery_price = CoinGecko(tx_ticker, dt.strptime(time, '%d/%m/%Y %H:%M:%S')).return_historic_price()
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
        
        new_header_list = ['tx_hash', 'timestamp', 'time', 'direction', 'tx_type', 'tx_volume', 'tx_ticker', 'coin_gecko_tx_discovery_price', 'tx_value_in_USD', 'from_address', 'to_address', 'fee_1_volume', 'fee_1_ticker', 'coin_gecko_fee_1_discovery_price', 'fee_1_value_in_USD', 'fee_2_volume', 'fee_2_ticker', 'coin_gecko_fee_2_discovery_price', 'fee_2_value_in_USD']

        with open(self.thor_transactions_filepath, 'w') as formatted_transactions:
            tx_data_object = csv.writer(formatted_transactions)
            tx_data_object.writerow(new_header_list)

            for row in data_row_list:
                tx_data_object.writerow(row)

        return f'{self.thor_transactions_filepath} has been modified!' 


