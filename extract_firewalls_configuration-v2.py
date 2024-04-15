import csv
import os
import datetime
from fortinet_api import FortinetAPI

# Set path for CSV import
csv_file = 'FirewallsData.csv'

# Set the path to the root folder to save exports
root_folder = f'Firewall_Configs_Backup_{datetime.now().strftime("%Y-%m-%d")}'
os.mkdir(root_folder)

# Prompt for credentials
username = input('Enter your Fortinet username: ')
password = getpass.getpass('Enter your Fortinet password: ')

# Read CSV file and extract data
with open(csv_file, 'r') as csv_f:
    reader = csv.reader(csv_f)
    next(reader)  # Skip the header row
    for row in reader:
        hostname = row[0]
        ip = row[1]
        company = row[2]

        # Initialize the FortinetAPI object with the IP and creds
        api = FortinetAPI(hostname, ip_address, username, password)

        # Get firewall config for the hostname
        config = api.get_config()

        # Create new folder in the root folder for the sub
        company_folder = os.path.join(root_folder, company)
        if not os.path.exists(company_folder):
            os.mkdir(company_folder)

        # Save the firewall config to a file in the company folder
        with open(os.path.join(root_folder, company, f'{hostname}_config.txt'), 'w') as config_file:
            config_file.write(config)