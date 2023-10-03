from pathlib import Path

from blockchain import Blockchain

class DefiKingdoms(Blockchain):
    lilas_ledger_url = "https://dfkreport.cognifact.com"
    transactions_filepath = f"{Blockchain.blockchain_transactions_filepath}DFK/"
    dfk_8949_filepath = "./Tax/8949c/"


    def __init__(self):
        super().__init__()
        self.wallet_address_dictionary = dictionary_from_csv(f"{DefiKingdoms.pub_wallets_filepath}ETH/pub_wallets.csv")


    def download_dfk_transactions(self):
        for wallet in self.wallet_address_dictionary.values():
            self.dl_tx_report_link(f"{DefiKingdoms.lilas_ledger_url}{wallet}", f"{DefiKingdoms.transactions_filepath}DFK{wallet}")

        return f"Your default browser has been loaded with links to Lila's Ledger at dfkreport.cognifact.com. Choose your date range for the tax year you are downloading on the webpage, uncheck Harmony blockchain from included chains, then enter the 0xAddress in the Report Generation box then click Generate." 


    def create_8949_from_transactions_csv(self):

        dfk_8949_generated_message = f"New 8949 form generated in {DefiKingdoms.dfk_8949_filepath}. Please check the document for accuracy and make sure that the numbers make sense. Fixes to any missing or incorrect information should be made to the Blockchain tx report used to generate this file and not directly to this file. This is so that you can keep all your records congruent by overwriteing your old file and letting the software do the heavy lifting. Due to the nature of the DFK game and all the smallish swaps, bridges, and transactions made while playing the game it is not abnormal for some information to be missing from the Blockchain tx report which may negatively impact your cost basis thus not maximizing your deductions. For example say you bridged some Jewel from Klaytn to DFK then swapped that Jewel to Crystal on the Crystalvale DEX. The tx report may have the date acquired field slightly wrong or missing because the jewel used to make the swap came from the bridge contract and the DFK blockchain explorer cannot trace the transaction further back because those transactions were made on the Klaytn chain. This usually results in having a cost acquired of zero and not maximizing your deductions. A lot of the time this is not a huge deal because the value of said swap in relation to zero is small, your total tax liability may be at a loss for this year despite not maximizing these deductions, trying to chase down this information for the size and quantity of the missing trade info is just too cumbersome, or some combination of all these factors. Make sure to consult a tax professional if you need assistance or are uncomfortable at this step however as I am not one. Once your accuracy check is complete and you are satisfied with your 8949 form, archive your records for safe keeping. Read instructions for a deep dive into the archival process."
        filepath_list = [item for item in Path(DefiKingdoms.transactions_filepath).iterdir() if item.is_file()]

        for path in filepath_list:
            
            with open(path, "r") as tx_data_from_csv:
                tx_data_object = csv.reader(tx_data_from_csv)
                header_list = next(tx_data_object)
                header_index = {item: header_list.index(item) for item in header_list}
                cap_gains_check = lambda x: x[header_index.get("category")]  == "gains"
                date_time_ternary = lambda x, column_name: "" if x[header_index.get(column_name)] == "" else dt.strptime(x[header_index.get(column_name)], "%Y-%m-%d").strftime("%m-%d-%Y")
                cap_gains_data = []

                for row in tx_data_object:
                    if cap_gains_check(row):
                        cap_gains_row = [
                                row[header_index.get("description")],
                                date_time_ternary(row, "acquired date"),
                                date_time_ternary(row, "sold date"),
                                float(row[header_index.get("proceeds")]),
                                float(row[header_index.get("costs")]),
                                "",
                                "",
                                float(row[header_index.get("gains")])
                                ]
                        cap_gains_data.append(cap_gains_row)
            
            self._generate_8949c(f"{DefiKingdoms.dfk_8949_filepath}{path.stem}.csv", cap_gains_data)

        return dfk_8949_generated_message 

