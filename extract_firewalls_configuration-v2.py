import os
import getpass
from netmiko import ConnectHandler
from datetime import datetime

def ReadFile(inFile):
    # Function to read .txt files into python list
    with open(inFile, "r") as f:
        content = f.readlines()   
    content = [x.strip() for x in content]
    return content

def Parse_FW_configuration(FW, username, password):
    # Read FW configuration/routes and add them to .txt files
    FW_name = FW[0]
    FW_IP = FW[1]
    FW_Company = FW[2]
    
    device = ConnectHandler(device_type='fortinet', ip=FW_IP, username=username, password=password)
    device.send_command_timing('cli', 2, 1500)  # To decide where to start (2,1500) used for delay and waiting time
    configLines = device.send_command_timing('show full-configuration', 2, 1500)
    routeLines = device.send_command_timing('get router info routing-table details', 2, 1500)
    configLines = str(configLines)
    
    # Add datetime stamp to filenames
    timestamp = datetime.now().strftime("%Y%m%d")  # YearMonthDay
    # timestamp = datetime.now().strftime("%Y%m%d%H%M%S") # YearMonthDayHourMinuteSecond
    root_folder = "Firewall_config_backup_" + timestamp
    if not os.path.exists(root_folder):
        os.makedirs(root_folder)
    
    company_folder = os.path.join(root_folder, FW_Company)
    if not os.path.exists(company_folder):
        os.makedirs(company_folder)
    
    # Write configuration and routes to files within company folder
    configFile = open(os.path.join(company_folder, FW_name + "_config_" + timestamp + ".txt"), "w")
    configFile.write(configLines)
    routeFile = open(os.path.join(company_folder, FW_name + "_routes_" + timestamp + ".txt"), "w")
    routeFile.write(routeLines)
    configFile.close()
    routeFile.close()
    device.disconnect()

# Extract configuration and routes from the FW :

firewallsData = ReadFile("FirewallsData.csv")
FWsDic = {}
unParsedFW = []

# Prompt for username and password
FW_Username = input("Enter the username: ")
FW_Password = getpass.getpass("Enter the password: ")

for line in firewallsData[1:]:  # Start from 1 to neglect the header line
    name, ip, company = line.split(',')
    FWsDic[name + "_" + ip] = [name + "_" + ip, ip, company.strip()]  # Removed platform from the dictionary
    unParsedFW.append(name + "_" + ip)

for FW in FWsDic.values():
    print(FW)

while len(unParsedFW) != 0:
    for fw in unParsedFW:
        try:
            print("try ", fw)
            Parse_FW_configuration(FWsDic[fw], FW_Username, FW_Password)
            unParsedFW.remove(fw)
            print(fw, "Done")
            print("Remaining FWs List:")
            print(unParsedFW)
        except Exception as error: 
            print(error)
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>error " + str(fw))
            continue
