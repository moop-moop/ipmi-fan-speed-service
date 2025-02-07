import ipmi_fan_speed_service.utils as utils
import os

# define input parameter dictionary: network interface, username, password

def main():
    connection = {
        "network_interface": os.environ["IPMI_NETWORK_INTERFACE"],
        "username": os.environ["IPMI_USERNAME"],
        "password": os.environ["IPMI_PASSWORD"]
    }
    temp = utils.get_system_temp(connection)
    utils.set_fan_speed(connection, temp)

if __name__ == "__main__":
    main()
