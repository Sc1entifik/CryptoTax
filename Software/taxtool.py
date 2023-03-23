import csv
import requests
import os
import numpy as np
from selenium import webdriver

def dict_reader(csv_file):
    return_dict = {}
    with open(csv_file, 'r', newline='') as csv_dict:
        dict_object = csv.DictReader(csv_dict)
        
        for kv_pair in dict_object:
            return_dict.update(kv_pair)
            

    return return_dict 


# QuarterlyTaxes class is extra and it's scope is a little outside of this project. However handling quarterly taxes is something we have to do so I included it anyhow.
class QuarterlyTaxes():
    quarterly_date_range = {1:'Jan_to_March', 2:'April_to_May', 3:'June_to_August', 4:'September_to_December'}
    current_worksheets_filepath = 'QuarterlyTaxesFilePath'
    tax_percentages_dict = dict_reader('../CSV/OtherInformation/tax_jurisdiction_percentages.csv')
    federal_percentage = tax_percentages_dict.get('federal')
    state_percentage = tax_percentages_dict.get('state')
    local_percentage = tax_percentages_dict.get('local')

    #tax year in yyyy format
    def __init__(self, tax_year):
        self.due_date_dict = {1: f'04/15/{tax_year}', 2: f'06/15/{tax_year}', 3: f'09/15/{tax_year}', 4: f'01/15/{tax_year + 1}'}
        


