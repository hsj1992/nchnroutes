#!/usr/bin/env python3
## 读取config.ini里的PaoPaoDNS中的force_cn.txt，将域名放到域名数组里；
## 将域名进行解析，获取到IP放入IP数组.
import configparser
import socket
import subprocess

# 创建一个ConfigParser对象并读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

# 获取domaintxt_path的值，默认使用DEFAULT部分
domaintxt_path = config.get('DEFAULT', 'domaintxt_path', fallback='')
if domaintxt_path:
    # 读取文件并处理内容
    domains_list = []
    with open(domaintxt_path, 'r') as file:
        for line in file:
            # 去除每行开头的'domain:'字段并去除两端的空白字符
            domain = line.strip().replace('domain:', '')
            # 将提取出的域名添加到列表中
            domains_list.append(domain)

def get_ip_addresses(domain):
    try:
        # 使用gethostbyname_ex获取域名对应的IP地址列表
        _, _, ip_addresses = socket.gethostbyname_ex(domain)
        return ip_addresses
    except (socket.gaierror, UnicodeError) as e:
        print(f"Error resolving domain '{domain}': {e}")
        return []

# 示例用法
all_ip_addresses = []

for domain_to_lookup in domains_list:
    # Skip domains that are not valid or cannot be resolved
    if not domain_to_lookup or '.' not in domain_to_lookup:
        print(f"Invalid or unresolvable domain: {domain_to_lookup}")
        continue

    ip_addresses = get_ip_addresses(domain_to_lookup)

    # Add obtained IP addresses to the overall list
    all_ip_addresses.extend(ip_addresses)

exclude_param = " ".join(f"{ip}/32" for ip in all_ip_addresses)

subprocess.run(["python3", "produce.py", "--exclude", exclude_param])