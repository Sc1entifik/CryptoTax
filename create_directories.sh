#!/bin/bash
echo "This shell script creates the following directories."
echo ""
echo "CryptoTax/CSV/OtherInformation"
echo "CryptoTax/CSV/PubWallets"
echo "CryptoTax/CSV/ScheduleCIncome/Archive"
echo "CryptoTax/CSV/ScheduleCWriteoffs/Archive"
echo "CryptoTax/CSV/ScheduleCQuarterlyPayments/Archive"
echo "CryptoTax/CSV/8949c/Archive"
echo ""
echo "After running this script please run create_files.sh to create the needed files for the software to run correctly."
mkdir -p -v CSV/OtherInformation
mkdir -p -v CSV/PubWallets
mkdir -p -v CSV/ScheduleCIncome/Archive
mkdir -p -v CSV/ScheduleCWriteoffs/Archive
mkdir -p -v CSV/ScheduleCQuarterlyPayments/Archive
mkdir -p -v CSV/8949c/Archive
