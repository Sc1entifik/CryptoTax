#!/bin/bash
echo "This shell script creates the following directories and files."
echo "Make sure to replace dummy information in tax_jurisdiction_percentages.csv with your tax jurisdiction percentages."
echo ""
echo "CryptoTax/CSV/OtherInformation/tax_jurisdiction.csv"
echo "CryptoTax/CSV/ScheduleCIncome/Archive"
echo "CryptoTax/CSV/ScheduleCWriteoffs/Archive"
echo "CryptoTax/CSV/ScheduleCQuarterlyPayments/Archive"
mkdir -p -v CSV/ScheduleCIncome/Archive
mkdir -p -v CSV/ScheduleCWriteoffs/Archive
mkdir -p -v CSV/ScheduleCQuarterlyPayments/Archive
mkdir -p -v CSV/OtherInformation
cat << EOF > CSV/OtherInformation/tax_jurisdiction_percentages.csv
federal,state,local
.12,.0307,.017
EOF
