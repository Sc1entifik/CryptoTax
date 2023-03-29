# CRYPTO TAX

## DISCLAIMER!!!
**I AM NOT A TAX PROFESSIONAL AND AM NOT RESPONSIBLE FOR YOU NOT FILLING YOUR TAXES OUT CORRECTLY!** 

**MAKE SURE TO FOLLOW ALL TAX CODES FOR YOUR COUNTRY OR TAX JURISDICTION**

**THIS PROJECT IS NOT DESIGNED TO FILL OUT YOUR TAXES FOR YOU BUT TO AIDE YOU IN GATHERING THE INFORMATION YOU NEED TO FILL THEM OUT YOURSELF OR TO HAVE A REAL TAX PFOFESSIONAL FILL THEM OUT FOR YOU.**

**THIS SOFTWARE IS BUILT BY ONE PERSON FOR PERSONAL AND NOT COMMERCIAL USE. I TRY TO BE THOROUGH IN TESTING MY CODE BUT THAT DOES NOT MEAN THERE CAN'T BE UNDISCOVERED BUGS. TRIPPLE CHECK ALL YOUR FORMS FOR ERRORS**

**ANY REDISTRIBUTION OF THIS SOFTWARE ESPECIALLY FOR COMMERCIAL USE IS STRICTLY PROHIBITED**


## Mission
This program is designed to gather transaction data from Blockchain explorers and label that data for tax preparation. 


## How to use
As of now there is no support for any forms other than US tax forms.

This is just an overview discription and each item listed here will be further discussed in the instructions section.

- Enter your wallet addresses into the your_wallet_addresses.csv file for each relevant L1 Blockchain in the YourWallets folder in the CSV folder. Each L1 Blockchain will have one of these.
- Use the UX to dl all transaction forms for your tax period to the Blockchain transaction folder for the Blockchains that you interact with.
- Fill out the other CSV data forms in the CSV OtherForms folder this will cover things like bridging addresses. There will only be one of these for each type of address as no two blockchains should ever have an identical bridging address for example.
- Use the UX to label all transactions. This option will access your wallet addresses and other addresses listed in OtherForms such as Bridge addresses to label all the transactions in the files in your Blockchain transaction folders.
- Check your Blockchain transactions folders. Look at all the files in there for this year and make sure all the transactions are now labeled properly and are not missing any labels.
- Use the UX and choose fill out form, choose form type and a form will be generated with the data needed to fill that form out in your TaxForms folder.
- Tripple check everything it only takes one mistake or one software bug to effect all forms you are filling out or having a tax professional fill out for you.
- Once you are happy and confidant with your results go back to the UX and choose Archive current year. Your tax data and transaction data forms will be moved to the Archive folder in their relevant form type year subfolders.
- Contragulations you now can fill your own taxes out using these forms or send a copy of them to your tax professional.


## Version features
- v.01: Initial Commit. Barely getting started not functioning. Do not use yet. Includes .gitignore due to wanting to keep any tax information which may accidently get pushed to this repository private.

- v.0.4: 
	1. Renamed taxtool.py to quarterly.py in order to create more .py files for seperation of concerns. 
	2. Created create_directories.sh to create needed directories for program to run properly while being able to push to repository without pushing sensitive files.
	3. quarterly.py will now create quarterly income and writeoff files and can use them to fill out a quarterly payment slip. 

## Upcoming features
- Download transactions csv files from blockchain explorers.
- Labeling transactions in blockchain transaction csv files.
- More automated tax forms coming!
