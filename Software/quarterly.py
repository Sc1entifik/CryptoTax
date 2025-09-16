import csv

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

    '''
    def _return_csv_column_as_list(self, file_path, key):
        column_list = []

        with open(file_path, 'r') as csv_table:
            csv_dict = csv.DictReader(csv_table)
            for row in csv_dict:
                column_list.append(row.get(key))

        return column_list
    '''


    def _unique_business_names_set(self, income_dictionaries):
        unique_business_names = set()

        for income_dictionary in income_dictionaries:
            unique_business_names.add(income_dictionary.get("business_name"))

        return unique_business_names


    def _income_and_deductions_dictionaries(self, quarter):
        income_csv_path = f'{QuarterlyTaxes.schedule_c_income_filepath}/schedule_c_q{quarter}_income.csv'
        deductions_csv_path = f'{QuarterlyTaxes.schedule_c_writeoffs_file_path}/schedule_c_q{quarter}_writeoffs.csv'

        with open(income_csv_path, 'r') as income_table:
            income_iterator = csv.DictReader(income_table)
            income_dictionaries = list(income_iterator)

        with open(deductions_csv_path, 'r') as deductions_table:
            deductions_iterator = csv.DictReader(deductions_table)
            deductions_dictionaries = list(deductions_iterator)


        return income_dictionaries, deductions_dictionaries




    def _tax_estimates_list(self, quarter):
        income_dictionaries, deduction_dictionaries = self._income_and_deductions_dictionaries(quarter)
        business_names = self._unique_business_names_set(income_dictionaries)
        due_date = self.due_date_dict.get(quarter)
        tax_estimates = []
        
        for business in business_names:
            business_income = sum(int(income_object.get("income")) for income_object in income_dictionaries if income_object.get("business_name") == business)
            business_writeoff = sum(int(deduction_object.get("write_off_amount")) for deduction_object in deduction_dictionaries if deduction_object.get("business_name") == business)
            taxable_income = business_income - business_writeoff if business_income - business_writeoff > 0 else 0
            federal_payment = round(taxable_income * QuarterlyTaxes.federal_percentage, 2) 
            state_payment = round(taxable_income * QuarterlyTaxes.state_percentage, 2) 
            local_payment = round(taxable_income * QuarterlyTaxes.local_percentage, 2) 
            tax_estimates.append([due_date, business, business_income, business_writeoff, federal_payment, state_payment, local_payment])
    
        return tax_estimates


    def generate_quarterly_schedule_c_forms(self):
        schedule_c_form_types = ['income', 'writeoff']

        for form_type in schedule_c_form_types:
            for quarter in self.due_date_dict:
                file_path = f'{QuarterlyTaxes.schedule_c_income_filepath}/schedule_c_q{quarter}_income.csv' if form_type == 'income' else f'{QuarterlyTaxes.schedule_c_writeoffs_file_path}/schedule_c_q{quarter}_writeoffs.csv'
                header = ['date', 'business_name', 'income'] if form_type == 'income' else ['date', 'business_name', 'write_off_description', 'write_off_amount']
                first_row = [self.due_date_dict.get(quarter), None] if form_type == 'income' else [self.due_date_dict.get(quarter), None, None]

                print(self._quarterly_csv_form_generator(file_path, header, first_row))

        return f'Quarterly schedule C income and writeoff input forms for the current tax year have been created in {QuarterlyTaxes.schedule_c_income_filepath} and {QuarterlyTaxes.schedule_c_writeoffs_file_path}!\nExample row is written in each file replace with real data.'


    def fill_out_quarterly_form(self, quarter):
        quarterly_form_filepath = f'{QuarterlyTaxes.scedule_c_quarterly_payments_file_path}/schedule_c_q{quarter}_payment.csv'
        
        with open(quarterly_form_filepath, 'w') as quarterly_form:
            writer = csv.writer(quarterly_form)
            header = ('date_sent', 'business_name', 'income', 'deductions', 'federal_tax', 'state_tax', 'local_tax')
            tax_estimates = self._tax_estimates_list(quarter) 
            writer.writerow(header)
            writer.writerows(tax_estimates)

        return f'{quarterly_form_filepath} has been created!'
        

quarter_forms = QuarterlyTaxes(2025)
#print(quarter_forms.generate_quarterly_schedule_c_forms())
#print(quarter_forms.fill_out_quarterly_form(1))
#print(quarter_forms.fill_out_quarterly_form(2))
#print(quarter_forms.fill_out_quarterly_form(3))
#print(quarter_forms.fill_out_quarterly_form(4))
