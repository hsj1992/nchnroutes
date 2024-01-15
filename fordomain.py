import subprocess
import socket
import sys
import requests

def nslookup_domain(domain):
    try:
        # 使用 socket.getaddrinfo 获取域名对应的 IP 地址
        addr_info = socket.getaddrinfo(domain, None, socket.AF_INET)
        ip_addresses = [ip for _, _, _, _, (ip, _) in addr_info]
        return ip_addresses
    except (socket.gaierror, IndexError, UnicodeError):
        return []

def process_url(url):
    ip_array = []
    failed_domains = []

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (e.g., 404)

        for line in response.text.split('\n'):
            # 使用 split 方法以冒号为分隔符，获取冒号后的域名部分
            domain = line.strip().split(':', 1)[-1].strip()
            ip = nslookup_domain(domain)
            if ip:
                ip_array.append(ip)
            else:
                failed_domains.append(domain)

        print("IP Addresses:")
        print(ip_array)

        print("\nFailed to resolve domains:")
        print(failed_domains)

        return ip_array

    except requests.RequestException as e:
        print(f"Error fetching data from URL: {e}")
        return None

# 示例用法
force_cn_list_url = 'http://192.168.31.4:7889/force_nocn_list.txt'
ip_array_force_cn = process_url(force_cn_list_url)
# 替换最后一位为0并添加子网掩码长度
modified_ips = [f"{ip.rsplit('.', 1)[0]}.0/24" for sublist in ip_array_force_cn for ip in sublist if ip != '0.0.0.1']

# 去重
flat_ip_array = list(set(modified_ips))

# 将 ip_array_force_cn 用于 produce.py 的 --exclude 参数
exclude_param = " ".join(ip for ip in flat_ip_array)
print(f"\nUsing --exclude parameter in produce.py: {exclude_param}")

# 执行 produce.py 脚本，传递 --next 参数
next_hop_param = "192.168.31.55"
subprocess.run([sys.executable, "produce.py", "--exclude", exclude_param, "--next", next_hop_param])
