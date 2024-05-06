"""
Module Name: v2board 动态倍率脚本(适配 1.7.4)
Author: Linki <https://t.me/is_linki>
Group: 维护交流群 <https://t.me/idcntools>
Date: 2024-05-06
Description: 使用 v2board 后端提供的 Api 配合 Linux Crontab 定时任务实现动态调整节点倍率.
"""

from datetime import datetime

import yaml
import requests
import copy
import pytz

shanghai_tz = pytz.timezone('Asia/Shanghai')

def get_time_prefix():
    return f"{datetime.now(shanghai_tz).strftime("%Y-%m-%d %H:%M:%S")}: "

def is_time_between(start_time_str, end_time_str):
    current_time = datetime.now(shanghai_tz).time()
    start_time = datetime.strptime(start_time_str, "%H:%M").time()
    end_time = datetime.strptime(end_time_str, "%H:%M").time()
    if start_time > end_time:
        raise Exception(f"{get_time_prefix()}开始时间不能大于结束时间 {start_time} -> {end_time}")
    return start_time <= current_time <= end_time


class V2BClient:

    def __init__(self, host, admin_path, admin_account, admin_password) -> None:
        self.host = host
        self.admin_path = admin_path
        self.admin_account = admin_account
        self.admin_password = admin_password
        self.auth_data = None
        self.__login()
        self.headers = {
            "Host": self.host,
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "sec-ch-ua-mobile": "?0",
            "authorization": "",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "sec-ch-ua-platform": '"Windows"',
            "Accept": "*/*",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Accept-Encoding": 'utf-8',
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
        

    def __has_auth_data(self) -> bool:
        if self.auth_data == "" or not self.auth_data:
             raise Exception(f"{get_time_prefix()}没有授权数据")
    
    def __login(self) -> None:
        api = f"https://{self.host}/api/v1/passport/auth/login"
        data = {
            "email": self.admin_account,
            "password": self.admin_password
        }
        res = requests.post(api, data, verify=False)
        # print(res.text)
        if res.status_code == 200:
            res = res.json()["data"]
            # print(res)
            if res["is_admin"] != 1:
                raise Exception(f"{get_time_prefix()}配置文件中的V2Board账户不是管理员")
            # print("auth_data:", res["auth_data"])
            self.auth_data =  res["auth_data"]
            print(f"{get_time_prefix()}登录成功")
        else:
            raise Exception(f"{get_time_prefix()}登录请求失败, status_code: {res.status_code} msg: {res.json()["message"]}")
    
    def get_nodes(self) -> list:
        self.__has_auth_data()
        api = f"https://{self.host}/api/v1/{self.admin_path}/server/manage/getNodes"
        headers = self.headers
        headers["authorization"] = self.auth_data
        # print(self.auth_data)
        # print(headers)
        res = requests.get(api, headers=headers, verify=False)
        if res.status_code == 200:
            print(f"{get_time_prefix()}成功获取节点数据")
            return res.json()["data"]
        else:
            raise Exception(f"{get_time_prefix()}请求失败api: {api}, status_code: {res.status_code}, msg: {res.json()["message"]}")
        
    def batch_change(self, update_nodes_data=[]) -> None:
        self.__has_auth_data()
        headers = self.headers
        headers["authorization"] = self.auth_data
        for node_data in update_nodes_data:
            post_data = dict()
            for k, v in node_data.items():
                if k == "group_id":
                    for id in v:
                        post_data[f"group_id[{v.index(id)}]"] = id
                else:
                    post_data[k] = v
            if not post_data["type"]:
                raise Exception(f"{get_time_prefix()}修改节点ID {post_data["id"]} 时缺少节点类型数据")
            api = f"https://{self.host}/api/v1/{self.admin_path}/server/{post_data["type"]}/save"
            res = requests.post(api, headers=headers, data=post_data, verify=False)
            if res.status_code == 200:
                print(f"{get_time_prefix()}修改{post_data["type"]}节点{post_data["id"]} 为 {post_data["rate"]} 倍率 成功。")
            else:
                print(f"{get_time_prefix()}修改{post_data["type"]}节点{post_data["id"]} 为 {post_data["rate"]} 倍率 失败。")
        

class DynamicRate:

    def __init__(self) -> None:
        self.config = self.__load_config()
        self.v2b_client = V2BClient(self.config["host"], self.config["admin_path"],self.config["admin_account"] ,self.config["admin_password"])

    def __load_config(self) -> dict:
        with open("config.yaml", "r") as file:
            config = yaml.safe_load(file)
        check_keys = ["host", "admin_path", "admin_account", "admin_password","nodes"]
        for key in check_keys:
            if not config[key]:
                raise Exception(f"{get_time_prefix()}config.yaml 中没有必要的key: {key} ")
        return config
    
    def change_rate(self):
        # 获取节点
        exist_nodes = self.v2b_client.get_nodes()
        # 匹配到指定节点
        config_nodes = self.config["nodes"]
        update_nodes_data = []
        for config_node in config_nodes:
            for exist_node in exist_nodes:
                if exist_node["id"] == config_node["id"] and exist_node["type"] == config_node["type"]:
                    for item in config_node["rate_config"]:
                        if is_time_between(item["start_time"], item["end_time"]):
                            temp = copy.deepcopy(exist_node)
                            temp["rate"] = item["rate"]
                            update_nodes_data.append(temp)
        # 更新节点
        self.v2b_client.batch_change(update_nodes_data)


if __name__ == "__main__":
    dm_rate = DynamicRate()
    dm_rate.change_rate()