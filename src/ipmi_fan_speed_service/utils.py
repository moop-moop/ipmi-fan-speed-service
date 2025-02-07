import logging
import subprocess
from enum import Enum

logging.basicConfig(filename='ipmi_debug.log', filemode='w', level=logging.DEBUG)

class IPMICommands(Enum):
    base = "raw 0x30"
    SET_ALL_FANS = f"{base} 0x30 0x02 0xff"
    ENABLE_MANUAL_FAN_CONTROL = f"{base} 0x30 0x01 0x00"
    DISABLE_MANUAL_FAN_CONTROL = f"{base} 0x30 0x01 0x01"
    THIRD_PARTY_PCIE_RESPONSE_STATE = f"{base} 0xce 0x01 0x16 0x05 0x00 0x00 0x00"
    ENABLE_THIRD_PARTY_PCIE_RESPONSE = f"{base} 0xce 0x00 0x16 0x05 0x00 0x00 0x00 0x05 0x00 0x00 0x00 0x00"
    DISABLE_THIRD_PARTY_PCIE_RESPONSE = f"{base} 0xce 0x00 0x16 0x05 0x00 0x00 0x00 0x05 0x00 0x01 0x00 0x00"
    # GET_EXHAUST_TEMPERATURE = f"{base} 0x46 0x01 0x00"
    # GET_CPU1_TEMPERATURE = f"{base} 0x2c 0x01 0x00"
    # GET_CPU2_TEMPERATURE = f"{base} 0x2c 0x01 0x01"

# function to get the current system temperatures
def get_system_temp(con: dict[str,str]) -> int:
    # Placeholder for actual temperature retrieval logic, e.g., reading from sensors calulated
    return 40

# function to set all the fan speeds
def set_fan_speed(con: dict[str,str], temp: int):
    # 1. get the fan speed from the temperature
    speed = get_speed_from_temp(temp)
    # 2. convert the speed to hex
    speed_hex = int_to_hex(speed)
    # 3. make the ipmi command
    ipmi_cmd = get_ipmi_cmd(con, IPMICommands.SET_ALL_FANS)
    # 4. run the command
    print(f"Setting all fan speeds to {speed}% because the temperature is {temp}°C")
    try:
        output = subprocess.run(f"{ipmi_cmd} {speed_hex}", shell=True, capture_output=True).stdout.decode()
        # 5. log the output
        print(f"output: {output}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to call `{ipmi_cmd} {speed_hex}`: {e}")
    
def get_ipmi_cmd(con: dict[str, str], cmd_enum: Enum) -> str:
    # turn con['network_interface'] into an ip address
    ip = get_ip_network_interface(con['network_interface'])
    # make the base command
    base_cmd = f"ipmitool -I lanplus -H {ip} -U {con['username']} -P {con['password']}"
    return f"{base_cmd} {cmd_enum.value}"

def int_to_hex(i:int) -> str:
    hex_string = f"0x{i:02X}"
    return hex_string

def get_speed_from_temp(temp:int) -> int:
    # Fan Speed % = 10^((Temp - 35)/15.39) + 11
    # algorithm to set the fan speed based on the temperature, fan speed curve
    return int(10**((temp - 35)/15.39) + 11)

def get_ip_network_interface(net: str) -> str:
    # get the ip address of the network interface
    try:
        result = subprocess.run(f"ip addr show {net}", shell=True, capture_output=True, check=True)
        return result.stdout.decode().split("inet ")[1].split("/")[0]
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to get IP address for network interface {net}: {e}")
        return ""