import yaml
from dynamic_rate import V2BClient
import datetime
from dynamic_rate import is_time_between

# print(datetime.datetime.now())


# def read_yaml_config(file_path):
#     with open(file_path, 'r') as file:
#         config = yaml.safe_load(file)
#     return config

# # 示例用法
# config_data = read_yaml_config('config.yaml')
# print(config_data)

# v2b_client = V2BClient(config_data["host"], config_data["admin_path"],config_data["admin_account"] ,config_data["admin_password"])
# for i in v2b_client.get_nodes():
#     print(i)

print(is_time_between("15:00", "2:00"))



