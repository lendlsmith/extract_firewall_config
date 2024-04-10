from netmiko import ConnectHandler
from datetime import datetime  # Import datetime module

def ReadFile(inFile):
    # Function to read .txt files into python list
    with open(inFile, "r") as f:
        content = f.readlines()   
    content = [x.strip() for x in content]
    return content

def Parse_FW_configuration(FW):
    # Read FW configuration/routes and add them to .txt files
    FW_name     = FW[0]
    FW_IP       = FW[1]
    FW_Username = input("Enter the username: ")
    FW_Password = input("Enter the password: ")  
    
    device = ConnectHandler(device_type='fortinet', ip= FW_IP , username=FW_Username, password=FW_Password)
    device.send_command_timing('cli',2,1500) # To decide where to start (2,1500) used for delay and waiting time
    configLines = device.send_command_timing('show full-configuration',2,1500)
    routeLines = device.send_command_timing('get router info routing-table details',2,1500)
    configLines = str(configLines)
    
    # Add datetime stamp to filenames
    timestamp = datetime.now().strftime("%Y%m%d")  # YearMonthDay
    #timestamp = datetime.now().strftime("%Y%m%d%H%M%S") # YearMonthDayHourMinuteSecond
    configFile = open(FW_name + "_" + timestamp + ".txt" , "w")
    configFile.write(configLines)
    routeFile = open(FW_name + "_routes_" + timestamp + ".txt" , "w")
    routeFile.write(routeLines)
    configFile.close()
    routeFile.close()
    device.disconnect()  

# Extract configuration and routes from the FW :

firewallsData = ReadFile("FirewallsData.csv")
FWsDic = {}
unParsedFW = []

for line in firewallsData[1:]: # Start from 1 to neglect the header line 
    name, ip, platform = line.split(',')
    FWsDic[name + "_" + ip] = [name + "_" + ip, ip] # Removed platform from the dictionary
    unParsedFW.append(name + "_" + ip)

for FW in FWsDic.values():
    print(FW)

while len(unParsedFW) != 0:
    for fw in unParsedFW:
        try:
            print("try ",fw)
            Parse_FW_configuration(FWsDic[fw])
            unParsedFW.remove(fw)
            print(fw, "Done")
            print("Remaining FWs List:")
            print(unParsedFW)
        except Exception as error: 
            print(error)
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>error " + str(fw))
            continue
