# GCM
Python Script to write a GnuCash gcm file with column width definitions for all accounts in a data file

BACKGROUND

The open source accounting program GnuCash (www.gnucash.org) uses a system file, called
a '''gcm''' file, to manage the screen layout in GnuCash windows and registers. Each
GnuCash data file has its own gcm file to manage the GnuCash appearance. 

The gcm file is a text file stored in the 'books' folder beneath USER_CONFIG_HOME 
(see https://wiki.gnucash.org/wiki/Configuration_Locations#USER_CONFIG_HOME)
A gcm file contains sections for different GnuCash screen elements, wuch as dialog boxes,
account registers, reports, budgets, and so on. Each section begins with a header, followed
by variable/value pairs on separate lines. An account register for a BANK type account will 
be entered as follows:

[Register c138810137d0f2279b02e8a5bb1df06a]
date_width=160
num_width=94
reconcile_width=33
balance_width=150
transfer_width=600
debit_width=140
credit_width=140

GnuCash only creates a gcm entry for registers that have been adjusted by the user
in some way; otherwise, the program opens an account register with default column widths that 
are apparently embedded in the source code. Unfortunately for me, the defaults aren't to my 
preference, and there doesn't appear to ba any way to set new default column widths without 
changing the source code.

MY SOLUTION

I decided that I could achieve my goal by creating a gcm file with entries for *ALL* the accounts 
in my data file; that way, when I opened an account, GnuCash would use the stored columns for that
account. After some thought, I decided that I was mostly concerned about making settings for some of 
the account types that GnuCash defines. Specifically, I wanted to set column widths for accounts of type: 
   - BANK
   - CREDIT
   - INCOME
   - LIABILITY
   - MUTUAL
   - STOCK

The newly-created gcm file uses the general settings that GnuCash has already created, merged with 
generated register column definitions for all accounts of the above types. I derived the general settings
from a copy of my gcm file. For reasons that are unclear to me, the gcm file places register entries after 
general application settings but before definitions for open windows, and this sequence is important. 
Therefore, I broke the general gcm settings into two pieces--one for the opening section, and one for the 
tail end of the file.

To generate the register sections, I used a CSV file with entries for every account in the data file, 
coupled with their TYPE. I used an SQLite copy of my data file to extract the GUID and TYPE of all accounts
in my data file and then placed this information in a csv file.

The python script included here (generate_gcm.py) uses two gcm source files (gcm_base.txt and 
gcm_post.txt) along with the account csv file (account_info.txt) to generate a new gcm file that contains 
register definitions for all accounts (output.gcm). Each account type that gets a register definition has
a simple text value which defines the different column widths in that register. These variables can be edited 
to suit individual preference.

IMPLEMENTATION AND USE

The script requires three text files:
  1 - gcm_base.txt - the starting portion of your existing gcm file, up to the first register definition
  2 - gcm_post.txt - the concluding portion of your existing gcm file, after the last register definition
  3 - account_info.txt - a comma-separated value text file with the Account GUID and Account type, with a header row

Place these files in the same folder as the script file, and from a command line in that folder, enter
       python ./generate_gcm.py

Following the execution, you will have a new file in the folder: output.gcm

Copy this file into USER_CONFIG_HOME, make a copy of your original gcm file, and then rename output.gcm to your
data file name. For example, if your data file is Accounts, rename Accounts.gcm to Accounts-old.gcm, and then rename
output.gcm to Accounts.gcm

When GnuCash is next opened, all registers of the same type should have the same column definitions. If anything 
fails, delete this file and copy your original gcm file back.


