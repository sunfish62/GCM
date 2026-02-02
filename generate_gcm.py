# generate_gcm.py creates a new GnuCash gcm file to manage register columns by account type
# Defined account types in this code are: BANK, CREDIT, INCOME, LIABILITY, MUTUAL, STOCK
# GnuCash includes other account types not included here.

import csv

# Mapping account types to their respective column widths as embedded strings
# Change column width values to your preferred values.
# Setting values for a different account type requires adding a named vriable here which matches
# GnuCash's stored account types.

column_widths_by_type = {
    "BANK": """\
date_width=160
num_width=94
reconcile_width=33
balance_width=150
transfer_width=600
debit_width=140
credit_width=140
""",
    "CREDIT": """\
date_width=160
num_width=44
reconcile_width=33
balance_width=150
transfer_width=600
debit_width=140
credit_width=140
""",
    "INCOME": """\
date_width=160
num_width=44
reconcile_width=33
balance_width=150
transfer_width=600
debit_width=140
credit_width=140
""",
    "LIABILITY": """\
date_width=160
num_width=44
reconcile_width=33
balance_width=150
transfer_width=600
debit_width=140
credit_width=140
""",
    "MUTUAL": """\
date_width=160
num_width=44
reconcile_width=33
balance_width=150
transfer_width=600
debit_width=140
credit_width=140
shares_width=120
price_width=120
""",
    "STOCK": """\
date_width=160
num_width=44
reconcile_width=33
balance_width=150
transfer_width=600
debit_width=140
credit_width=140
shares_width=120
price_width=120
""",
}

# Read account information from a CSV file
# account_info.txt format includes a header line at the top, and GUID,TYPE for each account in the file

def read_account_info(filename):
    account_info = []
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header line
        for row in reader:
            if row and len(row) >= 2:  # Ensure there are enough columns
                guid = row[0].strip()
                account_type = row[1].strip()
                account_info.append({"guid": guid, "account_type": account_type})
    return account_info

# Generate GCM content
def generate_gcm(account_info):
    gcm_lines = []
    
    for account in account_info:
        guid = account["guid"]
        account_type = account["account_type"]
        
        if account_type in column_widths_by_type:
            gcm_lines.append(f"[Register {guid}]\n")
            gcm_lines.append(column_widths_by_type[account_type])
            gcm_lines.append("\n")  # Add a newline for separation between accounts
    
    return ''.join(gcm_lines)

# Main execution
if __name__ == "__main__":
    base_filename = "gcm_base.txt"
    input_filename = "account_info.txt"
    post_filename = "gcm_post.txt"
    output_filename = "output.gcm"
    
    # Read the base GCM content
    with open(base_filename, 'r') as base_file:
        base_content = base_file.read()
    
    # Read account information
    account_info = read_account_info(input_filename)
    
    # Generate GCM content
    gcm_content = generate_gcm(account_info)

    # Read the post GCM content
    with open(post_filename, 'r') as post_file:
        post_content = post_file.read()

    # Write the combined content to the output file
    with open(output_filename, 'w') as file:
        file.write(base_content)
        file.write(gcm_content)
        file.write(post_content)

    print(f"GCM file '{output_filename}' generated successfully.")
