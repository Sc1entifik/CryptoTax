import csv
import requests
import os
import numpy as np
from selenium import webdriver

def dict_reader(csv_file):
    return_dict = {}
    with open(csv_file, 'r', newline='') as csv_dict:
        dict_object = csv.DictReader(csv_dict)
        
        for key_value_pair in dict_object:
            return_dict.update(key_value_pair)

    return return_dict 


# QuarterlyTaxes class generates input forms and uses those forms to automate quarterly tax forms
class QuarterlyTaxes():
    quarterly_date_range = {1:'Jan_to_March', 2:'April_to_May', 3:'June_to_August', 4:'September_to_December'}
    schedule_c_income_filepath = '../CSV/ScheduleCIncome'
    schedule_c_writeoffs_file_path = '../CSV/ScheduleCWriteoffs'
    scedule_c_quarterly_payments_file_path = '../CSV/ScheduleCQuarterlyPayments'
    tax_percentages_dict = dict_reader(f'../CSV/OtherInformation/tax_jurisdiction_percentages.csv')
    federal_percentage = float(tax_percentages_dict.get('federal'))
    state_percentage = float(tax_percentages_dict.get('state'))
    local_percentage = float(tax_percentages_dict.get('local'))


    #tax year in yyyy format
    def __init__(self, tax_year):
        self.due_date_dict = {1: f'04/15/{tax_year}', 2: f'06/15/{tax_year}', 3: f'09/15/{tax_year}', 4: f'01/15/{tax_year + 1}'}


    def _quarterly_csv_form_generator(self, full_file_path, header, first_row):

        with open(full_file_path, 'w') as write_off_form:
            writer = csv.writer(write_off_form)
            writer.writerow(header)
            writer.writerow(first_row)

        return f'{full_file_path} has been created!'


    def _return_csv_column_as_list(self, file_path, key):
        column_list = []

        with open(file_path, 'r') as csv_table:
            csv_dict = csv.DictReader(csv_table)
            for row in csv_dict:
                column_list.append(row.get(key))

        return column_list
    

    def generate_quarterly_schedule_c_forms(self):
        schedule_c_form_types = ['income', 'writeoff']

        for form_type in schedule_c_form_types:
            for quarter in self.due_date_dict:
                file_path = f'{QuarterlyTaxes.schedule_c_income_filepath}/schedule_c_q{quarter}_income.csv' if form_type == 'income' else f'{QuarterlyTaxes.schedule_c_writeoffs_file_path}/schedule_c_q{quarter}_writeoffs.csv'
                header = ['date', 'income'] if form_type == 'income' else ['date', 'write_off_description', 'write_off_amount']
                first_row = [self.due_date_dict.get(quarter), None] if form_type == 'income' else [self.due_date_dict.get(quarter), None, None]

                print(self._quarterly_csv_form_generator(file_path, header, first_row))

        return f'Quarterly schedule C income and writeoff input forms for the current tax year have been created in {QuarterlyTaxes.schedule_c_income_filepath} and {QuarterlyTaxes.schedule_c_writeoffs_file_path}!\nExample row is written in each file replace with real data.'


    def fill_out_quarterly_form(self, quarter):
        income_path = f'{QuarterlyTaxes.schedule_c_income_filepath}/schedule_c_q{quarter}_income.csv'
        deductions_path = f'{QuarterlyTaxes.schedule_c_writeoffs_file_path}/schedule_c_q{quarter}_writeoffs.csv'
        quarterly_form_filepath = f'{QuarterlyTaxes.scedule_c_quarterly_payments_file_path}/schedule_c_q{quarter}_payment.csv'
        total_income = round(sum(map(float, self._return_csv_column_as_list(income_path, 'income'))), 2)
        total_deductions = round(sum(map(float, self._return_csv_column_as_list(deductions_path, 'write_off_amount'))), 2)
        
        with open(quarterly_form_filepath, 'w') as quarterly_form:
            writer = csv.writer(quarterly_form)
            header = ('date_sent', 'income', 'deductions', 'federal_tax', 'state_tax', 'local_tax')
            payment = lambda x: round((total_income - total_deductions) * x, 2)
            row = [self.due_date_dict.get(quarter), total_income, total_deductions, payment(QuarterlyTaxes.federal_percentage), payment(QuarterlyTaxes.state_percentage), payment(QuarterlyTaxes.local_percentage)]
            writer.writerow(header)
            writer.writerow(row)

        return f'{quarterly_form_filepath} has been created!'
        

    

        


    
        


