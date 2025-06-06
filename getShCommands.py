import netmiko
import textfsm
import json
import re
from netmiko import ConnectHandler

# read contents of netLoop.json and contain it in a variable called file
with open('netLoop.json', 'r') as file:
    
    # convert json data types to python data types using .load 
    # and contain it in a variable called jsonConfig
    jsonConfig = json.load(file)

# parse data from jsonConfig to separate variables
device_info = jsonConfig['device']
loopback1 = jsonConfig['loopback1_config']
loopback2 = jsonConfig['loopback2_config']
new_hostname = jsonConfig['new_hostname']
internet = jsonConfig['net_config']
set = jsonConfig['line_and_ip']

# connect to the device based on device_info data
accessCli = ConnectHandler(**device_info)

# send a show command to the cli and contain the output in a variable called sh_ip
# textfsm is optional and is used only for converting the output to a non-wordwrap output 
sh_ip = accessCli.send_command('sh ip int br', use_textfsm=True)

# create and then open the json file
with open('sh_ip_int_br.json', 'w') as blankFile:
    
    # convert the object type into str in order to write it into json
    content = json.dumps(sh_ip, indent=2)
    
    # write the content into the json file
    blankFile.write(content)


## Experiment with python reading specific lines of a json file
# read the json file and iterate through its contents
with open('sh_ip_int_br.json', 'r') as readFile:
    
    # make python read through the json file, then output as specific ip address: 192.168.102.5
    readContent = json.load(readFile)
    for i in readContent:
        ints = i['ip_address']
        
        # specify a string that ends with 2.5
        regex = r'2.5$'
        output = re.search(regex, ints)
        if output:
            print(ints)
        
accessCli.disconnect
